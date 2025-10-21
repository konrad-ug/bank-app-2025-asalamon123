from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678912", None)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678912"

    def test_account_creation_short_pesel(self):
        account = Account("John", "Doe", "123", None)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "Invalid"

    def test_account_creation_long_pesel(self): 
        account = Account("John", "Doe", "123456789123456789", None)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "Invalid"

    def test_account_creation_invalid_code(self):
        account = Account("John", "Doe", "123456789123456789", "wrong_code")
        assert account.promo_code == "wrong_code"
        assert account.balance == 0

    def test_account_creation_valid_code(self):
        account = Account("John", "Doe", "123456789123456789", "PROMO_ABC")
        assert account.promo_code == "PROMO_ABC"
        assert account.balance == 50