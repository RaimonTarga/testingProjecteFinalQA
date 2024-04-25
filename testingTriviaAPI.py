import json
import datetime
import os
import random
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

URL = "https://holoturia.github.io/Trivia-API/triviaGame.html"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE_NAME = "triviaAPITestResults.json"
OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_FILE_NAME)
results = []

try:
    driver = webdriver.Chrome()
    driver.get(URL)
    categorySelect = Select(driver.find_element(By.XPATH, "/html/body/main/div/div[1]/div[1]/select"))
    for i in range(0,9):
        try:
            result = {}
            result["test_start"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            categorySelect.select_by_index(i)
            result["category"] = categorySelect.first_selected_option.text
            driver.find_element(By.XPATH, "/html/body/main/div/div[1]/button").click()
            sleep(10)
            result["question"] = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/p[2]").text
            result["choice"] = random.randrange(1,5)
            buttonID = "a"+str(result["choice"])
            result["answer"] = driver.find_element(By.ID, buttonID).text
            driver.find_element(By.ID, buttonID).click()
            sleep(5)
            try:
                driver.find_element(By.ID, "bob")
                result["correct"] = True
            except NoSuchElementException:
                result["correct"] = False
        except NoSuchElementException:
            print("Question didn't load, waiting 5 seconds")
            sleep(5)
        except:
            print("Error with index " + i)
        finally:
            result["test_end"] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            results.append(result)
            sleep(3)
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