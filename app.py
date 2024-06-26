import openai 
import streamlit as st
from bs4 import BeautifulSoup
import requests
from openai import OpenAI

api = st.text_input('Enter your OpenAI API key:', type='password')

if api:
    client = OpenAI(api_key=api)
userinput= st.text_input('픽입력:')

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

# st.write(text) TEST
if api:
  vector_store = client.beta.vector_stores.create(name="Bottom pick")

if api:
  assistant = client.beta.assistants.create(
    name="LOL Pick Assistant",
    instructions="문서를 참조하여 (챔피언1의 카운터는 ~입니다 추천조합은~입니다 그 이유는~입니다 챔피언1의 카운터는 ~입니다 추천조합은~입니다 그 이유는~입니다)의 형식만으로 답변하고 카운터와 조합은 문서에서 이유는 직접 생각해서 알려줘 한국어로 답해",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search":{
            "vector_store_ids": [vector_store.id]
        }
    }  
  )



  file_paths = [filename]

  file_streams = [open(path, "rb") for path in file_paths]

  file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id,
  files=file_streams
  )
  if userinput:
    thread = client.beta.threads.create(
      messages=[
        {
          "role": "user",
          "content": userinput,
          #"attachments": [{"file_id": message_file.id, "tools":[{"type":"file_search"}]]
        }
      ]
    )
    #thread
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    #run
    thread_messages = client.beta.threads.messages.list(thread.id, run_id=run.id)
    #thread_messages
    for msg in thread_messages.data:
      st.write(f"{msg.role}: {msg.content[0].text.value}")
      print(f"{msg.role}: {msg.content[0].text.value}")

