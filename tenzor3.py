import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os
import time

class TestDownloadPlugin:
    @pytest.fixture
    def browser(self):  
        download_directory = os.path.abspath('./Download')
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': download_directory, 
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': True
                 }
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        return driver
        

    def test_download_plugin(self, browser):
        download_directory = os.path.abspath('./Download')
        try:
            # Step 1
            browser.get("https://sbis.ru/")
            print("Open 'https://sbis.ru/'")
            print("Step 1.OK")

            # Step 2
            footer_element = browser.find_element(By.CLASS_NAME, "sbisru-Footer__container")
            browser.execute_script("arguments[0].scrollIntoView(true);", footer_element)
            print("Step 2. Footer element found")

            # Step 3: Click on "Скачать локальные версии"
            footer_element.find_element(By.LINK_TEXT, "Скачать локальные версии").click()
            print("Step 3. Clicked on 'Скачать локальные версии' link")
            time.sleep(2)

            # Step 4: Click on "СБИС Плагин"
            sbis_plugin_button = browser.find_element(By.XPATH, "//div[contains(@class, 'controls-TabButton__wrapper') and div[contains(@class, 'controls-TabButton__caption') and text()='СБИС Плагин']]")
            browser.execute_script("arguments[0].scrollIntoView();", sbis_plugin_button)
            WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "controls-tabButton__overlay")))
            browser.execute_script("arguments[0].click();", sbis_plugin_button)
            print("Step 4. Clicked on 'СБИС Плагин'")

            # Step 5: Find the element with text "Windows"
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'sbis_ru-DownloadNew-innerTabs__title') and text()='Windows']")))
            time.sleep(2)
            print("Step 5: Нашли элемент 'Windows'")

            # Step 6: Click on the word "Скачать"
            download_link = browser.find_element(By.LINK_TEXT, "Скачать (Exe 7.12 МБ)").click()
            print("Step 6. Скачали файл")
            time.sleep(5)
            
            # Step 7: Сравниваем размер файла
            downloaded_file_path = os.path.join(download_directory, "sbisplugin-setup-web.exe")
            file_size = os.path.getsize(downloaded_file_path)
            file_size_mb = file_size / (1024 * 1024)
            print(f"The size of the downloaded file is: {file_size_mb:.2f} MB")
            # Extract the size mentioned in the link text
            link_text = "Скачать (Exe 7.12 МБ)"
            size_text = link_text.split("(")[-1].split(" ")[1]
            size_from_link = float(size_text)
            print(f"Size mentioned in link text: {size_from_link} MB")
            if abs(size_from_link - file_size_mb) < 0.01:  # Allow a tolerance of 0.01 MB
                print("Step 7. Размер файла совпадает!")
            else:
                print("Step 7. File size does not match!")

        except NoSuchElementException as ex:
            pytest.fail("Element not found")
        except Exception as ex:
            pytest.fail("An error occurred")


# Run the test using pytest
if __name__ == "__main__":
    pytest.main(['-v', '-s', 'tenzor3.py'])