a = ['hello','good2bye','goodnight']
for word in a:
    for char in word:
        if char.isalpha():
            print (char)
        else:
            break
    print (word)