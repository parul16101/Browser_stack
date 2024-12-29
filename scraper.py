import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time
from googletrans import Translator
from collections import Counter
import re
import json

translator = Translator()

def run_test(browser_config):
    print(f"Starting test for configuration: {browser_config}")
    
    if browser_config['browser'] == 'Chrome':
        options = ChromeOptions()
    elif browser_config['browser'] == 'Firefox':
        options = FirefoxOptions()
    elif browser_config['browser'] == 'Safari':
        options = SafariOptions()
    else:
        print(f"Unsupported browser: {browser_config['browser']}")
        return

    options.set_capability('browserName', browser_config['browser'])
    options.set_capability('browserVersion', 'latest')
    options.set_capability('bstack:options', {
        'os': browser_config['os'],
        'osVersion': browser_config['os_version'],
        'userName': 'paruldamahe_0ILq2C',
        'accessKey': 'vXhp26yKxbDCosjE7oZy'
    })

    if 'device' in browser_config:
        options.set_capability('bstack:options', {'device': browser_config['device']})

    try:
        print("Connecting to BrowserStack...")
        driver = webdriver.Remote(
            command_executor='https://hub-cloud.browserstack.com/wd/hub',
            options=options
        )
        print("Connected to BrowserStack successfully.")

        print("Navigating to El País Opinion section...")
        driver.get("https://elpais.com/opinion/")

        try:
            print("Waiting for cookie banner...")
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            cookie_button.click()
            print("Cookie banner accepted.")
        except Exception as e:
            print(f"Cookie banner not found or already accepted: {str(e)}")

        print("Waiting for articles to load...")
        time.sleep(5)

        print("Finding articles...")
        articles = driver.find_elements(By.TAG_NAME, "article")[:5]
        print(f"Found {len(articles)} articles.")

        all_translated_titles = []

        for i, article in enumerate(articles, 1):
            try:
                print(f"Processing article {i}...")
                title = article.find_element(By.TAG_NAME, "h2").text
                translated_title = translator.translate(title, dest='en').text
                content = article.find_element(By.CLASS_NAME, "c_d").text
                
                print(f"Article {i}:")
                print(f"Título: {title}")
                print(f"Contenido: {content}\n")
                print(f"Translated: {translated_title}\n")
                sys.stdout.flush()  # Force output to be displayed immediately

                all_translated_titles.append(translated_title)
            except Exception as e:
                print(f"Error processing article {i}: {str(e)}")

        print("Processing word frequencies...")
        all_text = ' '.join(all_translated_titles)
        words = re.findall(r'\w+', all_text.lower())
        word_counts = Counter(words)
        repeated_words = {word: count for word, count in word_counts.items() if count > 2}

        print("Words repeated more than twice across all headers:")
        for word, count in repeated_words.items():
            print(f"'{word}': {count} times")
        sys.stdout.flush()

    except Exception as e:
        print(" ")
    finally:
        if 'driver' in locals():
            print("Closing WebDriver...")
            driver.quit()

def main():
    try:
        print("Loading browser configurations...")
        with open('browserstack.json') as f:
            config = json.load(f)
        
        print("Starting parallel test execution...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(run_test, config['browsers'])
        
        print("Test execution completed.")
    except Exception as e:
        print(f"An error occurred in the main function: {str(e)}")

if __name__ == "__main__":
    main()
