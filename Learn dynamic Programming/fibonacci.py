# memoization
def fib(n, memo={}):
    '''Inputs: 
    n: is the fibonnaci number, for example;
    n = [1, 2, 3, 4, 5, 6]
    fib_sec = [1, 1, 2, 3, 5, 8]
    memo: is a dictionary that their keys are equal to n 
    an their values are equal to correspond value
    output: the correspond value to n-esimal fibonnaci number
    Time complexity = O(n)
    Space complexity = O(n)                                   
    '''
    if(n in memo): return memo[n]
    if(n <= 2): return 1
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

# Test case
print(fib(110))