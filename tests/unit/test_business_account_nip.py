import pytest
from unittest.mock import patch
from src.account import BusinessAccount

@pytest.fixture
def acc():
    with patch("src.account.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        yield BusinessAccount("MegaCorp", "1234567890")

class TestBusinessNip:
    @patch("src.account.requests.get")
    def test_business_account_valid_nip(self, mock_get, acc):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny"
                }
            }
        }

        assert acc.nip == "1234567890"

    
    @patch("src.account.requests.get")
    def test_business_account_invalid_nip(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Zwolniony"
                }
            }
        }

        with pytest.raises(ValueError):
            BusinessAccount("Mafia", "8461627563")

