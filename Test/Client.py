# import os
# from openai import OpenAI
#
# # 构造 client
# client = OpenAI(
#     api_key='sk-u3LMNOLlKjtflTBan2daXvuc309dFO8IP51vro22vXLaAnUz', # 混元 APIKey
#     base_url="https://api.hunyuan.cloud.tencent.com/v1", # 混元 endpoint
# )
#
# question = input("输入你想问的问题：")
#
# # 自定义参数传参示例
# completion = client.chat.completions.create(
#     model="hunyuan-pro",
#     messages=[
#         {
#             "role": "user",
#             "content": question,
#         },
#     ],
# )
# print(completion.choices[0].message.content)

from openai import OpenAI
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from Email import tools
from zhipuai import ZhipuAI


class Client:

    def __init__(self, question):
        self.q = question

    # def __str__(self):
    #     if self.q:
    #         embedding_fun = SentenceTransformerEmbeddings(model_name="./text2vec-base-chinese")
    #         db = Chroma(persist_directory="D:/chroma_vector_data/", embedding_function=embedding_fun)
    #         doc = db.similarity_search(self.q)
    #         context = doc[0].page_content
    #         client = OpenAI(
    #             api_key='sk-u3LMNOLlKjtflTBan2daXvuc309dFO8IP51vro22vXLaAnUz',  # 混元 APIKey
    #             base_url="https://api.hunyuan.cloud.tencent.com/v1",  # 混元 endpoint
    #             # base_url='https://api.aihao123.cn/luomacode-api/open-api/v1',
    #             # api_key='sk-t1f6f5i2pp4lp3ir59hg5u7t3qoq6q97t4704iit02n437ad',
    #         )
    #         prompt = "对于以下的问题，你不确定就说不知道:\n"
    #         response = client.chat.completions.create(
    #             model="hunyuan-pro",
    #             messages=[
    #                 {
    #                     "role": "system",
    #                     "content": context
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": prompt + self.q,
    #                 },
    #             ],
    #             tools=tools
    #         )
    #         return response.choices[0].message

    def message(self):
        # import chromadb.api
        # chromadb.api.client.SharedSystemClient.clear_system_cache()
        embedding_fun = SentenceTransformerEmbeddings(model_name="./text2vec-base-chinese")
        db = Chroma(persist_directory="D:/chroma_vector_data/", embedding_function=embedding_fun)
        doc = db.similarity_search(self.q)
        if len(doc) != 0:
            context = doc[0].page_content
        else:
            context = " "
        client = OpenAI(
            api_key='sk-u3LMNOLlKjtflTBan2daXvuc309dFO8IP51vro22vXLaAnUz',  # 混元 APIKey
            base_url="https://api.hunyuan.cloud.tencent.com/v1",  # 混元 endpoint
            # base_url='https://api.aihao123.cn/luomacode-api/open-api/v1',
            # api_key='sk-t1f6f5i2pp4lp3ir59hg5u7t3qoq6q97t4704iit02n437ad',
        )
        prompt = "对于以下的问题，你不确定就说不知道:\n"
        response = client.chat.completions.create(
            model="hunyuan-pro",
            messages=[
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": prompt + self.q,
                },
            ],
            tools=tools
        )
        return response.choices[0].message
