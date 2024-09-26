import sys

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def initialize_webdriver(url, selenium_logger):

    try:
        # Initialize the WebDriver
        driver = webdriver.Edge()

        # # Setup Chrome options for headless mode
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Enable headless mode
        # driver = webdriver.Chrome(options=chrome_options)

        # Open the homepage
        driver.get(url)

        # Wait until the page is fully loaded using document.readyState
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )

        # # Wait for the page to load
        # time.sleep(2)

        # Log successful connection
        selenium_logger.info(f"Website {url} opened successfully")

    except Exception as e:
        selenium_logger.error(
            f"Error while opening the url {url}: \n{type(e).__name__}: {e}"
        )
        sys.exit(1)

    try:
        # Use the id to locate the element
        element = driver.find_element(By.ID, "cookiescript_close")
        element.click()  # Perform the click action
        selenium_logger.info(f"Cookies banner closed succesfully")

    except Exception as e:
        selenium_logger.error(
            f"Error while finding/clicking the cookies element: \n{type(e).__name__}: {e}"
        )
        sys.exit(1)

    return driver


def get_offer_data(data_index, child_div, selenium_logger):

    try:
        inner_div_1 = child_div.find_element(By.TAG_NAME, "div")
        inner_div_2 = inner_div_1.find_element(By.TAG_NAME, "div")
        # Now locate the <a> tag inside the first inner div
        link_element = inner_div_2.find_element(By.TAG_NAME, "a")
        # Extract the href (link) from the <a> tag
        link = link_element.get_attribute("href")

        position_name = inner_div_2.text.split("\n")[0]
        company_name = inner_div_2.text.split("\n")[3]

        new_row = pd.DataFrame(
            [[data_index, link, position_name, company_name]],
            columns=["data_index", "link", "position_name", "company_name"],
        )

    except Exception as e:
        selenium_logger.error(
            f"Error while locating the offer with index {data_index}: \n{type(e).__name__}: {e}"
        )
        sys.exit(1)

    return new_row


def get_offers(driver, selenium_logger):
    # Init the dataframe with offers
    offers_df = pd.DataFrame(
        columns=["data_index", "link", "position_name", "company_name"]
    )

    try:
        # Locate the parent div (using your unique identifier, e.g., data-test-id)
        parent_div = driver.find_element(
            By.CSS_SELECTOR, '[data-test-id="virtuoso-item-list"]'
        )
        parent_div.find_elements(By.XPATH, "./div")[0]
        selenium_logger.info("Located the div with offers list")

    except Exception as e:
        selenium_logger.error(
            f"Error while locating the div with offers list: \n{type(e).__name__}: {e}"
        )
        sys.exit(1)

    try:
        # Retrieve the height of a single offer, window height, whole page height and current scroll position
        order_height = parent_div.find_elements(By.XPATH, "./div")[0].size["height"]
        window_height = driver.execute_script("return window.innerHeight;")
        document_height = driver.execute_script("return document.body.scrollHeight;")
        current_scroll_position = driver.execute_script("return window.scrollY;")
        selenium_logger.info("Website data (height, window height etc.) retrieved")
    except Exception as e:
        selenium_logger.error(
            f"Error while retrieving the website data: \n{type(e).__name__}: {e}"
        )
        sys.exit(1)

    # Scrolling the website and retrieving all the offers
    while current_scroll_position + window_height < document_height:

        print(f'window height: {driver.execute_script("return window.innerHeight;")}')
        try:
            # Find all child divs inside the parent div
            child_divs = parent_div.find_elements(By.XPATH, "./div")
        except Exception as e:
            selenium_logger.error(
                f"Error while retrieving the list of offers: \n{type(e).__name__}: {e}"
            )
            sys.exit(1)

        # Loop through each child div and find nested a tags with links
        for child_div in child_divs:

            try:
                # Extract the 'data-index' attribute from each child div
                data_index = child_div.get_attribute("data-index")
                print(data_index)

            except Exception as e:
                selenium_logger.error(
                    f"Error while retrieving data_index: \n{type(e).__name__}: {e}"
                )
                sys.exit(1)

            if not offers_df["data_index"].isin([data_index]).any():

                new_row = get_offer_data(data_index, child_div, selenium_logger)

                # Append the row using pd.concat()
                offers_df = pd.concat([offers_df, new_row], ignore_index=True)

        try:
            # Scroll height is an order height times number of orders
            # scroll_height = order_height * len(child_divs)
            scroll_height = 80 * len(child_divs)
            print(f"scroll_height: {scroll_height}")
            # Scroll so that more offers load
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")

            # # Wait for the scroll action to complete and new elements to load
            # WebDriverWait(driver, 10).until(
            #     lambda driver: driver.execute_script("return window.scrollY;")
            #     > current_scroll_position
            # )
            # # Wait until the page is fully loaded using document.readyState
            # WebDriverWait(driver, 10).until(
            #     lambda driver: driver.execute_script("return document.readyState")
            #     == "complete"
            # )

            try:
                # Wait until any child div within the parent div has the 'data-index' bigger than the last one found
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//div[@data-index="{int(data_index)+1}"]')
                    )
                )
            except TimeoutException:
                selenium_logger.warning(
                    f"Timeout for data-index {data_index} when looking for a new data-index reched, try to scroll some more"
                )
                driver.execute_script(f"window.scrollBy(0, {scroll_height/2});")

            # Update scroll position and document height for the next loop
            current_scroll_position = driver.execute_script("return window.scrollY;")
            document_height = driver.execute_script(
                "return document.body.scrollHeight;"
            )

        except Exception as e:
            selenium_logger.error(
                f"Error while scrolling the website: \n{type(e).__name__}: {e}"
            )
            sys.exit(1)

    selenium_logger.info("All offers extracted succesfully")

    return offers_df


def get_website_data(url, selenium_logger):

    driver = initialize_webdriver(url, selenium_logger)
    offers_df = get_offers(driver, selenium_logger)

    offers_df.to_csv("offers.csv")

    driver.close()
