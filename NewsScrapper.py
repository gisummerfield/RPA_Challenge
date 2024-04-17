from RPA.Browser.Selenium import Selenium
import logging
import time
from datetime import datetime, date
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
import os
import stat
import re
from openpyxl import Workbook
from dateutil.relativedelta import relativedelta


class NewsScrapper:

    months = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
    }

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.articles = []

        logging.info("Started")
        self.browser = Selenium()
        self.browser.open_available_browser(url="https://www.latimes.com/", maximized=True,
                                       options={"arguments": ['--incognito']})
        self.at_homepage = True
        self.file_name = ""

        time.sleep(2)

    def string_contains_money(self, string):
        # Regular expression pattern to match different money formats
        money_pattern = r'\$[\d,.]+|\b\d+\s*(?:dollars|USD)\b'

        # Search for the pattern in the string
        matches = re.findall(money_pattern, string)

        # If matches are found, return True, otherwise False
        return bool(matches)

    def get_start_of_search_range(self, months):
        if months < 2:
            return datetime(datetime.now().year, datetime.now().month, 1)
        else:
            return datetime(datetime.now().year, datetime.now().month, 1) - relativedelta(months=months - 1)

    def extract_article_elements(self, element_html, direcory, search_phrase):
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

        self.browser.capture_element_screenshot("xpath://img[@src=\"" + picture_src + "\"]", direcory + "/"
                                                + picture_filename + ".jpg")

        contains_money = self.string_contains_money(title) or self.string_contains_money(description)

        phrase_count = (title.lower() + description.lower()).count(search_phrase.lower())

        return [title, date, description, picture_filename, str(phrase_count), str(contains_money)]


    def search(self, search_phrase: str, search_range: int):
        # Return empty list if a search is attempted while not at the homepage
        if not self.at_homepage:
            logging.warning("Tried to search while not at the homepage!")
            return []

        self.at_homepage = False
        search_phrase = search_phrase
        search_range = search_range

        date_today = date.today()

        self.file_name = str(date_today) + "_" + search_phrase + "_" + str(search_range)
        directory_path = self.file_name

        if os.path.exists(directory_path):
            try:
                os.remove(directory_path)
            except Exception as e:
                print(f"Error deleting directory: {e}")
        else:
            # Directory does not exist, create it
            try:
                os.mkdir(directory_path)
                os.chmod(directory_path, stat.S_IRWXU)
            except Exception as e:
                print(f"Error creating directory: {e}")



        logging.info("Searching for news articles with the phrase \'" + search_phrase + "\' from the last"
                     + str(search_range) + " month(s)")
        # Click on the search button
        self.browser.click_button_when_visible("xpath://*[@data-element='search-button']")
        # Clear the search bar
        self.browser.clear_element_text("xpath://*[@data-element='search-form-input']")
        # Type a phrase into the search bar
        self.browser.input_text("xpath://*[@data-element='search-form-input']", search_phrase)
        # Hit enter to perform the search
        self.browser.press_keys("xpath://*[@data-element='search-form-input']", "ENTER")

        time.sleep(2)

        self.logger.info("Sorting by most recent")
        # Select an item in the dropdown by value
        self.browser.select_from_list_by_value("name:s", "1")

        time.sleep(2)

        while True:

            # Find all article elements
            article_elements = self.browser.find_elements("xpath://div[@class='promo-wrapper']")

            for article_element in article_elements:
                element_html = self.browser.get_element_attribute(article_element, "outerHTML")

                article_info = self.extract_article_elements(element_html, directory_path, search_phrase)
                print(article_info)

                if "ago" in article_info[1]:
                    date_object = datetime.today()
                else:
                    # Convert date string to datetime variable
                    print(article_info[1])
                    if article_info[1][3] == ".":
                        date_object = datetime.strptime(article_info[1], "%b. %d, %Y")
                    else:
                        date_object = datetime.strptime(article_info[1], "%B %d, %Y")

                if self.get_start_of_search_range(search_range) <= date_object:
                    self.articles.append(article_info)
                else:
                    logging.info("Done finding aritcles")
                    return self.articles



            time.sleep(3)

            try:
                # Go to next page of the articles
                self.browser.click_link("xpath://div[@class='search-results-module-next-page']/a")
            except ElementClickInterceptedException:
                self.browser.reload_page()
                time.sleep(1)
                self.browser.click_link("xpath://div[@class='search-results-module-next-page']/a")



    def export_articles_as_excel(self, articles):
        # Create a new workbook
        wb = Workbook()

        # Select the active worksheet
        ws = wb.active

        # Iterate through the list of lists and write each list as a row
        for row in articles:
            ws.append(row)

        # Save the workbook
        wb.save(self.file_name + ".xlsx")




    time.sleep(2)




if __name__ == "__main__":

    # Test 1
    search_phrase = "Spain"
    search_range = 3

    LAScrapper = NewsScrapper()
    article_list = LAScrapper.search(search_phrase, search_range)

    print(article_list)


    LAScrapper.export_articles_as_excel(article_list)

    LAScrapper.browser.close_browser()
