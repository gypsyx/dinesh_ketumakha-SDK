import pytest
from lotrpy.lotr import LOTR
from lotrpy.models import (
  Movie,
  MovieListResponse,
  Quote,
  QuoteListResponse
) 
from requests.exceptions import HTTPError

def test_get_movies(lotr_object):
    resp = lotr_object.get_movies()
    assert len(resp.movies) > 0
    assert isinstance(resp, MovieListResponse)


def test_get_movie(lotr_object):
    resp = lotr_object.get_movie("5cd95395de30eff6ebccde5d")
    # import pdb;pdb.set_trace()
    assert isinstance(resp, Movie)
    assert resp.name

    # negative test
    with pytest.raises(HTTPError):
        resp = lotr_object.get_movie("bad_id")

def test_get_quote(lotr_object):
    resp = lotr_object.get_quote("5cd96e05de30eff6ebccebcf")
    # import pdb;pdb.set_trace()
    assert isinstance(resp, Quote)
    assert resp.dialog

    # negative test
    with pytest.raises(HTTPError):
        resp = lotr_object.get_quote("bad_id")


def test_get_quotes_from_movie(lotr_object):
    resp = lotr_object.get_quotes_from_movie("5cd95395de30eff6ebccde5b")
    assert len(resp.quotes) > 0
    assert isinstance(resp, QuoteListResponse)

def test_get_quotes(lotr_object):
    resp = lotr_object.get_quotes()
    assert len(resp.quotes) > 1
    assert isinstance(resp, QuoteListResponse)




