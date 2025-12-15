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

        requests.delete(f"{URL}/{account['pesel']}")


    def test_account_already_exists_for_pesel(self, account):
        requests.post(URL, json=account)
        response = requests.post(URL, json=account)

        assert response.status_code == 409
        data = response.json()
        assert "message" in data
        assert data["message"] == "Account with given pesel already exists"

        requests.delete(f"{URL}/{account['pesel']}") 

    def test_get_account_not_found(self):
        response = requests.get(f"{URL}/00000000000")
        assert response.status_code == 404

    def test_update_account(self, account):
        response = requests.post(URL, json=account)
        assert response.status_code == 201

        updated_data = {
            "name": "Jane",
            "surname": "Smith",
            "promo_code": "PROMO_XYZ"
        }

        response = requests.patch(f"{URL}/{account['pesel']}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Account updated"

        get_response = requests.get(f"{URL}/{account['pesel']}")
        account_data = get_response.json()
        assert account_data["name"] == "Jane"
        assert account_data["surname"] == "Smith"
        assert account_data["promo_code"] == "PROMO_XYZ"

        
        requests.delete(f"{URL}/{account['pesel']}")

    def test_delete_account(self, account):
        response = requests.post(URL, json=account)
        assert response.status_code == 201

        del_response = requests.delete(f"{URL}/{account['pesel']}")
        assert del_response.status_code == 200
        data = del_response.json()
        assert data["message"] == "Account deleted"

        get_response = requests.get(f"{URL}/{account['pesel']}")
        assert get_response.status_code == 404