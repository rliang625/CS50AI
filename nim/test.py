a = dict()
a[(1,2,3),(1,2)] = 1
a[(1,2,3),(3,1)] = 0
for b in a:
    if (1,2,3) in a[b]:
        print (True)
    else:
        print (False)