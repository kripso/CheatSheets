import math
digits = int(math.log10(5**42))+1

for i in range(23):
    print(bin(5**i)[2:])

binnary = '1011111010111100001'
tmp = ''

for i in range(len(binnary)-1, -1, -1):
    tmp += binnary[i]

print(tmp, len(tmp))
1001000110000100111001110010101
1001000110000100111001110010101