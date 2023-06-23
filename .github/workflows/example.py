#https://qiita.com/gaato/items/9ed028ffecdbf9ecaf2a
#に感謝感謝。
import sys
import time
from fastapi import FastAPI
import requests

app=FastAPI()

@app.get("/api/v1/PaizaCR/{code}")

def PaizaCR(code:str =None):
    if code:
        runresult=PaizaTrue(code)
        return {
            "status":"200",
            "code":code,
            "results":{
                "status":runresult["result"],
                "Errors":{
                    "Error":runresult["stderr"],
                    "Build_Error":runresult["build_stderr"],
                },
                "result":runresult["stdout"],
            }
        }
    return {
        "status":"Error",
        "code":code,
        "results":{
            "status":"Failed",
            "Error":{
                "Error":"",
                "Build_Error":"",
            },
            "result":"Failed",
        }
    }

def PaizaTrue(code):
    url = 'http://api.paiza.io'
    # API に送る JSON を辞書で指定
    params = {
        'source_code': code,
        'language': "javascript",
        'input': '',
        'api_key': 'guest',
    }
    # /runners/create に POST リクエストを送る
    response = requests.post(
        url + '/runners/create',
        json=params
    )
    id = response.json()['id']

    time.sleep(2.0)

    # API に送る JSON を辞書で指定
    params = {
        'id': id,
        'api_key': 'guest',
    }
    # /runners/get_details に GET リクエストを送る
    response = requests.get(
        url + '/runners/get_details',
        json=params
    )
    # 結果を辞書にする
    result = response.json()

    return result
