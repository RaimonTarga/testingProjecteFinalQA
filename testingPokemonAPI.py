import json
import datetime
import os
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

URL = "https://sixfantasy.github.io/pokemonweb/search.html"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE_NAME = "pokemonAPITestResults.json"
OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_FILE_NAME)
INPUT_FILE_NAME = "pokemonAPITests.json"
INPUT_PATH = os.path.join(ROOT_DIR, INPUT_FILE_NAME)
results = []

try:
    driver = webdriver.Chrome()
    driver.get(URL)
    with open(INPUT_PATH , "r") as f:
        input_data = json.load(f)
    
    for item in input_data:
        try:
            result = {}
            result["search_term"] = item["search_term"]
            result["test_start"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            driver.find_element(By.XPATH, "/html/body/main/search/input").send_keys(item["search_term"])
            sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/search/button").click()
            sleep(5)
            result["correct"] = True
            searchResults = []
            for resultElement in driver.find_elements(By.TAG_NAME, "h2"):
                searchResults.append(resultElement.text)
            for expectedResult in item["expected_results"]:
                if expectedResult not in searchResults:
                    result["correct"] = False
        except NoSuchElementException:
            print("no such element exception in local scope")
        except:
            print("Error with item " + item)
        finally:
            result["test_end"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            results.append(result)
            driver.find_element(By.XPATH,"/html/body/main/search/input").click()
            driver.find_element(By.XPATH, "/html/body/main/search/input").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.XPATH, "/html/body/main/search/input").send_keys(Keys.DELETE)
            sleep(3)
except IOError:
    print("File " + INPUT_FILE_NAME + " doesn't exist or cannot be found")
except NoSuchElementException:
    print("No such element exception IN GLOBAL SCOPE")
except json.JSONDecodeError:
    print("JSON exception")
except:
    print("Unkown exception")
finally:
    print("Testing ended, closing driver")
    driver.close()
    print("Writing results to file " + OUTPUT_PATH)
    with open(OUTPUT_PATH, "w") as outfile:
        outfile.write(json.dumps(results))