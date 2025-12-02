import pytest
import requests


@pytest.fixture
def account():
    return {
        "name": "John",
        "surname": "Doe",
        "pesel": "65010112345",
        "promo_code": "PROMO_ABC"
    }

URL = "http://127.0.0.1:5000/api/accounts"


class TestAccount:
    def test_create_account(self, account):
        response = requests.post(URL, json=account)

        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert data["message"] == "Account created"

        get_response = requests.get(f"{URL}/{account['pesel']}")
        assert get_response.status_code == 200

        account_data = get_response.json()
        assert account_data["name"] == account["name"]
        assert account_data["surname"] == account["surname"]
        assert account_data["pesel"] == account["pesel"]
        assert account_data["promo_code"] == account["promo_code"]
        assert account_data["balance"] == 50