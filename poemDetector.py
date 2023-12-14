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
                break

    if close == True:
        print("CLOSE TO A LIMERICK")
        return False

    print("NOT A LIMERICK")
    return False

def detectBallad(poem):
    if len(poem) % 4 != 0:
        print("NOT A BALLAD")
        return False
    
    correct_rs = [[1,2,3,2], [1,2,1,2]]
    print("HEREEE", correct_rs)
    rs = utils.word_rhyme(poem)
    print(f"Rhymescheme: {rs}")
    
    tol = len(poem) * 0.125
    for c in correct_rs:
        ballad = True
        close = True
        wrong = 0
        for i in range(len(rs)):
            if rs[i] != c[i % 4]:
                ballad = False
                break
        if ballad == True:
            print("IS A BALLAD")
            return True
        else:
            i = 0
            while i in range(len(rs) - 4):
                quartrain = [rs[i], rs[i+1], rs[i+2], rs[i+3]]
                if c == [1,2,3,2]:
                    if quartrain[1] == None or quartrain[3] == None:
                        quartrain[1] = 0
                        quartrain[3] = 0
                    if quartrain[1] != quartrain[3] or quartrain[0] == quartrain[2]:
                        print("a", i)
                        wrong += 1
                else:
                    if quartrain[0] == None or quartrain[2] == None:
                        quartrain[0] = 0
                        quartrain[2] = 0
                    if quartrain[1] == None or quartrain[3] == None:
                        quartrain[1] = 0
                        quartrain[3] = 0
                    if quartrain[0] != quartrain[2] or quartrain[1] != quartrain[3]:
                        print("b", i)
                        wrong += 1
                if wrong > tol:
                    close = False
                    break
                i += 4
            
            # for i in range(len(rs)):
            #     if rs[i] == None:
            #         rs[i] = 1
            #     if abs(rs[i] - c[i % 4]) > tol:
            #         print("yAaaaaaaaaaaa")
            #         close = False
            #         break
        if close == True:
            print("CLOSE TO A BALLAD", c)
            return False

    print("NOT A BALLAD")
    return False


def detectSonnet(poem):
    if len(poem) != 14:
        print("NOT A SONNET")
        return False
    
    shakespearean_rs = [1,2,1,2,3,4,3,4,5,6,5,6,7,7]
    petrarchan_rs = [[1,2,2,1,3,4,4,3,5,6,5,6,5,6],
                     [1,2,2,1,3,4,4,3,5,6,7,5,6,7]]
    rs = utils.word_rhyme(poem)
    print(f"Rhymescheme: {rs}")
    tol = 1
    close = True
    if rs == shakespearean_rs:
        print("IS A SHAKESPEAREAN SONNET")
        return True
    else:
        for i in range(len(rs)):
            if rs[i] == None:
                rs[i] = 0
            if abs(rs[i] - shakespearean_rs[i]) > tol:
                close == False
                break

    if close == True:
        print("CLOSE TO A SHAKESPEAREAN SONNET")
        return False
    
    close_1 = False
    for p_rs in petrarchan_rs:
        close = True
        if rs == p_rs:
            print("IS A PETRARCHAN SONNET")
            return True
        else:
            for i in range(len(rs)):
                if rs[i] == None:
                    rs[i] = 0
                if abs(rs[i] - p_rs[i]) > tol:
                    close == False
                    break
        if close:
            close_1 = True
    
    if close_1:
        print("CLOSE TO A PETRARCHAN SONNET")
        return False

    print("NOT A SONNET")
    return False


def detectVillanelle(poem):
    if len(poem) != 19:
        print("NOT A VILLANELLE")
        return False
    
    first = poem[0]
    third = poem[2]

    if first != poem[5] or first != poem[11] or first != poem[17]:
        print("NOT A VILLANELLE")
        return False
    if third != poem[8] or third != poem[14] or third != poem[18]:
        print("NOT A VILLANELLE")
        return False
    
    correct_rs = [1,2,1,1,2,1,1,2,1,1,2,1,1,2,1,1,2,1,1]
    rs = utils.word_rhyme(poem)
    print(f"Rhymescheme: {rs}")

    tol = 1
    close = True
    if rs == correct_rs:
        print("IS A VILLANELLE")
        return True
    else:
        for i in range(len(rs)):
            if rs[i] == None:
                rs[i] = 0
            if abs(rs[i] - correct_rs[i]) > tol:
                close == False
                break
    
    if close == True:
        print("CLOSE TO A VILLANELLE")
        return False
    print("IS NOT A VILLANELLE")
    return False
    
def detectBlankVerse(poem):
    meter = utils.meter_detector(poem)
    if meter != '':
        print("IS A BLANK VERSE")
        return True
    else:
        return False

def detectFreeVerse(poem):
    meter = utils.meter_detector(poem)
    if meter == '':
        print("IS A FREE VERSE")
        return True
    else:
        return False
