#julius
import socket
import socketio
import time

HOST = '127.0.0.1'   # juliusサーバーのIPアドレス
PORT = 10500         # juliusサーバーの待ち受けポート
DATESIZE = 1024     # 受信データバイト数

sio = socketio.Client()

class Julius:

    def __init__(self):

        self.sock = None
        sio.connect('http://127.0.0.1:3001/')
        sio.wait()

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

    def run(self):

        # socket通信でjuliusサーバーに接続
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self.sock.connect((HOST, PORT))

            strTemp = "" # 話した言葉を格納する変数
            fin_flag = False # 話終わりフラグ

            while True:

                # juliusサーバからデータ受信
                data = self.sock.recv(DATESIZE).decode('utf-8')

                for line in data.split('\n'):
                    # 受信データから、<WORD>の後に書かれている言葉を抽出して変数に格納する。
                    # <WORD>の後に、話した言葉が記載されている。
                    index = line.find('WORD="')
                    if index != -1:
                        # strTempに話した言葉を格納
                        strTemp = strTemp + line[index+6:line.find('"',index+6)]

                    # 受信データに</RECOGOUT>'があれば、話終わり ⇒ フラグをTrue
                    if '</RECOGOUT>' in line:
                        fin_flag = True

                # 話した言葉毎に、print文を実行
                if fin_flag == True:
                    '''
                    if 'クリア' in strTemp:
                        searchbox_input('')
                    elif '検索' in strTemp:
                        search_button_click()
                    else:
                        searchbox_input('東北大学')
                    '''

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
                    
                    sio.emit('v-command', CMD)

                    fin_flag = False
                    strTemp = ""
                    CMD = 0


if __name__ == "__main__":

    julius = Julius()
    julius.run()

