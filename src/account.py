class Account:
    def __init__(self, first_name, last_name, pesel, promo_code):
        self.first_name = first_name
        self.last_name = last_name


        if len(pesel) == 11:
            self.pesel = pesel  
        else: 
            self.pesel = "Invalid"

        self.promo_code = promo_code

        if self.can_get_promo():
            self.balance = 50
        else:
            self.balance = 0

        self.history = []


    def extract_year_from_pesel(self):
        if self.pesel == "Invalid":
            return None
        try:
            yy = int(self.pesel[0:2])
            mm = int(self.pesel[2:4])
        except ValueError:
            return None


        if 1 <= mm <= 12:
            century = 1900
        elif 21 <= mm <= 32:
            century = 2000
            mm -= 20
        elif 41 <= mm <= 52:
            century = 2100
            mm -= 40
        elif 61 <= mm <= 72:
            century = 2200
            mm -= 60
        elif 81 <= mm <= 92:
            century = 1800
            mm -= 80
        else:
            return None

        return century + yy



    def can_get_promo(self):
        if not (self.promo_code and self.promo_code.startswith("PROMO_")):
            return False

        birth_year = self.extract_year_from_pesel()
        if birth_year is None:
            return False

        return birth_year > 1960

    def send_transfer(self, amount): 
        if amount <= 0: 
            return False
        if self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)
            return True
        
        return False

    def recieve_transfer(self, amount): 
        if amount <= 0: 
            return False
        
        self.balance += amount
        self.history.append(amount)
        return True

    def send_express_transfer(self, amount):
        fee = 1
        total = amount + fee
        if (self.balance + fee) >= total:
            self.balance -= total
            self.history.append(-amount)
            self.history.append(-fee)
            return True
        return False


    def _has_enough_history(self, amount):
        return len(self.history) >= 5 and sum(self.history[-5:]) >= amount
    
    def _recent_transfers_positive(self):
        return all(t > 0 for t in self.history[-3:])
    
    def submit_for_loan(self, amount): 
        if self._has_enough_history(amount) and self._recent_transfers_positive():
            self.balance += amount
            return True

        return False 



class BusinessAccount(Account):
    def __init__(self, company_name, nip): 
        self.company_name = company_name

        if len(nip) == 10 and nip.isdigit(): 
            self.nip = nip
        else: 
            self.nip = "Invalid"

        self.balance = 0
        self.history = []

    def send_express_transfer(self, amount):
        fee = 5
        total = amount + fee
        if (self.balance + fee) >= total:
            self.balance -= total
            return True
        return False

    def _has_enough_balance(self, amount):
        return self.balance >= 2 * amount

    def _has_correct_history(self): 
        return -1775 in self.history

    def take_loan(self, amount): 
        if self._has_enough_balance(amount) and self._has_correct_history():
            self.balance += amount
            return True

        return False 



class AccountRegistry: 
    def __init__(self): 
        self.accounts = []

    def add_account(self, account: Account):
        self.accounts.append(account)

    def search_by_pesel(self, pesel):
        for acc in self.accounts:
            if acc.pesel == pesel:
                return acc
        return None
        