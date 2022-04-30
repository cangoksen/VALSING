from ValsingLinks0 import ValsingLinks
from time import  time

### NAIVE TEST
A0 = [[1, 0, 0, 0],
     [0, 1, 1, 1]]

A = [[0, 0, 0, 1],
     [0, 1, 1, 1],
     [0, 1, 1, 0],
     [1, 0, 0, 1],
     [1, 1, 1, 1],
     [1, 0, 0, 0],
     [1, 1, 1, 0]]
'''
0001
1110

1001
0110

1000
0110
0001

1000
0111

1111

'''



C = list(reversed(A))

B = [[0, 0, 1, 1, 0, 0],
     [1, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 0],
     [1, 1, 1, 0, 0, 0],
     [0, 0, 0, 1, 1, 0],
     [0, 0, 0, 0, 1, 1],
     [1, 0, 1, 0, 1, 1]]

# B and D have 1 solution (not counting ordering)
D = list(reversed(B))

time_res = []
for i, problem in enumerate([A,B,C,D]):
    X = ValsingLinks(problem)

    start = time()
    for _ in range(10000): #10k
        X.solve()
        X.solutions = set()
    end = time()
    X.solve()
    print(len(X.solutions))
    print(X.solutions)
    time_res.append(end-start)

print()
for i, duration  in enumerate(time_res):
    print(i+1, ":\t",duration)
    print()
