def Num(letter) -> int:
    if letter == '一':
        return 1
    if letter == '二':
        return 2
    if letter == '三':
        return 3
    if letter == '四':
        return 4
    if letter == '五':
        return 5
    if letter == '六':
        return 6
    if letter == '七':
        return 7
    if letter == '八':
        return 8
    if letter == '九':
        return 9
    if letter == '十':
        return 10 
    if letter == '百':
        return 100

def Change(strTemp) -> int:
    CMD = 0
    DIGIT = len(strTemp)
    
    #文字数１
    if DIGIT == 1:
        if strTemp[0] == '十':
            CMD = 10
        elif strTemp[0] == '百':
            CMD = 100
        else:
            CMD = Num(strTemp[0])
            #文字数２
    elif DIGIT == 2:
        if strTemp[0] == '十':
            CMD = 10 + Num(strTemp[1]) 
        elif strTemp[0] == '百':
            CMD = 100 + Num(strTemp[1])
        elif strTemp[1] == '十':
            CMD = 10*Num(strTemp[0]) 
        elif strTemp[1] == '百':
            CMD = 100*Num(strTemp[0])
    #文字数３
    elif DIGIT == 3:
        if strTemp[0] == '百':
            if strTemp[1] == '十':
                CMD = 110 + Num(strTemp[2])
            else:
                CMD = 100 + 10*Num(strTemp[1])
        else:
            if strTemp[1] == '十':
                CMD = 10*Num(strTemp[0]) + Num(strTemp[2])
            if strTemp[1] == '百':
                CMD = 100*Num(strTemp[0]) + Num(strTemp[2])      
    #文字数４
    elif DIGIT == 4:
        if strTemp[0] == '百':
            CMD = 100 + 10*Num(strTemp[1]) + Num(strTemp[3])
        else:
            if strTemp[2] == '十':
                CMD = 100*Num(strTemp[0]) + 10 + Num(strTemp[3])
            else:
                CMD = 100*Num(strTemp[0]) + 10*Num(strTemp[2])
    #文字数５
    elif DIGIT == 5:
        CMD = 100*Num(strTemp[0]) + 10*Num(strTemp[2]) + Num(strTemp[4])
    
    print(CMD)

Change('五十二')