import phonenumbers

def check_number(phone_number):
    phone_number = phonenumbers.parse(phone_number, None)
    print(phonenumbers.is_valid_number(phone_number))
    return phonenumbers.is_valid_number(phone_number)
    