# coding=utf-8
# geekshang.top
from baidu_api import *
from chatgpt_api import *
from audioRecorder_api import *
import datetime
import sys


class Robot:
    def __init__(self):
        self.name = input("Please enter your alias: ")
        print("You could enter \'Bye\' or say it to quit the chat.")
        self.CU_ID = "12345" + self.name
        self.API_KEY = ""   # Baidu API key
        self.API_SECRET = ""    # Baidu API secret
        self.CHAT_KEY = ""  # ChatGPT Key
        self.PROXY = "http://localhost:"   # Proxy port
        self.CLI_Question = '\n{0}: '.format(self.name)
        self.CLI_Answer = '\nRobot: '

    def run(self):
        baiduConnection = BaiduConnection(self.CU_ID, self.API_KEY, self.API_SECRET)
        audioRecorder = AudioRecorder()
        chatGPT = ChatGPT(self.CHAT_KEY, self.PROXY)
        while True:
            print(self.CLI_Question)
            audioRecorder.record_by_control()
            ans = baiduConnection.audio2text()
            print(ans)
            if ans.find(u"再见") != -1:     # Say Bye
                aans = u"再见，祝你拥有美好的一天！"    # Chatbot answer to Bye
                baiduConnection.text2audio(aans)
                audioRecorder.play_wav()
                print(aans)
            aans = chatGPT.chat(ans)
            baiduConnection.text2audio(aans)
            audioRecorder.play_wav()
            print(aans)


if __name__ == "__main__":
    today = datetime.date.today()
    if today.year > 2023:   # Simple time limits
        sys.exit()
    robot = Robot()
    robot.run()
