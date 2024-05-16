import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import datetime

class TestCheckRegion:
    @pytest.fixture
    def browser(self, request):  
        driver = webdriver.Chrome()
        driver.maximize_window()
        request.addfinalizer(driver.quit)
        return driver

    def test_check_region(self, browser):
        try:
            # Step 1
            browser.get("https://sbis.ru/")
            print("Open 'https://sbis.ru/'")
            print("Step 1.OK")
            
            # Step 2
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Контакты"))).click()
            print("Clicked on 'Контакты'")
            print("Step 2.OK")

            # Step 3
            region_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sbis_ru-Region-Chooser__text")))
            print("Region:", region_element.text)
            print("Step 3.OK")

            # Step 4
            partner_blocks = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@tabindex]")))
            print("Блок'Партнеры' найден")
            print("Step 4.OK")
            
            # Step 5
            region_element.find_element(By.XPATH, "//*[contains(@class, 'sbis_ru-link')]").click()
            print("Выбор региона клик")
            print("Step 5.OK")

            # Step 6
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            print(current_date)
            input_name = "ws-input_" + current_date
            input_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, input_name)))
            input_element.clear()
            input_element.send_keys("Камчатский край") 
            print("Step 6.OK")

            # Step 7
            kamchatka_element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Камчатский край')]")))
            kamchatka_element.click()
            print("Clicked on 'Камчатский край'")
            print("Step 7.OK")
            time.sleep(2)

            # Step 8
            selected_region_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sbis_ru-Region-Chooser__text")))
            selected_region_text = selected_region_element.text
            print(selected_region_text)
            assert selected_region_text == "Камчатский край", "Selected region has not been substituted"

            partner_blocks_after_click = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@tabindex]")))
            assert len(partner_blocks_after_click) != len(partner_blocks), "List of partners has not changed"

            current_url = browser.current_url
            print(current_url)
            assert "kamchatskij-kraj" in current_url, "URL does not contain information of the selected region"
            current_title = browser.title
            assert "Камчатский край" in current_title, "Title does not contain information of the selected region"
            print("Step 8.OK")

   
        except NoSuchElementException as ex:
            pytest.fail("Element not found")
        except Exception as ex:
            pytest.fail("An error occurred")


# Run the test using pytest
if __name__ == "__main__":
    pytest.main(['-v', '-s', 'tensor2.py'])
