import random
from tqdm import tqdm

totalCount = 0
iters = 100000
for i in tqdm(range(iters)):
    square = 1
    while square != 3:
        if square == 1:
            if random.randrange(1, 7) < 5:
                square = 2
        elif square == 2:
            if random.randrange(1,3) == 1:
                square = 3
            else:
                square = 1
        totalCount += 1
print(totalCount / iters)
input()
