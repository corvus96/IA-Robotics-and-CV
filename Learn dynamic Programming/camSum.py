import timeit

def canSum(targetSum, numbers, memo={}):
    ''' Inputs:
    targetSum: is an integer non negative
    numbers: is an array of numbers
    Output: if you can generate targetSum with
    array elements return true, but if you can't return false
    Time complexity = O(n*m) when n = array length and m = target sum 
    Space complexity = O(m)  
    '''
    if(targetSum in memo): return memo[targetSum]
    if(targetSum == 0): return True
    if(targetSum < 0): return False
    for num in numbers:
        remainder = targetSum - num
        if(canSum(remainder, numbers, memo)): 
            memo[targetSum] = True
            return True
    memo[targetSum] = False
    return False

# Test cases
def test():
    canSum(7, [2, 6])
    canSum(8, [2, 1, 5, 7])
    canSum(5000, [6, 3, 9, 23])

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("test()", setup="from __main__ import test"))