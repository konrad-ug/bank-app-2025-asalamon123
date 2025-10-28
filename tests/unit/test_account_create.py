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
        account = Account("John", "Doe", "65010112345", "PROMO_ABC")  
        assert account.promo_code == "PROMO_ABC"
        assert account.balance == 50

    def test_promo_born_after_1960(self):
        # 1965-01-01
        account = Account("Jan", "Kowalski", "65010112345", "PROMO_ABC")
        assert account.balance == 50
    
    def test_no_promo_born_in_1960(self):
        # 1960-01-01
        account = Account("Ewa", "Nowak", "60010112345", "PROMO_ABC")
        assert account.balance == 0
    
    def test_no_promo_for_born_before_1960(self):
        # 1955-01-01 
        account = Account("Adam", "Nowak", "55010112345", "PROMO_ABC")
        assert account.balance == 0

    def test_promo_for_born_after_2000(self):
        # 2005-01-01 
        account = Account("Ola", "Zielińska", "05210112345", "PROMO_ABC")
        assert account.balance == 50

    def test_no_promo_if_pesel_invalid(self):
        account = Account("Piotr", "Nowak", "123", "PROMO_ABC")
        assert account.balance == 0
    
    def test_no_promo_if_code_not_start_with_PROMO(self):
        account = Account("Kasia", "Nowak", "65010112345", "DISCOUNT_50")
        assert account.balance == 0