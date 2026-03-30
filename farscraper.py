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
    if match is None:
        raise ValueError('Could not find next episode link')

    next_title = match.group(1)
    next_page = fandom.page(next_title)
    return next_page

if __name__ == '__main__':
    args = argp.parse_args()

    count = args.count

    try:
        if args.page_title:
            page = fandom.page(args.page_title)
        else:
            page = fandom.page(FIRST_EP_NAME)
            describe(page)
            count -= 1
    except fandom.error.PageError as e:
        print(e)
        sys.exit(1)

    for i in range(count):
        try:
            page = get_next_released(page)
            if page.title == FIRST_COMIC_NAME:
                # TODO comics listing
                print('comics listing not yet implemented...', flush=True)
                sys.exit(1)
            describe(page)
        except Exception as e:
            print('Exception:', e)
            traceback.print_exception(type(e), e, e.__traceback__)
            sys.exit(1)
