import pytest
from unittest.mock import patch, MagicMock
import jobs.test_job as test_job

@patch('jobs.test_job.postApiEndpoint')
def test_test_api_task_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'ok': True}
    result = test_job.test_api_task.run()
    assert result['return']
    assert result['status_code'] == 200

@patch('jobs.test_job.postApiEndpoint')
def test_test_api_task_fail(mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = 'fail'
    with pytest.raises(Exception):
        test_job.test_api_task.run()

def test_test_task():
    result = test_job.test_task.run()
    assert result['return']

def test_test_body_task():
    result = test_job.test_body_task.run('a', 'b', 'c')
    assert result['body'] == {'args1': 'a', 'args2': 'b', 'args3': 'c'}
