import json
from typing import Any, Union, Optional, List
from datetime import datetime
from urllib.parse import urlparse, urlencode, quote_plus, urlunparse

from .const import TWITTER_SEARCH_URL


class TweetDisplayType:
    TOP = "Top"
    LATEST = "Latest"
    IMAGE = "Image"

    def validate(t: str) -> bool:
        allowed_type = ["Top", "Latest", "Image"]
        return t in allowed_type


DisplayTypeQuery = {
    TweetDisplayType.TOP: "top",
    TweetDisplayType.LATEST: "live",
    TweetDisplayType.IMAGE: "image" 
}


class ScraperOptions:
    def __init__(
        self,
        words: Optional[Union[str, List[str]]] = None,
        words_any: Optional[Union[str, List[str]]] = None,
        hashtag: Optional[str] = None,
        since: Optional[Union[datetime, str]] = None,
        until: Optional[Union[datetime, str]] = None,
        to_account: Optional[str] = None,
        from_account: Optional[str] = None,
        mention_account: Optional[Union[str, List[str]]] = None,
        lang: Optional[str] = None,
        display_type: \
            Optional[Union[TweetDisplayType, str]] = TweetDisplayType.TOP,
        filter_replies: Optional[bool] = False,
        min_replies: Optional[int] = None,
        min_likes: Optional[int] = None,
        min_retweets: Optional[int] = None,
        geocode: Optional[str] = None,
        limit: Optional[int] = float("inf"),
        proximity: Optional[bool] = False):

        try:
            assert TweetDisplayType.validate(display_type)
        except:
            raise Exception(f"\'{display_type}\'" + \
                " is not recognized as valid TweetDisplayType")

        self._options = {
            "words": words,
            "words_any": words_any,
            "hashtag": hashtag,
            "since": safe_cast_to_datetime(since),
            "until": safe_cast_to_datetime(until),
            "to_account": to_account,
            "from_account": from_account,
            "mention_account": mention_account,
            "lang": lang,
            "display_type": display_type,
            "filter_replies": filter_replies,
            "min_replies": min_replies,
            "min_likes": min_likes,
            "min_retweets": min_retweets,
            "geocode": geocode,
            "limit": limit,
            "proximity": proximity
        }
    
    def __getattribute__(self, __name: str) -> Any:
        if __name in object.__getattribute__(self, '_options'):
            return object.__getattribute__(self, '_options').get(__name)
        else:
            return object.__getattribute__(self, __name)


def safe_cast_to_datetime(dt: Union[datetime, str]) -> datetime:
    return datetime.strptime(dt, "%Y-%m-%d") if type(dt) == str else dt

def coalesce(*args) -> Optional[Any]:
    """Returns the first non-null value"""
    for i in args:
        if i:
            return i
    
    return None

def join_if_list(x: Union[str, List[str]], sep: str) -> str:
    if type(x) == list:
        return f"{sep}".join(x)
    else:
        return x

def prepend(
    x: Union[str, List[str]],
    pre: str) -> Union[str, List[str]]:
    if type(x) == list:
        return [f"{pre}{i}" for i in x]
    else:
        return f"{pre}{x}"

def try_except_default(to_try, exception, default_value):
    try:
        return to_try()
    except exception:
        return default_value

def construct_url(options: ScraperOptions):
    url = urlparse(TWITTER_SEARCH_URL)
    
    # Construct search query from ScraperOptions
    search_query = [
        join_if_list(options.words, " ") if options.words else "",

        # Words any
        "({})".format(
            join_if_list(options.words_any, " OR ")) if options.words_any \
                else ""

        # Hashtag
        # Input: ['ai', 'ml']
        # Output: (#ai OR #ml)
        "({})".format(
            join_if_list(prepend(options.hashtag, "#"), " OR ")) \
            if options.hashtag else "",
        
        "(from:{})".format(options.from_account) if options.from_account \
            else "",
        "(to:{})".format(options.to_account) if options.to_account \
            else "",
        
        # Mention account
        # Input: ['elonmusk', 'billgates']
        # Output: (@elonmusk OR @billgates)
        "({})".format(
            join_if_list(prepend(options.mention_account, "@"), " OR ")) \
            if options.mention_account else "",
        
        "lang:{}".format(options.lang) if options.lang else "",
        "since:{}".format(datetime.strftime(options.since, "%Y-%m-%d")) \
                    if options.since else "",
        "until:{}".format(datetime.strftime(options.until, "%Y-%m-%d")) \
                    if options.until else "",
        "min_replies:{}".format(options.min_replies) \
            if options.min_replies else "",
        "min_likes:{}".format(options.min_likes) \
            if options.min_likes else "",
        "min_retweets:{}".format(options.min_retweets) \
            if options.min_retweets else "",
        "geocode:{}".format(options.geocode) if options.geocode else "",
        "-filter:replies" if options.filter_replies else ""
    ]
    search_query = " ".join(search_query)
    search_query = " ".join(search_query.split())

    query = {
        "q": search_query,
        "src": "typed_query",
        "f": DisplayTypeQuery[options.display_type],
    }

    if options.proximity:
        query["lf"] = "on"
    
    query = urlencode(query, quote_via=quote_plus)
    url = url._replace(query=query)

    return urlunparse(url)

class Tweet:
    def __init__(
        self,
        tweet_id: str,
        tweet_url: str,
        display_name: str,
        username: str,
        created_date: Union[str, datetime],
        text: str,
        embedded: str,
        reply_count: int,
        retweet_count: int,
        like_count: int,
        emojis: List[str],
        image_links: List[str]) -> None:
        self._data = {
            "tweet_id": tweet_id,
            "tweet_url": tweet_url,
            "display_name": display_name,
            "username": username,
            "created_date": created_date,
            "text": text,
            "embedded": embedded,
            "reply_count": reply_count,
            "retweet_count": retweet_count,
            "like_count": like_count,
            "emojis": emojis,
            "image_links": image_links
        }
    
    def __getattribute__(self, __name: str) -> Any:
        if __name in object.__getattribute__(self, '_data'):
            return object.__getattribute__(self, '_data').get(__name)
        else:
            return object.__getattribute__(self, __name)
    
    def _is_valid_operand(self, other: object) -> bool:
        return hasattr(other, "tweet_id")
    
    def __repr__(self) -> str:
        return json.dumps(self._data)

    def __eq__(self, __o: object) -> bool:
        if not self._is_valid_operand(__o):
            return NotImplemented
        return self.tweet_id == __o.tweet_id