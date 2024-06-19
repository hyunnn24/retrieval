import openai 
import streamlit as st
from bs4 import BeautifulSoup
import requests
from openai import OpenAI

api = st.text_input('Enter your OpenAI API key:', type='password')

if api:
    client = OpenAI(api_key=api)


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

st.write(text)
if api:
  assistant = client.beta.assistants.create(
    name="LOL Pick Assistant",
    instructions="You are an expert of league of legend bottonline pick.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
  )

