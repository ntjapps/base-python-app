import pytest
from unittest.mock import patch, MagicMock
import helpers.imapInterface as imap


@patch('helpers.imapInterface.imaplib.IMAP4_SSL')
@patch('helpers.imapInterface.os.environ.get')
def test_openConnection_success(mock_env, mock_imap):
    mock_env.side_effect = lambda k, d=None: 'test' if 'PORT' not in k else '993'
    mock_mail = MagicMock()
    mock_imap.return_value = mock_mail
    mail = imap.openConnection()
    assert mail == mock_mail


@patch('helpers.imapInterface.imaplib.IMAP4_SSL')
def test_openConnection_failure(mock_imap):
    mock_imap.side_effect = Exception('fail')
    assert imap.openConnection() is None


@patch('helpers.imapInterface.os.environ.get')
def test_closeConnection_success(mock_env):
    mail = MagicMock()
    imap.closeConnection(mail)
    mail.close.assert_called_once()
    mail.logout.assert_called_once()
