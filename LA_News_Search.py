from robocorp import workitems
from robocorp.tasks import task
# from robocorp.workitems import Input

from NewsScraper import NewsScraper
"""
Example script showing how to use the NewsScraper class.
"""

LAScraper = NewsScraper()                                       # Create NewsScraper object.

@task
def search():
    for input_data in workitems.inputs:
        print("Received payload:", input_data.payload)

        # Set search terms.
        search_phrase = input_data.payload['search_phrase']
        search_range = input_data.payload['search_range']

        article_list = LAScraper.search(search_phrase, search_range)    # Perform a search.
        LAScraper.export_articles_as_excel(article_list)                # Export articles to Excel file.
        LAScraper.zip_images()                                          # Zip images.
        LAScraper.reset_for_new_search()                                # Reset the NewsScraper for a new search.

    LAScraper.browser.close_browser()                               # Close browser.

