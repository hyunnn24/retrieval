import openai 
import streamlit as st
from bs4 import BeautifulSoup
import requests
import time

api = st.text_input('Enter your OpenAI API key:', type='password')

if api:
    openai.api_key = api

def run_and_wait(client, assistant, thread):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while True:
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(run_check.status)
        if run_check.status in ['queued', 'in_progress']:
            time.sleep(2)
        else:
            break
    return run_check

def download_and_save(url, filename):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    with open(filename, 'w') as fo:
        fo.write(text)

github_url = "https://github.com/hyunnn24/retrieval/blob/main/data.txt"
url = github_url.replace("/blob/", "/raw/")
filename = 'data.txt'

download_and_save(url, filename)

with open(filename) as fi:
    text = fi.read()

# st.write(text)

try:
    my_file = openai.File.create(
        file=open(filename, 'rb'),
        purpose='assistants'
    )

    assistant = openai.Assistant.create(
        name="Bottom Pick Expert",
        instructions="You're a LOL bottom pick expert. Look at the file and answer.",
        tools=[{"type": "retrieval"}],
        model="gpt-4o",
    )
except:
    st.error("An error occurred")


ask = st.text_input("상대픽을 입력하세요:")
if ask:
    try:
        thread = openai.Thread.create(
            messages=[
                {
                    "role": "user",
                    "content": ask,
                }
            ]
        )
        run_check = run_and_wait(openai, assistant, thread)
        if run_check.status == 'completed':
            thread_messages = openai.Thread.messages.list(thread.id)
            for msg in thread_messages.data:
                st.write(f"{msg.role}: {msg.content[0].text.value}")
    except:
        st.error("An error occurred")
