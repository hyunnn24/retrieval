import openai 
import streamlit as st
from bs4 import BeautifulSoup
import requests
from openai import OpenAI

api = st.text_input('Enter your OpenAI API key:', type='password')

if api:
    client = OpenAI(api_key=api)

import time

def run_and_wait(client, assistant, thread):
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
  )
  while True:
    run_check = client.beta.threads.runs.stream(
      thread_id=thread.id,
      run_id=run.id
    )
    print(run_check.status)
    if run_check.status in ['queued','in_progress']:
      time.sleep(2)
    else:
      break
  return run

def download_and_save(url, filename):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  text = soup.get_text(separator=' ', strip=True)
  with open(filename,'w') as fo:
    fo.write(text)

github_url = "https://github.com/hyunnn24/retrieval/blob/main/data.txt"
url = github_url.replace("/blob/", "/raw/")
filename = 'data.txt'

download_and_save(url, filename)

with open(filename) as fi:
  text = fi.read()

#st.write(text)
if api:
  my_file = client.files.create(
      file = open(filename,'rb'),
      purpose='assistants'
  )

  assistant = client.beta.assistants.create(
    name="Financial Analyst Assistant",
    instructions="You're a LOL bottom pick expert. Look at the file and answer.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
  )


ask=st.text_input("상대픽을 입력하세요:")
if ask:
    thread = client.beta.threads.create(
    messages=[
            {
            "role": "user",
            "content": ask,
            #"file_ids": [my_file.id]
            }
        ]
    )
    thread

    run_and_wait(client, assistant, thread)
if run_check.status in ['completed']:
    thread_messages = client.beta.threads.messages.list(thread.id)
    for msg in thread_messages.data:
        st.write(f"{msg.role}: {msg.content[0].text.value}")