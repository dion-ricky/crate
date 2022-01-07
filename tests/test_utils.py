import json
import unittest
from datetime import datetime

from crate.utils import safe_cast_to_datetime, coalesce, join_if_list, prepend, \
                        ScraperOptions, construct_url, Tweet

class TestUtils(unittest.TestCase):
    def test_safe_cast_datetime(self):
        in_str = "2022-01-01"
        in_dt = datetime(2022, 1, 1)
        compare = datetime(2022, 1, 1)
        
        self.assertEqual(safe_cast_to_datetime(in_str), compare)
        self.assertEqual(safe_cast_to_datetime(in_dt), compare)

    def test_coalesce(self):
        x = None
        y = 1

        self.assertEqual(coalesce(x, y), y)
    
    def test_join_if_list(self):
        l = ['#twitter', '#internet']
        s = '#twitter'

        self.assertEqual(join_if_list(l, ' OR '), '#twitter OR #internet')
        self.assertEqual(join_if_list(s, ' OR '), '#twitter')
    
    def test_prepend(self):
        h = 'twitter'
        l = ['twitter', 'internet']
        pre = '#'

        self.assertEqual(prepend(h, pre), '#twitter')
        self.assertEqual(prepend(l, pre), ['#twitter', '#internet'])
    
    def test_construct_url(self):
        scraper_options = ScraperOptions(
            words=['aplikasi', 'tokopedia'],
            words_any=['tokopedia', 'android', 'iphone', 'ios'],
            mention_account=['TokopediaCare', 'Tokopedia'],
            lang='id',
            filter_replies=True
        )

        compare = "https://twitter.com/search?q=aplikasi+tokopedia+%28tokopedia+OR+android+OR+iphone+OR+ios%29+%28%40TokopediaCare+OR+%40Tokopedia%29+lang%3Aid+-filter%3Areplies&src=typed_query&f=top"

        self.assertEqual(construct_url(scraper_options), compare)
    
    def test_construct_url_since_until(self):
        scraper_options = ScraperOptions(
            from_account='whataweekhuh',
            since="2022-01-01",
            until="2022-01-07"
        )

        compare = "https://twitter.com/search?q=%28from%3Awhataweekhuh%29+since%3A2022-01-01+until%3A2022-01-07&src=typed_query&f=top"

        self.assertEqual(construct_url(scraper_options), compare)
    
    def test_tweet_model(self):
        tweet = Tweet(
            '1478696530051678209',
            'https://twitter.com/whataweekhuh/status/1478696530051678209',
            'What a week, huh? all Wednesdays',
            '@whataweekhuh',
            '2022-01-05',
            '',
            '',
            0,
            14300,
            69400,
            [],
            []
        )

        compare = {
            'tweet_id': '1478696530051678209',
            'tweet_url': 'https://twitter.com/whataweekhuh/status/1478696530051678209',
            'display_name': 'What a week, huh? all Wednesdays',
            'username': '@whataweekhuh',
            'created_date': '2022-01-05',
            'text': '',
            'embedded': '',
            'reply_count': 0,
            'retweet_count': 14300,
            'like_count': 69400,
            'emojis': [],
            'image_links': []
        }

        self.assertEqual(json.loads(repr(tweet)), compare)