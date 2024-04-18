from RPA.Browser.Selenium import Selenium
import logging
import time
from datetime import datetime, date
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
import os
import re
from openpyxl import Workbook
from dateutil.relativedelta import relativedelta
import requests


class NewsScrapper:

    def __init__(self):
        """
        Used to extract information of news articles based on a search term for the last x months.

        Currently the NewsScrapper only works for the LA Times website.
        """
        #
        self.logger = logging.getLogger(__name__)
        logging.info("Started")

        # List of all the articles, will be populated with lists.
        self.articles = []

        self.browser = Selenium()
        self.browser.open_available_browser(
            url="https://www.latimes.com/",
            maximized=True,
            options={
                "arguments": ['--incognito']})

        # This variable is used to ensure that a search cannot occur
        # if the browser is not at the homepage of the website.
        self.at_homepage = True

        # This is the name of the directory where the images are
        # saved and is used as the name of the excel file.
        self.file_name = ""

        time.sleep(2)       # Wait a little extra to ensure everything is loaded before a search occurs.

    @staticmethod
    def string_contains_money(string):
        """
        Return a bool dependant on if a string contains a dollar value.
        Looks for one of the following formats:
        $11.1 | $111,111.11 | 11 dollars | 11 USD
        """
        # Regular expression pattern to match different money formats.
        money_pattern = r'\$[\d,.]+|\b\d+\s*(?:dollars|USD)\b'

        # Search for the pattern in the string
        matches = re.findall(money_pattern, string)

        # If matches are found, return True, otherwise False.
        return bool(matches)

    @staticmethod
    def get_start_of_search_range(months):
        """
        Gets the start of the search range (date) according to the number of search months.

        Returns a datetime object.
        """
        if months < 2:
            return datetime(datetime.now().year, datetime.now().month, 1)
        else:
            return datetime(datetime.now().year, datetime.now(
            ).month, 1) - relativedelta(months=months - 1)

    @staticmethod
    def save_image(directory, image_source, image_filename):
        # Saving image.
        try:
            response = requests.get(image_source)
            if response.status_code == 200:
                with open(directory + "/" + image_filename + ".jpg", 'wb') as f:
                    f.write(response.content)
            else:
                logging.error("Failed to download image. Status code:", response.status_code)
        except Exception as e:
            logging.error("Error occurred:", e)


    def extract_article_elements(self, element_html, search_phrase):
        """
        Extracts various article elements from the article HTML.

        The entire HTML of the article element is parsed to the BeautifulSoup library.
        BeautifulSoup extracts the title, description, date and image source url.

        Extracted article elements are return as a list in the order:
        title, date, description, image_filename, phrase_count, contains_money, image_source

        Currently only works for the LA Times website.
        """

        soup = BeautifulSoup(element_html, 'html.parser')

        # Extracting title of the article.
        title = soup.find('h3', class_='promo-title').text.strip()

        # Extracting description of the article.
        description = soup.find('p', class_='promo-description').text.strip()

        # Extracting date of the article.
        date = soup.find('p', class_='promo-timestamp').text.strip()

        # Extracting image filename and soruce url.
        image_source = soup.find('img')['src']
        image_filename = image_source.split('%2F')[-1]

        # Determining if the title or description contains a dollar value.
        contains_money = self.string_contains_money(
            title) or self.string_contains_money(description)

        # Counting the number of occurrences of the search phrase in the title or description.
        phrase_count = (title.lower() + description.lower()
                        ).count(search_phrase.lower())

        return [title, date, description, image_filename,
                str(phrase_count), str(contains_money), image_source]

    def search(self, search_phrase: str, search_range: int):
        """
        Initiates a search for articles based on the search
        phrase and search range (months) provided.

        The following steps are followed during the search:

        1. The search bar is first brought up and the search phrase is entered and executed.
           The "Newest" dropdown item is then selected to display the articles in chronological order.
        2. The outerHTML of the articles is captured and sent to the extract_article_elements
           method to extract the needed article elements.
        3. The date of each article is checked to determine if searching should stop
           according to the search range.
        4. If searching should continue then the "next page" button is clicked, steps 2 + 3 are repeated.
           If searching should stop then the the articles list is returned.

        If the bottom of the search page is reached an annoying banner pops up and does not allow
        the clicking of the "next page" button. This raises the exception ElementClickInterceptedException.
        If this exception is raised then the page is reloaded and the next button can be clicked.


        Currently only works for the LA Times website.
        """


        # Return empty list if a search is attempted while not at the homepage.
        if not self.at_homepage:
            logging.warning("Tried to search while not at the homepage!")
            return []

        # No longer at the home page
        self.at_homepage = False
        search_phrase = search_phrase
        search_range = search_range

        # Generate a file/folder name based on the current date and search conditions.
        date_today = date.today()
        self.file_name = str(date_today) + "_" + \
            search_phrase + "_" + str(search_range)
        directory_path = self.file_name

        # Delete files in directory if it already exists
        if os.path.exists(directory_path):
            files = os.listdir(directory_path)
            # Iterate over each file and delete it
            for file in files:
                file_path = os.path.join(directory_path, file)
                # Check if the file is a regular file (not a directory)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            # Directory does not exist, create it
            try:
                os.mkdir(directory_path)
            except Exception as e:
                logging.error(f"Error creating directory: {e}")

        # Execute a search.
        logging.info(
            "Searching for news articles with the phrase \'" +
            search_phrase +
            "\' from the last" +
            str(search_range) +
            " month(s)")
        # Click on the search button.
        self.browser.click_button_when_visible(
            "xpath://*[@data-element='search-button']")
        # Clear the search bar.
        self.browser.clear_element_text(
            "xpath://*[@data-element='search-form-input']")
        # Type a phrase into the search bar.
        self.browser.input_text(
            "xpath://*[@data-element='search-form-input']", search_phrase)
        # Hit enter to perform the search.
        self.browser.press_keys(
            "xpath://*[@data-element='search-form-input']", "ENTER")

        time.sleep(2)

        self.logger.info("Sorting by most recent")
        # Select an item in the dropdown by value
        self.browser.select_from_list_by_value("name:s", "1")

        time.sleep(2)

        # Repeat until article date is outside the search range.
        while True:
            # Find all article elements
            article_elements = self.browser.find_elements(
                "xpath://div[@class='promo-wrapper']")

            # There are usually 10 per page, loop through them.
            for article_element in article_elements:
                # Get outerHTML.
                element_html = self.browser.get_element_attribute(
                    article_element, "outerHTML")

                # Extract element.
                article_info = self.extract_article_elements(
                    element_html, search_phrase)

                # If the article was very recently published then instead of a date
                # it might say "5 hours ago". In this case, make the date today.
                # This might need a revision to make sure of the date.
                if "ago" in article_info[1]:
                    date_object = datetime.today()
                else:
                    # Convert date string to datetime variable
                    if article_info[1][3] == ".":
                        date_object = datetime.strptime(
                            article_info[1], "%b. %d, %Y")
                    else:
                        date_object = datetime.strptime(
                            article_info[1], "%B %d, %Y")

                # Check if the latest article date falls outside the range.
                # Return the articles if it does.
                if self.get_start_of_search_range(search_range) <= date_object:
                    self.articles.append(article_info[:-1])
                    self.save_image(directory_path, article_info[6], article_info[3])
                else:
                    logging.info("Done finding aritcles")
                    return self.articles


            time.sleep(3)

            try:
                # Go to next page of the articles
                self.browser.click_link(
                    "xpath://div[@class='search-results-module-next-page']/a")
            except ElementClickInterceptedException:
                self.browser.reload_page()
                time.sleep(1)
                self.browser.click_link(
                    "xpath://div[@class='search-results-module-next-page']/a")

    def export_articles_as_excel(self, articles):
        """
        Exports all the articles as a excel spreadsheet.

        Deletes file if it already exists.
        """
        if os.path.exists(self.file_name + ".xlsx"):
            os.remove(self.file_name + ".xlsx")

        # Create a new workbook.
        wb = Workbook()
        # Select the active worksheet.
        ws = wb.active
        # Iterate through the list of articles and write each list as a row.
        for row in articles:
            ws.append(row)
        # Save the workbook.
        wb.save(self.file_name + ".xlsx")


if __name__ == "__main__":

    # Test 1
    search_phrase = "Spain"
    search_range = 2

    LAScrapper = NewsScrapper()
    article_list = LAScrapper.search(search_phrase, search_range)
    LAScrapper.export_articles_as_excel(article_list)
    LAScrapper.browser.close_browser()



