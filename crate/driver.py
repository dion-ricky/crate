from typing import Any, Optional, Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller


class DriverOptions:
    def __init__(
        self,
        headless: Optional[bool]=True,
        proxy: Optional[str]=None,
        show_images: Optional[bool]=False,
        option: Optional[str]=None):
        self._options = locals()
    
    def __getattribute__(self, __name: str) -> Any:
        if __name in object.__getattribute__(self, '_options'):
            return object.__getattribute__(self, '_options').get(__name)
        else:
            return object.__getattribute__(self, __name)


class Driver:

    def __init__(
        self,
        options: Optional[DriverOptions]) -> None:
        chromedriver_path = chromedriver_autoinstaller.install()

        driver_options = Options()
        driver_options.add_argument("log-level=3")

        driver_options.headless = options.headless

        # https://github.com/Altimis/Scweet/
        if options.headless:
            driver_options.add_argument("--disable-gpu")
        
        if options.proxy:
            driver_options.add_argument(f"--proxy-server={options.proxy}")
        
        if options.show_images:
            prefs = {"profile.managed_default_content_settings.images": 2}
            driver_options.add_experimental_option("prefs", prefs)
        
        if options.option:
            driver_options.add_argument(options.option)

        self.driver = webdriver.Chrome(
                            executable_path=chromedriver_path,
                            options=driver_options)
    
    def get(self, url: str):
        self.driver.get(url)

    def scroll(self) -> int:
        """Scroll window using javascript

        Returns current window Y position after scrolling"""

        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        
        return self.driver.execute_script("return window.pageYOffset;")

    def find_element(
        self,
        by: Union[By, str],
        value: Optional[str]) -> Optional[Any]:
        return self.driver.find_element(self.__by_pair(by), value)
    
    def find_elements(
        self,
        by: Union[By, str],
        value: Optional[str]) -> Optional[Any]:
        return self.driver.find_elements(self.__by_pair(by), value)

    def __by_pair(self, by):
        pair = {
            "id": By.ID,
            "xpath": By.XPATH,
            "link text": By.LINK_TEXT,
            "partial link text": By.PARTIAL_LINK_TEXT,
            "name": By.NAME,
            "tag name": By.TAG_NAME,
            "class name": By.CLASS_NAME,
            "css selector": By.CSS_SELECTOR
        }

        return pair[by]