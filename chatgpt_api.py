import openai
import os

class ChatGPT:
    def __init__(self, api_key, proxy):
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy
        openai.api_key = api_key
        self.messages = [{"role": "system", "content": "你现在是很有用的助手！"}]

    def generate_answer(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.7
        )
        res_msg = response.choices[0].message
        # ChatGPT_Answer = response['choices'][0].text.strio()
        return res_msg["content"].strip()

    def chat(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = self.generate_answer()
        self.messages.append({"role": "assistant", "content": response})
        return response


# if __name__ == '__main__':
#     chatGPT = ChatGPT()
#     prompt = input("Q:")
#     while True:
#         prompt = input("Q:")
#         print(chatGPT.chat(prompt))
