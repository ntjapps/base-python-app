import pytest
from helpers.laravelDbLoggerInterface import laravel_log_payload
from unittest.mock import patch

def test_laravel_log_payload_basic():
    with patch('helpers.laravelDbLoggerInterface.uuid.uuid7', return_value='uuid'):
        payload = laravel_log_payload('msg', 'info', {'a': 1}, {'b': 2})
        assert payload['message'] == 'msg'
        assert payload['level'] == '200'
        assert payload['context'] == {'a': 1}
        assert payload['extra'] == {'b': 2}
        assert payload['id'] == 'uuid'

@patch('helpers.laravelDbLoggerInterface.uuid.uuid7', return_value='uuid')
def test_laravel_log_payload_defaults(mock_uuid):
    payload = laravel_log_payload('msg')
    assert payload['level'] == '200'
    assert payload['context'] == {}
    assert payload['extra'] == {}
