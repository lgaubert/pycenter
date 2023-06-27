# PyCenter

Web Scrapper for Used Section of Guitar Center website

Guitar Center prevents traditional web scrapping by preventing URL parameters from loading until after init page load is complete
To circumvent this, we use a real browser to load the page, and wait to scrape until desired results have loaded
Uses Firefox + Selenium to do this. Geckodrivers will need to be installed in the same folder as project

https://github.com/mozilla/geckodriver/releases
