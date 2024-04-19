from robocorp.tasks import task
from robocorp import workitems
# from robocorp.workitems import Input

from NewsScraper import NewsScraper
"""
Example script showing how to use the NewsScraper class.
"""

LAScraper = NewsScraper()                                       # Create NewsScraper object.



##############
### Test 1 ###
##############
@task
def search1():
    input_data = workitems.inputs

    # Set search terms.
    search_phrase = input_data['search_phrase']
    search_range = input_data['search_range']

    article_list = LAScraper.search(search_phrase, search_range)    # Perform a search.
    LAScraper.export_articles_as_excel(article_list)                # Export articles to Excel file.
    LAScraper.zip_images()                                          # Zip images.
    LAScraper.browser.close_browser()                               # Close browser.

##############
### Test 1 ###
##############
# Set search terms.
# search_phrase = "spain"
# search_range = 2
#
# LAScraper.reset_for_new_search()                                # Research the NewsScraper for a new search.
# article_list = LAScraper.search(search_phrase, search_range)    # Perform a search.
# LAScraper.export_articles_as_excel(article_list)                # Export articles to Excel file.
# LAScraper.zip_images()                                          # Zip images.
#
# LAScraper.browser.close_browser()                               # Close browser.
