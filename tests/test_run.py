import pytest
from unittest.mock import patch, MagicMock
import run

def test_runScripts():
    with patch('run.celery.send_task') as mock_send_task, \
         patch('run.laravel_log_payload', return_value={'foo': 'bar'}):
        run.runScripts()
        mock_send_task.assert_called()
