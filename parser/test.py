import nltk

a = "hello, my name is bob "
b = nltk.tokenize.wordpunct_tokenize(a)
for word in b:
    if any(char.isalpha() for char in word):
        print(word)