import argparse
import fandom
import sys
import traceback

fandom.set_wiki('farscape')
fandom.set_lang('en')

DEFAULT_COUNT = 3
EP_BOX_TOKEN = 'Episode&#160;no.'
SEASON_NUM_TOKEN = '<td>Season&#160;'
EPISODE_NUM_TOKEN = '<br />Episode&#160;'
TITLE_TOKEN = 'title="'
FIRST_EP_NAME = 'Premiere'
FIRST_COMIC_NAME = 'Return of the King'

argp = argparse.ArgumentParser(
    prog='farscraper',
    description='calculates watch orders for Farscape by scraping the Farscape Encyclopedia Project wiki'
)
argp.add_argument('page_title', type=str, nargs="?")
argp.add_argument('count', type=int, nargs="?", default=DEFAULT_COUNT)

def describe(page) :
    index = page.html.find(EP_BOX_TOKEN) + len(EP_BOX_TOKEN)
    episode_snippet = page.html[index: index+100]

    season_index = episode_snippet.find(SEASON_NUM_TOKEN) + len(SEASON_NUM_TOKEN)
    season_end_index = episode_snippet.find('<br />', season_index)
    season_number = episode_snippet[season_index: season_end_index]

    episode_index = episode_snippet.find(EPISODE_NUM_TOKEN) + len(EPISODE_NUM_TOKEN)
    episode_end_index = episode_snippet.find('\n', episode_index)
    episode_number = episode_snippet[episode_index: episode_end_index]

    if season_number and episode_number :
        print('FAR {0}x{1} "{2}"'.format(season_number, episode_number.zfill(2), page.title))
    else :
        print('MOV "{0}"'.format(page.title))
    sys.stdout.flush()

def get_next_released(page) :
    index = page.html.find('Next&#160;→')
    index = page.html.find('</td>', index)
    index = page.html.find(TITLE_TOKEN, index) + len(TITLE_TOKEN)
    endIndex = page.html.find('"', index)
    next_title = page.html[index: endIndex]
    next = fandom.page(next_title)
    return next

if __name__ == '__main__' :
    args = argp.parse_args()

    if args.count :
        count = args.count
    else :
        count = DEFAULT_COUNT

    if args.page_title :
        page_title = args.page_title
    else :
        page_title = FIRST_EP_NAME
        page = fandom.page(page_title)
        describe(page)
        count -= 1
    page = fandom.page(page_title)

    for i in range(count) :
        try :
            page = get_next_released(page)
            if page.title == FIRST_COMIC_NAME :
                # TODO comics listing
                print('comics listing not yet implemented...')
                exit()
            describe(page)
        except Exception as e :
            print('Exception:', e)
            traceback.print_exception(e)
            exit()
