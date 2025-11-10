from src.account import BusinessAccount

class TestBusinessAccount: 
    def test_business_account_creation(self):
        account = BusinessAccount("MegaCorp", "1234567890")
        assert account.company_name == "MegaCorp"
        assert account.nip == "1234567890"
        assert account.balance == 0

    def test_invalid_nip(self):
        account = BusinessAccount("MegaCorp", "123")
        assert account.nip == "Invalid"



    
class TestBusinessAccountTransfers:
    def test_recieve_transfer_for_business_account(self):
        account = BusinessAccount("MegaCorp", "1234567890")
        result = account.recieve_transfer(100)
        assert result is True
        assert account.balance == 100

    def test_send_transfer_for_business_account(self):
        account = BusinessAccount("MegaCorp", "1234567890")
        account.recieve_transfer(200)
        result = account.send_transfer(50)
        assert result is True
        assert account.balance == 150

    def test_send_fails_if_not_enough_balance_for_business_account(self): 
        account = BusinessAccount("MegaCorp", "1234567890")
        result = account.send_transfer(50)
        assert result is False
        assert account.balance == 0

    def test_express_transfer_business_account(self):
        account = BusinessAccount("MegaCorp", "1234567890")
        account.recieve_transfer(100)
        result = account.send_express_transfer(100)
        assert result is True
        assert account.balance == -5

    def test_failed_express_transfer_business_account(self):
        account = BusinessAccount("MegaCorp", "1234567890")
        account.recieve_transfer(50)
        result = account.send_express_transfer(100)
        assert result is False
        assert account.balance == 50 