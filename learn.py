"""""
class Solution(object):
    def __init__(self, numRows):
        output = []
        current = []
        if numRows == 1:
            return(output.append([1]))
        else:
            for num in range(numRows):
                if num == 0:
                    output.append([1])
                elif num == 1:
                    output.append([1,1])
                else:
                    for i in range(num):
                        if i == 0:
                            current.append(1)
                        elif i == num:
                             current.append(1)
                        else:
                            current.append((output[-1][i-1])+(output[-1][i+1]))
                    output.append(current)
                    current.clear()
        print(output)

p1 = Solution(1)
"""
class Solution:
    def __init__(self, numRows):
        output = []
        
        if numRows == 1:
            output.append([1])
        else:
            for num in range(numRows):
                current = []
                for i in range(num + 1):
                    if i == 0 or i == num:
                        current.append(1)
                    else:
                        current.append(output[-1][i-1] + output[-1][i])
                output.append(current)
        
        print(output)

# Example usage:
p1 = Solution(1)  # Output: [[1]]
p2 = Solution(5)  # Output: [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
