import pytest
import requests
import time

@pytest.fixture
def account():
    return {
        "name": "John",
        "surname": "Doe",
        "pesel": "65010112345",
        "promo_code": "PROMO_ABC"
    }

URL = "http://127.0.0.1:5000/api/accounts"

class TestPerformance: 
    def test_performance_add_remove(self, account):
        for i in range(100):
            start = time.time()
            response = requests.post(URL, json=account, timeout=0.5)
            
            final_time = time.time() - start

            assert final_time < 0.5
            assert response.status_code == 201

            start2 = time.time()
            delete = requests.delete(f"{URL}/{account['pesel']}", timeout=0.5)

            final_time2 =  time.time() - start2

            assert final_time2 < 0.5 
            assert delete.status_code == 200 

    def test_performance_transfer(self, account):
        response = requests.post(URL, json=account)

        assert response.status_code == 201

        for i in range(100): 
            start = time.time()

            response = requests.post(
                f"{URL}/{account['pesel']}/transfer",
                json={"amount": 50, "type": "incoming"}, 
                timeout=0.5
            )

            final_time = time.time() - start

            assert final_time < 0.5
            assert response.status_code == 200

        get_response = requests.get(f"{URL}/{account['pesel']}")

        assert get_response.status_code == 200
        balance = get_response.json()["balance"]

        assert balance == 5050

        

        
