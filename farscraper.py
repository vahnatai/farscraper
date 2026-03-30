import argparse
import fandom
import re
import sys
import traceback

fandom.set_wiki('farscape')
fandom.set_lang('en')

DEFAULT_COUNT = 3
FIRST_EP_NAME = 'Premiere'
FIRST_COMIC_NAME = 'Return of the King'

_EPISODE_RE = re.compile(r'Episode\xa0no\..*?<td>Season\xa0(\d+)<br>Episode\xa0(\d+)', re.DOTALL)
_NEXT_RE = re.compile(r'Next\xa0→.*?</td>.*?title="([^"]+)"', re.DOTALL)

argp = argparse.ArgumentParser(
    prog='farscraper',
    description='calculates watch orders for Farscape by scraping the Farscape Encyclopedia Project wiki'
)
argp.add_argument('page_title', type=str, nargs="?")
argp.add_argument('count', type=int, nargs="?", default=DEFAULT_COUNT)

def describe(page):
    match = _EPISODE_RE.search(page.html)
    
    if match:
        season_number = match.group(1)
        episode_number = match.group(2)
        print(f'FAR {season_number}x{episode_number.zfill(2)} "{page.title}"', flush=True)
    else:
        print(f'MOV "{page.title}"', flush=True)

def get_next_released(page):
    match = _NEXT_RE.search(page.html)
    
    if match:
        next_title = match.group(1)
        next = fandom.page(next_title)
        return next
    else:
        raise ValueError('Could not find next episode link')

if __name__ == '__main__':
    args = argp.parse_args()

    count = args.count

    if args.page_title:
        page_title = args.page_title
    else:
        page_title = FIRST_EP_NAME
        page = fandom.page(page_title)
        describe(page)
        count -= 1

    try:
        page = fandom.page(page_title)
    except fandom.error.PageError as e:
        print(e)
        exit()

    for i in range(count):
        try:
            page = get_next_released(page)
            if page.title == FIRST_COMIC_NAME:
                # TODO comics listing
                print('comics listing not yet implemented...', flush=True)
                exit()
            describe(page)
        except Exception as e:
            print('Exception:', e)
            traceback.print_exception(type(e), e, e.__traceback__)
            exit()
