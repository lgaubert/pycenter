# PyCenter

Web Scrapper for Used Section of Guitar Center website

Guitar Center prevents traditional web scrapping by delaying URL parameters from loading until after init page load is complete
To circumvent this, we use a real browser to load the page, and wait to scrape until desired results have loaded
Uses Firefox + Selenium to do this. Geckodrivers needed for Selenium


# Setup
Install geckodrivers in same folder as project
https://github.com/mozilla/geckodriver/releases

Gmail doesn't allow you to auth with normal password, app password will need to be generated
https://support.google.com/accounts/answer/185833?sjid=17230802569285519254-NA
