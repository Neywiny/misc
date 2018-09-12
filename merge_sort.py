from time import time
from random import randint
from multiprocessing.pool import ThreadPool
pool = ThreadPool()
def merge(left, right):
    result = []
    i ,j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergesort(list,t=0):
    if len(list) < 2:
        return list
    middle = len(list) / 2
##    left = mergesort(list[:middle])
##    right = mergesort(list[middle:])
    async_result_l = pool.apply_async(mergesort,(list[:middle],0))
    async_result_r = pool.apply_async(mergesort,(list[middle:],0))
    left = async_result_l.get()
    right = async_result_r.get()
    return merge(left, right)
if __name__ == '__main__':
    l = [randint(1,100) for i in xrange(64)]
    t1 = time()
    mergesort(l)
    t2 = time()
    print t2-t1
