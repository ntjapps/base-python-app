import pytest
from unittest.mock import patch, MagicMock
import database.config as dbconfig


def test_openConnection_success():
    with patch('database.config.create_engine') as mock_engine:
        mock_engine.return_value = 'db'
        db = dbconfig.openConnection()
        assert db == 'db'


def test_openConnection_failure():
    with patch('database.config.create_engine', side_effect=Exception('fail')):
        with pytest.raises(SystemExit):
            dbconfig.openConnection()
