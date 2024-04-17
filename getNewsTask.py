from RPA.Browser.Selenium import Selenium
import logging
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException

logging.basicConfig(filename='getNewsTask.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

search_phrase = "ukraine"

logging.info('Started')
browser = Selenium()

browser.open_available_browser(url="https://www.latimes.com/", maximized=True, options={"arguments": ['--incognito']})

time.sleep(2)

logging.info('Searching for news articles with the phrase \'' + search_phrase + '\' from the last month(s)')
# Click on the search button
browser.click_button_when_visible("xpath://*[@data-element='search-button']")
# Clear the search bar
browser.clear_element_text("xpath://*[@data-element='search-form-input']")
# Type a phrase into the search bar
browser.input_text("xpath://*[@data-element='search-form-input']", search_phrase)
# Hit enter to perform the search
browser.press_keys("xpath://*[@data-element='search-form-input']", "ENTER")

time.sleep(2)

logging.info('Sorting by most recent')
# Select an item in the dropdown by value
browser.select_from_list_by_value("name:s", "1")

time.sleep(2)

articles = []

last_article_reached = False

while not last_article_reached:

    # Find all article elements
    article_elements = browser.find_elements("xpath://div[@class='promo-wrapper']")

    for article_element in article_elements:
        element_html = browser.get_element_attribute(article_element, "outerHTML")

        soup = BeautifulSoup(element_html, 'html.parser')

        # Extracting title of the article
        title = soup.find('h3', class_='promo-title').text.strip()

        # Extracting description of the article
        description = soup.find('p', class_='promo-description').text.strip()

        # Extracting date of the article
        date = soup.find('p', class_='promo-timestamp').text.strip()

        # Extracting picture filename
        picture_src = soup.find('img')['src']
        picture_filename = picture_src.split('%2F')[-1]

        browser.capture_element_screenshot("xpath://img[@src=\"" + picture_src + "\"]", picture_filename + ".jpg")
        articles.append([title, description, date, picture_filename])


    time.sleep(2)



    # Convert date string to datetime variable
    date_object = datetime.strptime(articles[-1][2], "%B %d, %Y")
    # Get current month and year
    current_month = datetime.now().month

    try:
        # Check if the month is this month
        if date_object.month == current_month:
            # Go to next page of the articles
            browser.click_link("xpath://div[@class='search-results-module-next-page']/a")
        else:
            logging.info("Done finding aritcles")
            last_article_reached = True
    except ElementClickInterceptedException:
        browser.reload_page()
        time.sleep(1)
        browser.click_link("xpath://div[@class='search-results-module-next-page']/a")




    time.sleep(2)

print(len(articles))

print(articles)

browser.close_browser()
exit()



