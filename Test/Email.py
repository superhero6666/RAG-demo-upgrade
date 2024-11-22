import os

from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
import openai

import streamlit as st

GPT_MODEL = "gpt-4o-mini"


client = OpenAI(
    api_key='sk-u3LMNOLlKjtflTBan2daXvuc309dFO8IP51vro22vXLaAnUz',  # 混元 APIKey
    base_url="https://api.hunyuan.cloud.tencent.com/v1",  # 混元 endpoint
    # base_url='https://api.aihao123.cn/luomacode-api/open-api/v1',
    # api_key='sk-t1f6f5i2pp4lp3ir59hg5u7t3qoq6q97t4704iit02n437ad',
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送带有主题和内容的邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "Subject": {
                        "type": "string",
                        "description": "邮件主题",
                    },
                    "Body": {
                        "type": "string",
                        "description": "邮件内容",
                    },
                    "Recipients": {
                        "type": "string",
                        "description": "收件人邮箱地址",
                    }
                },
                "required": ["Subject", "Body", "Recipients"],
            },
        }
    }
]

st.sidebar.header("📃 Dialgue Session:")


def chat_completion_request(messages, tools=None, tool_choice=None):
    try:
        response = client.chat.completions.create(
            model="hunyuan-pro",
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("不能生成回复")
        print(f"Exception: {e}")
        return e


def send_email(sender_email, recipient_email, subject, body):
    # 创建 MIMEMultipart 对象
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # 创建 SMTP_SSL 会话
    with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
        server.login(sender_email, "qsmeodnmfwmkejij")
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()


def main():
    st.title("AI Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Enter"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = chat_completion_request(
            messages=st.session_state.messages,
            tools=tools
        )
        st.sidebar.json(st.session_state)
        st.sidebar.write(response)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            print(1)
            if content := response.choices[0].message.content:
                print(2)
                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})
            if response.choices[0].message.tool_calls is not None:
                print(3)
                fn_name = response.choices[0].message.tool_calls[0].function.name
                fn_args = response.choices[0].message.tool_calls[0].function.arguments

                def confirm_send_fn():
                    send_email(
                        sender_email=args["FromEmail"],
                        recipient_email=args["Recipients"],
                        subject=args["Subject"],
                        body=args["Body"],
                    )
                    st.success("邮件已发送")
                    st.session_state.messages.append({"role": "assistant", "content": "邮件已发送，还需要什么帮助吗？"})
                    # reflash sidebar
                    st.sidebar.json(st.session_state)
                    st.sidebar.write(response)

                def cancel_send_fn():
                    st.warning("邮件发送已取消")
                    st.session_state.messages.append({"role": "assistant", "content": "邮件已取消，还需要什么帮助吗？"})
                    # reflash sidebar
                    st.sidebar.json(st.session_state)
                    st.sidebar.write(response)

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


if __name__ == "__main__":
    main()
