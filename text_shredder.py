import sys
import math

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    # create a dictionary with uppercase letter A-Z as the keys and their
    # respective counts as the values
    X = {chr(i): 0 for i in range(ord('A'), ord('Z')+1)}

    with open(filename, encoding='utf-8') as f:
        for line in f:
            for char in line:
                # only add to the count is an alphabet
                if char.upper() in X:
                    X[char.upper()] += 1
    return X

def main():
    # find the counts of each letter in the file
    letter_counts = shred('letter.txt')
    for letter, count in letter_counts.items():
        print(f"{letter} {count}")

    # get the probabilities for each letter
    e, s = get_parameter_vectors()

    # find X1 log e1 and X1 log s1
    # X1 is the count of the letter 'A'
    x1 = letter_counts['A']
    print(f"{x1 * math.log(e[0]):.4f}")
    print(f"{x1 * math.log(s[0]):.4f}")

    # find F(English)
    e_sum = 0
    # find the sum of the probabilities of each letter in English
    for i in range(26):
        e_sum += letter_counts[chr(ord('A') + i)] * math.log(e[i])
    f_english = math.log(0.6) + e_sum

    # find F(Spanish)
    s_sum = 0
    # find the sum of the probabilities of each letter in Spanish
    for i in range(26):
        s_sum += letter_counts[chr(ord('A') + i)] * math.log(s[i])
    f_spanish = math.log(0.4) + s_sum

    print(f"{f_english:.4f}")
    print(f"{f_spanish:.4f}")

    # find P(Y = English | X)
    diff = f_spanish - f_english
    if diff>= 100:
        probability = 0
    elif diff <= -100:
        probability = 1
    else:
        probability = 1 / (1 + math.exp(diff))

    print(f"{probability:.4f}")

if __name__ == "__main__":
    main()
