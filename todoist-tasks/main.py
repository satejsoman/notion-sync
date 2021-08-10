import os
import requests
from todoist import TodoistAPI
from datetime import datetime as dt 
import json

MINOR_TASKS_DB_ID = "995f23a2d3fd477da66936f87492a039"
NOTION_INTEGRATION_TOKEN = os.environ["NOTION_INTEGRATION_TOKEN"]

headers = {
    'Authorization': f"Bearer {NOTION_INTEGRATION_TOKEN}",
    'Content-Type': 'application/json',
    'Notion-Version': '2021-05-13',
}

data = '{ "parent": { "database_id": "' + MINOR_TASKS_DB_ID + '" }, "properties": { "Name": { "title": [ { "text": { "content": "plong" } } ] } } }'

response = requests.post('https://api.notion.com/v1/pages', headers =  headers, data = data)

def sync():
    todoist = TodoistAPI(os.environ["TODOIST_API_KEY"])
    todoist.sync()
    tasks = [
        _ for _ in todoist.state['items'] 
        if  _['due'] is not None          and \
            _['project_id'] == 1272551971 and \
            dt.strptime(_['due']['date'], "%Y-%m-%d") <= dt.today()
    ]


