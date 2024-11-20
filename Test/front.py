'''
    运用Streamlit完成前端页面显示
'''
import json

from Client import Client
import streamlit as st
import os
from Embedding import Embedding
from langchain_community.document_loaders import TextLoader
from Email import send_email
from TextToPhoto import TextToPhoto

with st.sidebar:
    name = st.text_input("昵称", key="name")
    phone = st.text_input("手机号", key="phone")
    tips = st.checkbox("温馨提示:您与大模型的对话都会被记录,并有可能被用于训练该大模型,勾选即表示您知情并同意",
                       value=False, key=None)
    ifPhoto = st.checkbox("文生图", value=False, key=None)

    # 添加文件上传组件
    uploaded_file = st.file_uploader("上传文件到知识库", type=None)  # 根据需要指定文件类型

st.title("💬 Test")
st.caption("🚀 demo")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "您好，有什么可以帮您?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "您好，有什么可以帮您?"}]


def upload_file(file):
    if file is not None:
        # 获取文件字节内容
        file_bytes = file.read()

        # 将文件保存到本地
        save_path = f"./{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(file_bytes)
        # 使用 TextLoader 加载文本数据
        text = TextLoader(save_path, encoding='utf-8').load()  # 使用 StringIO 处理内容
        Embedding(text).upload()
        return save_path


st.sidebar.button('清空聊天记录', on_click=clear_chat_history)

# 处理文件上传
if uploaded_file is not None:
    os.remove(upload_file(uploaded_file))

if prompt := st.chat_input():
    # if not name:
    #     st.info("请输入昵称.")
    #     st.stop()
    # if not phone:
    #     st.info("请输入手机号.")
    #     st.stop()
    # if not tips:
    #     st.info("请先选中知情同意书.")
    #     st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 调用文生图api
    if ifPhoto:
        url = TextToPhoto(prompt).generate()
        st.image(url)
        st.stop()

    # 调用 Client 类
    message = Client(prompt).message()
    with st.chat_message("assistant"):
        if content := message.content:
            st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})
        if message.tool_calls is not None:
            fn_name = message.tool_calls[0].function.name
            fn_args = message.tool_calls[0].function.arguments

            def confirm_send_fn():
                send_email(
                    sender_email=args["FromEmail"],
                    recipient_email=args["Recipients"],
                    subject=args["Subject"],
                    body=args["Body"],
                )
                st.success("邮件已发送")
                st.session_state.messages.append({"role": "assistant", "content": "邮件已发送，还需要什么帮助吗？"})

            def cancel_send_fn():
                st.warning("邮件发送已取消")
                st.session_state.messages.append({"role": "assistant", "content": "邮件已取消，还需要什么帮助吗？"})

            if fn_name == "send_email":
                args = json.loads(fn_args)
                st.markdown("邮件内容如下：")
                st.markdown(f"发件人: {args['FromEmail']}")
                st.markdown(f"收件人: {args['Recipients']}")
                st.markdown(f"主题: {args['Subject']}")
                st.markdown(f"内容: {args['Body']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.button(
                        label="✅确认发送邮件",
                        on_click=confirm_send_fn)
                with col2:
                    st.button(
                        label="❌取消发送邮件",
                        on_click=cancel_send_fn
                    )
