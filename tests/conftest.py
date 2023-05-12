import pytest
from lotrpy.lotr import LOTR

# This should be the testing token, so okay to have it here
TOKEN = "KkyexrFGQBW5wPJcNTKY"
SERVER_URL = "https://the-one-api.dev/v2/"

@pytest.fixture
def lotr_object():
    response = LOTR(token=TOKEN, server_url=SERVER_URL)
    return response