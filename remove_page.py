import os
from dotenv import load_dotenv
import datetime
from datetime import date, timedelta
import requests
import json
from json import JSONEncoder

# load environment variables from .env
load_dotenv()

base_db_url = "https://api.notion.com/v1/databases/"
base_pg_url = "https://api.notion.com/v1/pages/"

header = {"Authorization": os.getenv('NOTION_SECRET_KEY'),
          "Notion-Version": "2021-05-13", "Content-Type": "application/json"}

response_habits_db = requests.post(
    base_db_url + os.getenv('NOTION_HABIT_DB') + "/query", headers=header)


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


# Deleting previous year data, else it will mess up with monthly analytics
for page in response_habits_db.json()['results']:
    page_id = page['id']
    props = page['properties']
    current_month = props['Date']['date']['start']
    date_object = date.fromisoformat(current_month)

    if date_object.year < date.today().year:

        payload = {
            "archived": True
        }

        remove_page = requests.patch(
            base_pg_url + page_id, headers=header, json=payload)
        
        if remove_page.status_code == 200:
            print(
                f"Page removed, Status code: {remove_page.status_code}, Reason: {remove_page.reason}")
        else:
            print(
                f"Something went wrong, Status code: {remove_page.status_code}, Reason: {remove_page.reason}")
