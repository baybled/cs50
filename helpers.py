from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    # initilise set
    compared = {}
    
    # split data into lists, by newline character
    lista = a.split('\n')
    listb = b.split('\n')

    # compare lists, append to set if true
    for i in lista:
    	if i in listb:
    		compared.append(i)

    return compared


def sentences(a, b):
    """Return sentences in both a and b"""

    # initilise set
    compared = {}

    # separate each string in list called sentences

    lista = sent_tokenize(a)
    listb = sent_tokenize(b)

    # compare lists, append to set if true
    for i in lista:
    	if i in listb:
    		compared.append(i)

    return compared


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # initilise set and lists
    compared = {}

    lista = []
    listb = []

    # separate each string into substrings

    i = 0

    while i < len(a):
    	
    	# check if end of word is reached
    	if a[i + n] == None:
    		break

    	# store word in temp value
    	word = a[i:i+n]

    	# add to list
    	lista.append(word)

    	# move forward
    	i += 1

    j = 0 

    while j < len(b):

    	#check if end of word is reached
    	if a[j + n] == None:
    		break

    	# store word in temp value
    	word = b[j:j+n]

    	# add to list
    	listb.append(word)

    	# move forward
    	j += 1

    # compare lists, append to set if true
    for i in lista:
    	if i in listb:
    		compared.append(i)

    return compared