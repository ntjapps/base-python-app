import pytest
from unittest.mock import patch, MagicMock
import jobs.logger_job as logger_job

@patch('jobs.logger_job.ServerLogSession')
@patch('jobs.logger_job.insert')
@patch('jobs.logger_job.uuid.uuid7', return_value='uuid')
def test_log_db_task_dict(mock_uuid, mock_insert, mock_session):
    session = MagicMock()
    mock_session.return_value.__enter__.return_value = session
    payload = {'message': 'msg', 'channel': 'ch', 'level': '200', 'level_name': 'INFO', 'datetime': '2024-01-01', 'context': {}, 'extra': {}}
    result = logger_job.log_db_task.run(payload)
    assert result['return']
    session.execute.assert_called()
    session.commit.assert_called()

@patch('jobs.logger_job.ServerLogSession')
def test_log_db_task_none(mock_session):
    result = logger_job.log_db_task.run(None)
    assert result['return']
