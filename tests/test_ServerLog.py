import pytest
from unittest.mock import patch, MagicMock
from models.ServerLog import ServerLogModel, ServerLogSession


def test_ServerLogModel_fields():
    model = ServerLogModel()
    # Just check attributes exist
    for attr in ['id', 'message', 'channel', 'level', 'level_name', 'datetime', 'context', 'extra', 'created_at', 'updated_at']:
        assert hasattr(model, attr)


@patch('models.ServerLog.openConnection')
def test_ServerLogSession(mock_open):
    mock_db = MagicMock()
    mock_open.return_value = mock_db
    session = ServerLogSession()
    assert session is not None
