import re
from time import sleep
from typing import Optional, List
from urllib.parse import urlsplit

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from .driver import Driver, DriverOptions
from .utils import ScraperOptions, Tweet, construct_url, \
                    try_except_default


class Scraper:
    def __init__(
        self,
        options: Optional[DriverOptions] = DriverOptions(),
        sleep_duration: int = 5) -> None:
        self.__driver = Driver(options)
        self.sleep_duration = sleep_duration

    def scrape(self, options: ScraperOptions):
        url = construct_url(options)

        self.__driver.get(url)

        tweets = []
        last_y = None
        current_y = None

        while len(tweets) < options.limit:
            current_y = self.__driver.scroll()
            
            if last_y == current_y:
                break
            
            last_y = current_y

            _tweets = self.__get_tweets()

            for _tweet in _tweets:
                if _tweet not in tweets:
                    tweets.append(_tweet)

        return tweets
    
    def __get_tweets(self) -> List[Tweet]:
        tweets = []
        
        # Wait for twitter to finish loading tweet
        sleep(self.sleep_duration)

        cards = self.__driver.find_elements(By.XPATH,
                                            '//article[@data-testid="tweet"]')
        
        for card in cards:
            tweets.append(self.__parse_tweet_from_card(card))
        
        return tweets
    
    def __parse_tweet_from_card(
        self,
        card: WebElement) -> Optional[dict]:
        # https://github.com/Altimis/Scweet/

        tweet_url_el = try_except_default(
            lambda: card.find_element(By.XPATH,
                './/a[contains(@href, "/status/")]'),
            NoSuchElementException, None
        )
        
        if not tweet_url_el:
            return

        tweet_url = tweet_url_el.get_attribute('href')
        tweet_id = urlsplit(tweet_url).path.split('/')[-1]

        promoted = try_except_default(
            lambda: card.find_element(By.XPATH,
                        './/div[2]/div[2]/[last()]//span').text == "Promoted",
            NoSuchElementException, False
        )

        if promoted:
            return

        display_name = try_except_default(
            lambda: card.find_element(By.XPATH, './/span').text,
            NoSuchElementException, None
        )

        username = try_except_default(
            lambda: card.find_element(By.XPATH,
                        './/span[contains(text(), "@")]').text,
            NoSuchElementException, None
        )

        created_date = try_except_default(
            lambda: card.find_element(By.XPATH, './/time') \
                        .get_attribute('datetime'),
            NoSuchElementException, None
        )

        if not display_name or not username or not created_date:
            return
        
        text = try_except_default(
            lambda: card.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[1]') \
                        .text,
            NoSuchElementException, ""
        )

        embedded = try_except_default(
            lambda: card.find_element(By.XPATH, './/div[2]/div[2]/div[2]').text,
            NoSuchElementException, ""
        )

        reply_count = try_except_default(
            lambda: card.find_element(By.XPATH,
                            './/div[@data-testid="reply"]').text,
            NoSuchElementException, 0
        )

        retweet_count = try_except_default(
            lambda: card.find_element(By.XPATH,
                            './/div[@data-testid="retweet"]').text,
            NoSuchElementException, 0
        )

        like_count = try_except_default(
            lambda: card.find_element(By.XPATH,
                            './/div[@data-testid="like"]').text,
            NoSuchElementException, 0
        )

        emoji_tags = try_except_default(
            lambda: card.find_elements(By.XPATH,
                            './/img[contains(@src, "emoji")]'),
            NoSuchElementException, []
        )

        emojis = []
        for tag in emoji_tags:
            try:
                filename = tag.get_attribute('src')
                emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename) \
                                .group(1), base=16))
            except AttributeError:
                continue
            
            if emoji:
                emojis.append(emoji)

        image_links = []

        try:
            elements = card.find_elements(By.XPATH,
                            './/div[2]/div[2]//img' + \
                            '[contains(@src, "https://pbs.twimg.com/")]')
            for element in elements:
                image_links.append(element.get_attribute('src'))
        except:
            image_links = []
        
        return Tweet(
            tweet_id,
            tweet_url,
            display_name,
            username,
            created_date,
            text,
            embedded,
            reply_count,
            retweet_count,
            like_count,
            emojis,
            image_links
        )