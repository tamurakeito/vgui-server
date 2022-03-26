# from asyncio.windows_events import NULL
import socket
# from socket import socket, AF_INET, SOCK_DGRAM

HOST = '127.0.0.1'   # juliusサーバーのIPアドレス
PORT = 10500         # juliusサーバーの待ち受けポート
DATESIZE = 1024     # 受信データバイト数

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

class Julius:

    def __init__(self):
        # juliusとのソケット接続
        self.sock = None

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
                    print(strTemp)
                    # 出力は"[s]五十七[/s]"の形
                    # 数字は+3
                    # lenは+7

                    msg = ''
                    CMD = 0
                    DIGIT = len(strTemp) - 7

                    #文字数１
                    if DIGIT == 1:
                        if strTemp[3] == '十':
                            CMD = 10
                            msg = str(CMD)
                        elif strTemp[3] == '百':
                            CMD = 100
                            msg = str(CMD)
                        else:
                            CMD = Num(strTemp[3])
                            msg = str(CMD)
                    #文字数２
                    elif DIGIT == 2:
                        if strTemp[3] == '十':
                            CMD = 10 + Num(strTemp[4])
                            msg = str(CMD)
                        elif strTemp[3] == '百':
                            CMD = 100 + Num(strTemp[4])
                            msg = str(CMD)
                        elif strTemp[4] == '十':
                            CMD = 10*Num(strTemp[3])
                            msg = str(CMD)
                        elif strTemp[4] == '百':
                            CMD = 100*Num(strTemp[3])
                            msg = str(CMD)
                    #文字数３
                    elif DIGIT == 3:
                        if strTemp[3] == '百':
                            if strTemp[4] == '十':
                                CMD = 110 + Num(strTemp[5])
                                msg = str(CMD)
                            else:
                                CMD = 100 + 10*Num(strTemp[4])
                                msg = str(CMD)
                        else:
                            if strTemp[4] == '十':
                                CMD = 10*Num(strTemp[3]) + Num(strTemp[5])
                                msg = str(CMD)
                            if strTemp[4] == '百':
                                CMD = 100*Num(strTemp[3]) + Num(strTemp[5])
                                msg = str(CMD)
                    #文字数４
                    elif DIGIT == 4:
                        if strTemp[3] == '百':
                            CMD = 100 + 10*Num(strTemp[4]) + Num(strTemp[6])
                            msg = str(CMD)
                        else:
                            if strTemp[5] == '十':
                                CMD = 100*Num(strTemp[3]) + 10 + Num(strTemp[6])
                                msg = str(CMD)
                            else:
                                CMD = 100*Num(strTemp[3]) + 10*Num(strTemp[5])
                                msg = str(CMD)
                    #文字数５
                    elif DIGIT == 5:
                        CMD = 100*Num(strTemp[3]) + 10*Num(strTemp[5]) + Num(strTemp[7])
                        msg = str(CMD)

                    #VISUAL
                    elif DIGIT == 6:
                        msg = 'visual'
                    #DEFAULT
                    elif DIGIT == 7:
                        msg = 'default'

                    # 送信
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(msg.encode(), ("127.0.0.1", 5000))
                    s.close()

                    fin_flag = False
                    strTemp = ""
                    CMD = 0

if __name__ == "__main__":
    julius = Julius()
    julius.run()
