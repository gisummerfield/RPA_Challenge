from NewsScraper import NewsScraper
"""
Example script showing how to use the NewsScraper class.
"""

LAScraper = NewsScraper()                                       # Create NewsScraper object.

##############
### Test 1 ###
##############
# Set search terms.
search_phrase = "Nvidia"
search_range = 2

article_list = LAScraper.search(search_phrase, search_range)    # Perform a search.
LAScraper.export_articles_as_excel(article_list)                # Export articles to Excel file.
LAScraper.zip_images()                                          # Zip images.


##############
### Test 1 ###
##############
# Set search terms.
search_phrase = "spain"
search_range = 2

LAScraper.reset_for_new_search()                                # Research the NewsScraper for a new search.
article_list = LAScraper.search(search_phrase, search_range)    # Perform a search.
LAScraper.export_articles_as_excel(article_list)                # Export articles to Excel file.
LAScraper.zip_images()                                          # Zip images.

LAScraper.browser.close_browser()                               # Close browser.
