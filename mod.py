def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def check(num):
    print('checking: ', num, ' ', end='')
    
    cs = luhn_checksum(num)
    if cs == 0:
        print('OK')
    else:
        print('FAIL')

if __name__ == '__main__':
    check('5224690000000009')
    check('4111110595736880')
    check('5189820000009996')
    check('5413339000001000')
    check('5224690000000009')
