import utils

def detectHaiku(poem):
    if len(poem) != 3:
        print("NOT A HAIKU")
        return False
    else: 
        sent_syllables = [0, 0, 0]
        for i in range(len(poem)):
            for word in poem[i].split():
                sent_syllables[i] += utils.count_syllables(word)
        print(f"Sent Syllables: {sent_syllables}")
        correct_syllables = [5, 7, 5]
        tol = 1
        if sent_syllables == correct_syllables:
            print("IS A HAIKU")
            return True
        else:
            for i in range(len(sent_syllables)):
                if abs(sent_syllables[i] - correct_syllables[i]) <= tol:
                    continue
                else:
                    print("NOT A HAKU")
                    return False
            print("CLOSE TO A HAIKU")
    return False
    
def detectLimerick(poem):
    if len(poem) != 5:
        print("NOT A LIMERICK")
        return False
    
    
    sent_syllables = [0, 0, 0, 0, 0]
    for i in range(len(poem)):
        for word in poem[i].split():
            sent_syllables[i] += utils.count_syllables(word)
    print(f"Sent Syllables: {sent_syllables}")
    

    part_1 = [0, 1, 4]
    part_2 = [2, 3]
    tol = 1.5
    # First two lines contain seven to ten syllables
    # Final line contains seven to ten syllables
    lim = [0, 0, 0, 0, 0]
    for num in part_1:
        if abs(sent_syllables[num] - 8.5) <= tol:
            continue
        elif abs(sent_syllables[num] - 8.5) <= tol + 1:
            print("CLOSE TO A LIMERICK, line: ", num+1)
            lim[num] = 1
        else:
            print("NOT A LIMERICK, line: ", num+1)
            return False

    # Third and fourth lines contain five to seven syllables
    tol = 1
    for num in part_2:
        if abs(sent_syllables[num] - 6) <= tol:
            continue
        elif abs(sent_syllables[num] - 6) <= tol + 1:
            print("CLOSE TO A LIMERICK, line: ", num+1)
            lim[num] = 1
        else:
            print("NOT A LIMERICK, line: ", num+1)
            return False
       

    close = False
    for num in lim:
        if num == 1:
            close = True

    # AABBA rhyme scheme
    correct_rs = [1,1,2,2,1]
    tol = 1
    manual = [2, 2, 1, 1, 0]
    rs = utils.word_rhyme(poem)
    print(f"Rhymescheme: {rs}")
    if rs == correct_rs and close == False:
       
        print("IS A LIMERICK")
        return True
    else:
        close = True
        for i in range(len(rs)):
            if rs[i] == None:
                rs[i] = 0
            if abs(rs[i] - correct_rs[i]) > tol:
                close == False


    if close == True:
        print("CLOSE TO A LIMERICK")
        return False

    print("NOT A LIMERICK")
    return False