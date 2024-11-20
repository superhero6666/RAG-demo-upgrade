'''
    嵌入知识库
'''

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
# from langchain_chroma import Chroma


class Embedding:
    def __init__(self, text):
        self.text = text

    def upload(self):
        if self.text is None:
            print("None")
            return False
        if self.text is not None:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=100,
                chunk_overlap=0,
                separators=["}", "\n", "。"],
                length_function=len
            )
            split_docs = text_splitter.split_documents(self.text)
            embedding_function = SentenceTransformerEmbeddings(model_name="./text2vec-base-chinese")

            vectorstore = Chroma.from_documents(split_docs, embedding_function, persist_directory="D:/chroma_vector_data/")  # 本地存储到向量数据库的地址，换成你自己的
            vectorstore.persist()

# filepath = 'C:/Users/klhu03/Desktop/新建文本文档.txt'  #你本地文件及地址
# loader = TextLoader(filepath, encoding='utf-8')
# text = loader.load()
#
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=10,
#     chunk_overlap=0,
#     separators=["}","\n","。"],
#     length_function=len
# )
# split_docs = text_splitter.split_documents(text)
#
# embedding_function = SentenceTransformerEmbeddings(model_name = "./text2vec-base-chinese")
#
# vectorstore = Chroma.from_documents(split_docs, embedding_function, persist_directory="D:/chroma_vector_data/") # 本地存储到向量数据库的地址，换成你自己的
# vectorstore.persist()
#
# # 测试是否嵌入成功
# query = "你是谁？" #测试问句
# doc = vectorstore.similarity_search(query)
# print(doc[0].page_content)
