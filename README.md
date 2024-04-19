<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>NewsScraper</h1>

<p>NewsScraper is my approach to the RPA Challenge - Fresh news 2.0 challenge. It is a Python tool designed for extracting information from news articles based on a search term and a specified time range. Currently, it only supports extracting data from the LA Times website. It is designed to work on the Robocloud platform and accepts Work Items as inputs.</p>

<h2>Features</h2>

<ul>
    <li>Search for news articles based on a search phrase and a specified time range.</li>
    <li>Extract article elements such as title, date, description, and image name.</li>
    <li>Saves the article images in a separate folder.</li>
    <li>Export extracted articles as an Excel spreadsheet.</li>
    <li>Can perform multiple searches provided that the reset_for_new_search() function is used.</li>
    <li>Has the ability to zip all the images into one file (Recommended for Robocloud use).</li>
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
    <li>Create a Roblocloud Task by setting the Origin to this git repository.</li>
    <li>Create an unattended process based on the previously setup task.</li>
    <li>Create any number of work items based on the search phrase and search range. Example: <code>{
    "search_phrase": "Nvidia",
    "search_range": 2
}</code> </li>
    <li>Select and run the work items.</li>
</ol>

<h2>Example</h2>

<pre><code>
        from robocorp import workitems
        from robocorp.tasks import task
    
        from NewsScraper import NewsScraper
        # Example script showing how to use the NewsScraper class.
        
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
    
</code></pre>

<h2>Contributing</h2>

<p>Contributions are welcome! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.</p>

</body>
</html>
