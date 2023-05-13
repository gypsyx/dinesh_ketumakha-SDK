
import requests

from typing import NamedTuple, List, Union
from urllib.parse import urljoin
from lotrpy.serializers import (
    deserialize_movies, 
    deserialize_movie, 
    deserialize_quote,
    deserialize_quotes
)
from lotrpy.models import (
    Movie,
    MovieListResponse,
    Quote,
    QuoteListResponse
)

class LOTRException(Exception):
    pass

class LOTR():
    def __init__(self, token, server_url):
        if not token or not server_url:
            raise LOTRException("token and server_url required")
        self.token = token
        self.server_url = server_url


    def get_movies(self, **kwargs: dict) -> MovieListResponse:
        response = make_request(self.token, self.server_url, "movie", **kwargs)
        return deserialize_movies(response)

    def get_movie(self, movie_id: str) -> Union[Movie, None]:
        response = make_request(self.token, self.server_url, f"movie/{movie_id}")
        return deserialize_movie(response)


    def get_quotes(self, **kwargs: dict) -> QuoteListResponse:
        response = make_request(self.token, self.server_url, f"quote", **kwargs)
        return deserialize_quotes(response)

    def get_quotes_from_movie(self, movie_id: str, **kwargs: dict) -> QuoteListResponse:
        response = make_request(self.token, self.server_url, f"movie/{movie_id}/quote")
        return deserialize_quotes(response)

    def get_quote(self, quote_id: str) -> Union[Quote, None]:
        response = make_request(self.token, self.server_url, f"quote/{quote_id}")
        return deserialize_quote(response)

def make_request(token, base_url, fragment, **kwargs):
    headers = {'Authorization': f'Bearer {token}'}
    url = urljoin(base_url, fragment)

    params = {}
    if "page" in kwargs:
        params["page"] = kwargs["page"]
    
    if "limit" in kwargs:
        params["limit"] = kwargs["limit"]

    if "offset" in kwargs:
        params["offset"] = kwargs["offset"]

    if params:
        response = requests.get(url, headers=headers, params=params)
    else:
        response = requests.get(url, headers=headers)
    # surface up the error to the consumer of our SDK. The deployed server api itself 
    # isn't detailed in this regard to supply more specific errors.
    response.raise_for_status()
    return response.json()