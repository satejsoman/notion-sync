from pathlib import Path
import json 
import datetime

import requests

weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

try:
    pwd = Path(__file__).resolve().parent
except NameError:
    pwd = Path.cwd()
with (pwd / ".." / "creds.json").open() as f:
    creds = json.load(f)

now = datetime.datetime.now()
dow = weekdays[now.weekday()]

properties = {
    "day": {
        "type": "title",
        "title": [
            { 
                "type": "text", 
                "text": { 
                    "content": dow 
                }
            }
        ]
    },
    "date": {
        'type': 'date',
        'date': {'start': now.strftime("%Y-%m-%d")}
    }
}

if dow != "mon":
    properties["meatless monday"] = {
        'type': 'select',
        'select': {
            'id': '28d53ae7-75c1-4409-b6ca-699387051de5',
            'name': '-',
            'color': 'default'
        }   
    }

response = requests.post(
    "https://api.notion.com/v1/pages", 
    json = { 
        "parent": {"database_id": creds['HABITS_DB_ID']},
        "properties": properties
    },
    headers = {
        "Authorization" : f"Bearer {creds['NOTION_INTEGRATION_TOKEN']}",
        "Notion-Version": "2021-05-13"
    }
)
print(response)
print(json.loads(response.text))
