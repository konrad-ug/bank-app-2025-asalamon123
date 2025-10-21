class Account:
    def __init__(self, first_name, last_name, pesel, promo_code):
        self.first_name = first_name
        self.last_name = last_name
        if promo_code and promo_code.startswith("PROMO_"):
            self.balance = 50
        else: 
            self.balance = 0

        if len(pesel) == 11:
            self.pesel = pesel  
        else: 
            self.pesel = "Invalid"

        self.promo_code = promo_code