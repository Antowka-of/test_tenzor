import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time

class TestTensorWebsite:
    @pytest.fixture
    def browser(self, request):  
        driver = webdriver.Chrome()
        driver.maximize_window()
        request.addfinalizer(driver.quit)
        return driver

    def test_check_tensor_website(self, browser):
        try:
            # Step 1
            browser.get("https://sbis.ru/")
            # assert "Бизнес-платформа СБИС" in browser.title
            print("Step 1.OK")
            
            # Step 2
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Контакты"))).click()
            assert "Контакты" in browser.title
            print("Step 2.OK")
            
            # Step 3
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href,"tensor")]/img'))).click()
            print("Clicked on 'Тензор' banner")
            print("Step 3.OK")

            # Switch to the newly opened tab
            browser.switch_to.window(browser.window_handles[1])

            # Step 4
            block_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='container']/div[1]/div/div[5]/div/div/div[1]/div")))
            browser.execute_script("arguments[0].scrollIntoView(true);", block_element)
            print("Step 4.OK")
            
            # Step 5
            block_element.find_element(By.LINK_TEXT, "Подробнее").click()
            print("Clicked on 'Подробнее' hyperlink")
            print("Step 5.OK")
            
            # Step 6
            work_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='container']/div[1]/div/div[4]")))
            browser.execute_script("arguments[0].scrollIntoView(true);", work_element)
            print("Step 6.OK")

            # Step 7
            images = work_element.find_elements(By.TAG_NAME, "img")
            heights = [image.size["height"] for image in images]
            widths = [image.size["width"] for image in images]
            assert all(height == heights[0] for height in heights) and all(width == widths[0] for width in widths)
            print("Step 7.OK")

        except NoSuchElementException as ex:
            pytest.fail("Element not found")
        except Exception as ex:
            pytest.fail("An error occurred")


# Run the test using pytest
if __name__ == "__main__":
    pytest.main(['-v', '-s', 'tenzor1.py'])