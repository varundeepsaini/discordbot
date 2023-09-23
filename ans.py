def isPrime(num1):
    if num1 <= 1:
        return False
    if num1 <= 3:
        return True
    if num1 % 2 == 0 or num1 % 3 == 0:
        return False
    temp = 5
    while temp * temp <= num1:
        if num1 % temp == 0 or num1 % (temp + 2) == 0:
            return False
        temp = temp + 6
    return True


t = int(input())
for _  in range(t):
    n = int(input())

    if isPrime(n):
        print("Prime")
    else:
        print("Not Prime")
