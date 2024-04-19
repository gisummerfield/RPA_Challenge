from NewsScraper import NewsScraper

LAScraper = NewsScraper()

# Test 1 #
##########
search_phrase = "Nvidia"
search_range = 2

article_list = LAScraper.search(search_phrase, search_range)
LAScraper.export_articles_as_excel(article_list)
LAScraper.zip_images()


# Test 2 #
##########
search_phrase = "spain"
search_range = 2
LAScraper.reset_for_new_search()
article_list = LAScraper.search(search_phrase, search_range)
LAScraper.export_articles_as_excel(article_list)
LAScraper.zip_images()

LAScraper.browser.close_browser()