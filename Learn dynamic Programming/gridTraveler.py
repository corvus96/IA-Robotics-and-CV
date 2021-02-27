# This function calculate how many ways you can go from the 
# top left corner in a grid to the bottom 
# right corner, with only two movements [right, bottom] 
def gridTraveler(m, n, memo={}):
    '''Inputs: 
    m: are the rows of grid,
    n: are the column of grid,
    memo: is a dictionary that their keys are equal to "m,n" 
    an their values are equal to the correspond score, a score
    is equal to the number of ways from the actual position
    output: number of ways to go from top left corner 
    to bottom right corner in a grid
    Time complexity = O(n*m)
    Space complexity = O(n + m)                                   
    '''
    key = str(m) + ',' + str(n)
    if(key in memo): return memo[key]
    if(m == 1 and n == 1): return 1
    if(m == 0 or n == 0): return 0
    memo[key] = gridTraveler(m - 1, n, memo) + gridTraveler(m, n - 1, memo)
    return memo[key]

print(gridTraveler(2,3))

