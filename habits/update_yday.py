import datetime
import json
from pathlib import Path

import duolingo
import requests


def duolingo_streak_extended(creds):
    return duolingo.Duolingo(
        creds["DUOLINGO_USER"], 
        creds["DUOLINGO_PASS"]).\
    get_streak_info()\
    ["streak_extended_today"]

try:
    pwd = Path(__file__).resolve().parent.parent
except NameError:
    pwd = Path.cwd()
with (pwd / "creds.json").open() as f:
    creds = json.load(f)    

# query for "yesterday"'s entry - script runs at 11:59pm
print("querying for previous entry")
response = requests.post(
    f"https://api.notion.com/v1/databases/{creds['HABITS_DB_ID']}/query", 
    headers = {
        "Authorization" : f"Bearer {creds['NOTION_INTEGRATION_TOKEN']}",
        "Notion-Version": "2021-05-13"
    }
)

page_id = json.loads(response.text)["results"][0]["id"]
new_properties = {}

# check if duolingo streak continued 
print("checking duolingo")
if duolingo_streak_extended(creds):
    new_properties["duolingo"] = {"select": {"name": "_"}}


# check if waking up session exists 

# grab fitbit data 

# write new entry
print("updating entry")
response = requests.patch(
    f"https://api.notion.com/v1/pages/{page_id}", 
    json = { 
        "parent": {"database_id": creds['HABITS_DB_ID']},
        "properties": new_properties
    },
    headers = {
        "Authorization" : f"Bearer {creds['NOTION_INTEGRATION_TOKEN']}",
        "Notion-Version": "2021-05-13"
    }
)

print(response)
print(json.loads(response.text))
