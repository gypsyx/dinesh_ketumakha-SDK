
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
        # TODO add validation for token and server_url
        self.token = token
        self.server_url = server_url

    # TODO - needs ability to page
    def get_movies(self) -> MovieListResponse:
        response = make_request(self.token, self.server_url, "movie")
        return deserialize_movies(response)

    def get_movie(self, movie_id: str) -> Union[Movie, None]:
        response = make_request(self.token, self.server_url, f"movie/{movie_id}")
        return deserialize_movie(response)

    # TODO - needs ability to page
    def get_quotes(self) -> QuoteListResponse:
        response = make_request(self.token, self.server_url, f"quote")
        return deserialize_quotes(response)

    def get_quotes_from_movie(self, movie_id: str) -> QuoteListResponse:
        response = make_request(self.token, self.server_url, f"movie/{movie_id}/quote")
        return deserialize_quotes(response)

    def get_quote(self, quote_id: str) -> Union[Quote, None]:
        response = make_request(self.token, self.server_url, f"quote/{quote_id}")
        return deserialize_quote(response)

def make_request(token, base_url, fragment):
    headers = {'Authorization': f'Bearer {token}'}
    url = urljoin(base_url, fragment)
    response = requests.get(url, headers=headers)
    # surface up the error to the consumer of our SDK. The deployed server api itself 
    # isn't detailed in this regard to supply more specific errors.
    response.raise_for_status()
    return response.json()