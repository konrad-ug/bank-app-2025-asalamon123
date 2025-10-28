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
        elif 41 <= mm <= 52:
            century = 2100
        elif 61 <= mm <= 72:
            century = 2200
        elif 81 <= mm <= 92:
            century = 1800
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