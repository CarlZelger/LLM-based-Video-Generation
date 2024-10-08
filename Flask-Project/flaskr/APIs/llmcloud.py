from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from typing import Dict, List
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openai import OpenAI
# from .upsplash import generateImages, genFileName


def getDataForPP(topic,pages):
    query = f"answer with only five short bullet points nothing more (no punctuation marks),  6 words max, insert a semocolon after every bulletpoint, about {topic}."
    ret = askLLM(query)
    retList = [item.strip().lstrip('• ').lstrip('\n').capitalize() for item in ret.split(";") if item.strip()]
    return retList
    

def make_request(topic: str, title: str) -> Dict[str, str]:
    query = f"write me a coherent text about '{title}' in the context of {topic}; the limit is 300 words dont exeed it; NO introduction NO Notes JUST text"
    content = askLLM(query)
    return {title: content}

def generateText(topic: str, titles: List[str]) -> Dict[str, str]:
    ret = {}
    with ThreadPoolExecutor(max_workers=len(titles)) as executor:
        futures = [executor.submit(make_request, topic, title) for title in titles]
        for future in as_completed(futures):
            result = future.result()
            ret.update(result)
    return {key: ret[key] for key in titles}

        
def askLLM(q):
    openai = OpenAI(
        api_key="API_KEY",
        base_url="https://api.deepinfra.com/v1/openai",
    )

    chat_completion = openai.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[{"role": "user", "content": q}],
    )

    return chat_completion.choices[0].message.content

def addQuestiones(titles: List[str],topic: str):
    i = random.randint(0,len(titles)-1)
    query = f"give me one short and simple question, without providing an answer! about the following topic: {titles[i]} in the context of {topic}; no formattion or additional text, JUST the question NO answer and NO additional Text"
    ret = askLLM(query)
    ret = ret.replace(".","")
    ret = ret.replace("\n","")
    ret = ret.replace(":","")
    ret = ret.replace("!","")
    return ret


def cleanUp(s: str):
    ret = s.replace(":","")
    ret = ret.replace("\"","")
    ret = ret.replace(".","")
    ret = ret.replace("\n","")
    ret = ret.replace("'","")
    ret = ret.replace("etc","")
    ret = ret.strip()
    return ret

def generateSuggestion(text:str):
    query2 =f"provide the reader with a really simple option to improve the linguistic aspects of this text: '{text}', answer in less then five words, only with the option, nothign else. Examples for simple options are: 'use simpler language', 'Use gender-neutral language', 'use more scientific vocabulary'"
    output = cleanUp(askLLM(query2))
    return output

def applySuggestion(content: Dict[str,str],sug: str):
    ret = {}
    for k,v in content.items():
        query = f"rewrite the text: {v} with '{sug}' in mind"
        new_v = askLLM(query,700)
        ret[k] = new_v
    return ret







