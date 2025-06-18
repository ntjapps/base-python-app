import pytest
from unittest.mock import patch, MagicMock
import jobs.test_job as test_job

@patch('helpers.apiAuthInterface.requests.post')
def test_celery_test_api_task_success(mock_post):
    mock_token_response = MagicMock()
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {'access_token': 'test_token'}
    mock_api_response = MagicMock()
    mock_api_response.status_code = 200
    mock_api_response.json.return_value = {'ok': True}
    mock_post.side_effect = [mock_token_response, mock_api_response]

    result = test_job.celery_test_api_task()
    assert result['return']
    assert result['status_code'] == 200

@patch('helpers.apiAuthInterface.requests.post')
def test_celery_test_api_task_fail(mock_post):
    mock_token_response = MagicMock()
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {'access_token': 'test_token'}
    mock_api_response = MagicMock()
    mock_api_response.status_code = 400
    mock_api_response.text = 'fail'
    mock_post.side_effect = [mock_token_response, mock_api_response]

    with pytest.raises(Exception):
        test_job.celery_test_api_task()

def test_celery_test_task():
    result = test_job.celery_test_task()
    assert result['return']

def test_celery_test_body_task():
    result = test_job.celery_test_body_task('a', 'b', 'c')
    assert result['body'] == {'args1': 'a', 'args2': 'b', 'args3': 'c'}
