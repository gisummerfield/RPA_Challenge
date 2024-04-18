<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>NewsScraper</h1>

<p>NewsScraper is my approach to the RPA Challenge - Fresh news 2.0 challenge. It is a Python tool designed for extracting information from news articles based on a search term and a specified time range. Currently, it only supports extracting data from the LA Times website.</p>

<h2>Features</h2>

<ul>
    <li>Search for news articles based on a search phrase and a specified time range.</li>
    <li>Extract article elements such as title, date, description, and image name.</li>
    <li>Saves the article images in a separate folder.</li>
    <li>Export extracted articles as an Excel spreadsheet.</li>
</ul>

<h2>Installation</h2>

<ol>
    <li>Clone the repository:</li>
    <code>git clone https://github.com/your_username/NewsScraper.git</code>
    <li>Install the required dependencies:</li>
    <code>pip install -r requirements.txt</code>
</ol>

<h2>Usage</h2>

<p>To use NewsScraper, follow these steps:</p>

<ol>
    <li>Modify the <code>search_phrase</code> and <code>search_range</code> variables in the <code>__main__</code> block of the <code>NewsScraper.py</code> script to specify your search criteria.</li>
    <li>Run the <code>NewsScraper.py</code> script:</li>
    <code>python NewsScraper.py</code>
    <li>The tool will initiate a search on the LA Times website, extract relevant articles, and save them as an Excel spreadsheet in the current directory.</li>
</ol>

<h2>Example</h2>

<code>
    <pre>
# Example usage
search_phrase = "Spain"
search_range = 2

LAScraper = NewsScraper()
article_list = LAScraper.search(search_phrase, search_range)
LAScraper.export_articles_as_excel(article_list)
LAScraper.browser.close_browser()
    </pre>
</code>

<h2>Contributing</h2>

<p>Contributions are welcome! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.</p>

</body>
</html>
