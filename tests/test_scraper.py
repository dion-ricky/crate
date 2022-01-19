import os
import json
import unittest
import hashlib

from crate import ScraperOptions, Scraper
from crate.driver import Driver, DriverOptions
from crate.utils import Tweet

class TestScraper(unittest.TestCase):
    
    def test_driver_get(self):
        do = DriverOptions()
        driver = Driver(do)

        driver.get("https://www.google.com")

        self.assertEqual(driver.driver.title, 'Google')

    def test_scraper_from_account(self):
        do = DriverOptions(
            headless=True
        )

        scraper = Scraper(do)
        
        # Scrape from bot account for testing
        so = ScraperOptions(
            from_account="whataweekhuh",
            since="2022-01-01",
            until="2022-01-07"
        )

        tweet = json.loads(repr(scraper.scrape(so)))[0]
        tweet = Tweet(**tweet)

        compare = Tweet(
            tweet_id="1478696530051678209",
            tweet_url="https://twitter.com/whataweekhuh/status/1478696530051678209",
            display_name="What a week, huh? all Wednesdays",
            username="@whataweekhuh",
            created_date="2022-01-05T11:55:00.000Z",
            text="",
            embedded="106\n15.1K\n69.4K",
            reply_count="106",
            retweet_count="15.1K",
            like_count="69.4K",
            emojis=[],
            image_links=["https://pbs.twimg.com/media/ErAWtcNXcAIoD3N?format=jpg&name=small"]
        )

        print(tweet)

        self.assertEqual(tweet.tweet_id, compare.tweet_id)
        self.assertEqual(tweet.tweet_url, compare.tweet_url)
        self.assertEqual(tweet.image_links, compare.image_links)
    
    def test_scraper_text(self):
        do = DriverOptions(
            headless=True
        )

        scraper = Scraper(do)

        # Scrape from bot account for testing
        so = ScraperOptions(
            from_account="year_progress",
            since="2022-01-04",
            until="2022-01-05"
        )

        tweet = json.loads(repr(scraper.scrape(so)))[0]
        tweet = Tweet(**tweet)

        compare = Tweet(
            tweet_id="1478395814053568512",
            tweet_url="https://twitter.com/year_progress/status/1478395814053568512",
            display_name="Year Progress",
            username="@year_progress",
            created_date="2022-01-04T16:00:03.000Z",
            text="░░░░░░░░░░░░░░░ 1%",
            embedded="░░░░░░░░░░░░░░░ 1%\n178\n5.7K\n36.4K",
            reply_count="178",
            retweet_count="5.7K",
            like_count="36.4K",
            emojis=[],
            image_links=[]
        )

        self.assertEqual(tweet.tweet_id, compare.tweet_id)
        self.assertEqual(tweet.tweet_url, compare.tweet_url)
        self.assertEqual(tweet.text, compare.text)
    
    def test_driver_path_options(self):
        current_path = os.path.dirname(os.path.realpath(__file__))

        do = DriverOptions(
            driver_path=os.path.join(current_path, 'driver/chromedriver'),
            headless=True
        )

        scraper = Scraper(do)
        
        # Scrape from bot account for testing
        so = ScraperOptions(
            from_account="whataweekhuh",
            since="2022-01-01",
            until="2022-01-07"
        )

        tweet = json.loads(repr(scraper.scrape(so)))[0]
        tweet = Tweet(**tweet)

        compare = Tweet(
            tweet_id="1478696530051678209",
            tweet_url="https://twitter.com/whataweekhuh/status/1478696530051678209",
            display_name="What a week, huh? all Wednesdays",
            username="@whataweekhuh",
            created_date="2022-01-05T11:55:00.000Z",
            text="",
            embedded="106\n15.1K\n69.4K",
            reply_count="106",
            retweet_count="15.1K",
            like_count="69.4K",
            emojis=[],
            image_links=["https://pbs.twimg.com/media/ErAWtcNXcAIoD3N?format=jpg&name=small"]
        )

        print(tweet)

        self.assertEqual(tweet.tweet_id, compare.tweet_id)
        self.assertEqual(tweet.tweet_url, compare.tweet_url)
        self.assertEqual(tweet.image_links, compare.image_links)