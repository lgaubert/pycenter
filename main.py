from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
from product import Product
from email.message import EmailMessage
import smtplib
import datetime
import sqlite3
import json
import os
import time
import schedule


def email(new_product):

    email_address = os.environ.get('EMAIL_ADDRESS')
    email_password = os.environ.get('EMAIL_PASSWORD')

    if email_address is None or email_password is None:
        print("Error: Email credentials not found in environment variables.")
        return

    message = EmailMessage()
    message['From'] = email_address
    message['To'] = 'lgaubert@live.com'
    message['Subject'] = 'New Product Added'
    message.set_content(f"A new product has been added:\n\nName: {new_product.name}\nPrice: {new_product.price}\nLocation: {new_product.location}")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(message)



def scrape():
    with open('urls.json', 'r') as file:
        urls_data = json.load(file)

    conn = sqlite3.connect('pycenter.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            display_id TEXT,
            location TEXT,
            date_added DATE
        )
    ''')


    #Verify Geckodrivers are installed in local folder
    webdriver_service = Service('geckodriver')
    driver = webdriver.Firefox(service=webdriver_service)
    product_list = []


    for url_entry in urls_data['urls']:
        name = url_entry['name']
        url = url_entry['url']
        description = url_entry['description']

        print(f"Scraping {name} ({url})")
        driver.get(url)

        # Waits for page to load fully before scrapping
        time.sleep(2.5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        product_divs = soup.find_all('div', class_='product')
        for div in product_divs:
            product_name = div.find('div', class_='productTitle').find('a').text.strip()
            product_price = div.find('span', class_='productPrice').text.strip()
            product_location = div.find('div', class_='storeName').find('a', class_='storeDisplayPop').text.strip()
            product_id = div.find('var', class_='hidden productId').text.strip()

            product = Product(product_name, product_price, product_id, product_location)
            product_list.append(product)

            product.display_info()
            print()


    for product in product_list:
        display_id = product.display_id

        # check if already logged
        cursor.execute("SELECT * FROM products WHERE display_id = ?", (display_id,))
        existing_product = cursor.fetchone()

        if existing_product is None:
            cursor.execute("INSERT INTO products (name, price, display_id, location, date_added) VALUES (?, ?, ?, ?, ?)",
                       (product.name, product.price, product.display_id, product.location, datetime.datetime.now()))
            email(product)


    # close selenium and db connection
    conn.commit()
    conn.close()
    driver.quit()



# schedule job. will not be executed until run_pending is ran
schedule.every(1).minutes.do(scrape)

# Checks for scheduled jo
while True:
    schedule.run_pending()
    time.sleep(60)