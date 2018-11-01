def toPersianDigit(number):
    persian_digit = u"۱۲۳۴۵۶۷۸۹۰"
    english_digit = u"1234567890"
    for i in range(len(persian_digit)):
        number = number.replace(english_digit[i], persian_digit[i])
    return number
