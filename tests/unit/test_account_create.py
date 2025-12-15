import pytest
from src.account import Account
from src.account import AccountRegistry

@pytest.fixture
def acc():
    return Account("John", "Doe", "65010112345", "PROMO_ABC")

@pytest.fixture
def acc2():
    return Account("John", "Doe", "65010112345", None)


@pytest.fixture
def registry():
    return AccountRegistry()


class TestAccount:
    @pytest.mark.parametrize(
       "pesel, expected",
        [
            ("12345678912", "12345678912"),   # valid
            ("123", "Invalid"),               # short
            ("123456789123456789", "Invalid") # long
        ]
)

    def test_name_and_pesel_validation(self, pesel, expected):
        account = Account("John", "Doe", pesel, None)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == expected

    def test_account_creation_invalid_code(self):
        account = Account("John", "Doe", "123456789123456789", "wrong_code")
        assert account.promo_code == "wrong_code"
        assert account.balance == 0

    def test_account_creation_valid_code(self, acc):  
        assert acc.promo_code == "PROMO_ABC"
        assert acc.balance == 50

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

    def test_extract_year_value_error(self):
        account = Account("John", "Doe", "XX051231", "PROMO_ABC")
        assert account.extract_year_from_pesel() is None

    def test_extract_year_invalid_month(self):
        account = Account("John", "Doe", "99001312345", "PROMO_ABC")  # mm = 00
        assert account.extract_year_from_pesel() is None

    def test_extract_year_not_int_error(self):
        account = Account("John", "Doe", "65A10112345", "PROMO_ABC")
        assert account.extract_year_from_pesel() is None
        assert account.balance == 0

    def test_extract_year_2100_century(self):
        account = Account("John", "Doe", "41510112345", "PROMO_ABC")
        assert account.extract_year_from_pesel() == 2141
        assert account.balance == 50

    def test_extract_year_2200_century(self):
        account = Account("John", "Doe", "61710112345", "PROMO_ABC")
        assert account.extract_year_from_pesel() == 2261
        assert account.balance == 50

    def test_extract_year_1800_century(self):
        account = Account("John", "Doe", "81810112345", "PROMO_ABC")
        assert account.extract_year_from_pesel() == 1881
        assert account.balance == 0



class TestAccountTransfers:
    def test_recieve_transfer(self, acc2):
        result = acc2.recieve_transfer(100)
        assert result is True
        assert acc2.balance == 100

    def test_send_transfer(self, acc2):
        acc2.recieve_transfer(200)
        result = acc2.send_transfer(50)
        assert result is True
        assert acc2.balance == 150
    
    def test_send_fails_if_not_enough_balance(self, acc2): 
        result = acc2.send_transfer(50)
        assert result is False
        assert acc2.balance == 0 
    
    def test_receive_fails_if_negative_amount(self, acc2):
        result = acc2.recieve_transfer(-200)
        assert result is False
        assert acc2.balance == 0

    def test_send_fails_if_negative_amount(self, acc2):
        acc2.recieve_transfer(100)
        result = acc2.send_transfer(-20)
        assert result is False
        assert acc2.balance == 100

    def test_express_transfer_personal_account(self, acc2):
        acc2.recieve_transfer(100)
        result = acc2.send_express_transfer(100)
        assert result is True
        assert acc2.balance == -1

    def test_failed_express_transfer_personal_account(self, acc2):
        acc2.recieve_transfer(50)
        result = acc2.send_express_transfer(100)
        assert result is False
        assert acc2.balance == 50

class TestAccountHistory: 
    def test_history_receive_transfer(self, acc): 
        acc.recieve_transfer(500)
        assert acc.history == [500]

    def test_history_send_transfer(self, acc):
        acc.recieve_transfer(500)
        acc.send_transfer(200)
        assert acc.history == [500, -200]

    def test_history_express_transfer(self, acc):
        acc.recieve_transfer(500)
        acc.send_express_transfer(300)  
        assert acc.history == [500, -300, -1]

    def test_history_failed_send(self, acc):
        result = acc.send_transfer(100)
        assert result is False
        assert acc.history == []



class TestAccountLoan: 
    def test_loan_accepted(self, acc):
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        result = acc.submit_for_loan(100)
        assert result is True
        assert acc.balance == 650


    def test_loan_not_accepted_not_enough_transfers(self, acc):
        result = acc.submit_for_loan(100)
        assert result is False
        assert acc.balance == 50


    def test_loan_not_accepted_transfer_sum_bigger_than_amount(self, acc):
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        result = acc.submit_for_loan(1000)
        assert result is False
        assert acc.balance == 550


    def test_loan_not_accepted_sent_transfer(self, acc):
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.recieve_transfer(100)
        acc.send_transfer(100)
        result = acc.submit_for_loan(100)
        assert result is False

    def test_has_enough_history(self, acc):
        acc.history = [100, 100, 100, 100, 100]
        assert acc._has_enough_history(400) is True
        assert acc._has_enough_history(600) is False

    def test_recent_transfers_positive(self, acc):
        acc.history = [50, 50, 50]
        assert acc._recent_transfers_positive() is True
        acc.history = [50, -50, 50]
        assert acc._recent_transfers_positive() is False


class TestRegistry: 
    def test_create_empty_registry(self, registry):
        assert registry.accounts == []

    def test_add_to_registery(self, acc, registry):
        registry.add_account(acc)

        assert len(registry.accounts) == 1
        assert registry.accounts[0] is acc

    def test_search_by_pesel(self, registry, acc):
        registry.add_account(acc)
        other_acc = Account("John", "Doe", "65030112345", "PROMO_ABC")

        registry.add_account(other_acc)
        result = registry.search_by_pesel("65010112345")
        assert result == acc

    def test_fail_search_no_acc(self, registry):
        result = registry.search_by_pesel("65010112345")

        assert result is None

    def test_fail_wrong_pesel(self, registry, acc):
        registry.add_account(acc)
        other_acc = Account("John", "Doe", "65030112345", "PROMO_ABC")

        registry.add_account(other_acc)
        result = registry.search_by_pesel("123")
        assert result is None

    def test_return_all(self, registry, acc, acc2):
        registry.add_account(acc)
        registry.add_account(acc2)

        result = registry.return_all()

        assert result == [acc, acc2]

    def test_return_all_empty(self, registry, acc, acc2):
        result = registry.return_all()

        assert result == []

    def test_count(self, registry, acc, acc2):
        registry.add_account(acc)
        registry.add_account(acc2)

        result = registry.count_accounts()

        assert result == 2

    def test_count_empty(self, registry):
        result = registry.count_accounts()

        assert result == 0

    def test_exists(self, registry, acc):
        registry.add_account(acc)

        result = registry.exists(acc.pesel)

        assert result == True

    def test_not_exists(self, registry, acc):
        result = registry.exists(acc.pesel)

        assert result == False