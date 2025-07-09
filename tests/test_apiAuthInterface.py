import pytest
from unittest.mock import patch, MagicMock
import helpers.apiAuthInterface as api


@patch('helpers.apiAuthInterface.requests.post')
def test_getAccessToken_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'access_token': 'token'}
    token = api.getAccessToken()
    assert token == 'token'


@patch('helpers.apiAuthInterface.requests.post')
def test_getAccessToken_failure(mock_post):
    mock_post.return_value.status_code = 400
    with pytest.raises(Exception):
        api.getAccessToken()


@patch('helpers.apiAuthInterface.getAccessToken', return_value='token')
@patch('helpers.apiAuthInterface.requests.post')
def test_postApiEndpoint(mock_post, mock_token):
    mock_post.return_value.status_code = 200
    resp = api.postApiEndpoint('/endpoint', data={'foo': 'bar'})
    assert resp == mock_post.return_value
