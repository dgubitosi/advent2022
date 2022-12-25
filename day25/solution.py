filename = 'input.txt'

_convert = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}
_snafu = dict([(v, k) for k, v in _convert.items()])

def snafu(n):
    # alter standard base 5
    # 4 = 4-5 = -1, with carry
    # 3 = 3-5 = -2, with carry
    # 2 = 2, no carry
    # 1 = 1, no carry
    # 0 = 0, no carry
    result = ''
    carry = 0
    while n:
        base5 = n % 5
        base5 += carry
        if base5 > 2:
            base5 -= 5
            carry = 1
        else:
            carry = 0
        digit = _snafu[base5]
        #print(f'base5="{base5}" digit="{digit}" carry="{carry}" result="{result}"')
        result = digit + result
        n //= 5
    return result

total = 0
with open(filename) as f:
    for line in f:
        line = list(line.strip())[::-1]
        for i, c in enumerate(line):
            total += _convert[c] * 5**i
print(total)
print(snafu(total))
