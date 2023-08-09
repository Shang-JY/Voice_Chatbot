# -*- coding: utf-8 -*- #
import json
import base64
import requests


class BaiduConnection:
    def __init__(self, cu_id, api_key, api_secret):
        self.cu_id = cu_id
        self.API_KEY = api_key
        self.SECRET_KEY = api_secret
        self.ACCESS_TOKEN = self.get_access_token()

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        token = str(requests.post(url, params=params).json().get("access_token"))
        # todo try print("Baidu Connection Success")
        return token

    def audio2text(self, filename="upload_buffer.wav"):
        url = "https://vop.baidu.com/server_api"
        wav_fp = open(filename, 'rb')
        voice_data = wav_fp.read()
        LEN = len(voice_data)
        SPEECH = base64.b64encode(voice_data).decode('utf-8')

        # speech 可以通过 get_file_content_as_base64("C:\fakepath\test.m4a",False) 方法获取
        payload = json.dumps({
            "format": "pcm",
            "rate": 16000,
            "dev_pid": 1537,
            "channel": 1,
            "token": self.ACCESS_TOKEN,
            "cuid": self.cu_id,
            "len": LEN,
            "speech": SPEECH
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)

        return json.loads(response.text)['result'][0]

    def text2audio(self, text, filename="output_buffer.wav"):
        url = "https://tsn.baidu.com/text2audio"

        payload = 'tex={0}&tok={1}&cuid={2}&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=1&aue=6'.format(text,self.ACCESS_TOKEN,self.cu_id).encode("utf-8")
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        voice_data = response.content
        voice_fp = open(filename, 'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()


