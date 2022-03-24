from env_vars import *
import datetime
from datetime import date, timedelta
import requests
import json
from json import JSONEncoder

secret_key = NOTION_SECRET_KEY
habit_database_id = NOTION_HABIT_DB

base_db_url = "https://api.notion.com/v1/databases/"
base_pg_url = "https://api.notion.com/v1/pages/"

header = {"Authorization": secret_key,
          "Notion-Version": "2021-05-13", "Content-Type": "application/json"}

response_stocks_db = requests.post(
    base_db_url + habit_database_id + "/query", headers=header)

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

date_list = list()

for page in response_stocks_db.json()['results']:
  page_id = page['id']
  props = page['properties']
  current_month = props['Date']['date']['start']
  date_object = date.fromisoformat(current_month)
  
  if date_object.month == date.today().month:
    date_list.append(date_object)

start_date = max(date_list) + timedelta(days=1)

# define no. of new pages/records to be added in Tracker
days_count = 30

for date in (start_date + timedelta(n) for n in range(days_count)):
  # To fetch weekday from date
  day = date.strftime('%A')

  # To make datetime.date object JSON serializable
  date_json = json.dumps(date, indent=4, cls=DateTimeEncoder)
  date_modified = date_json[1:11]

  payload = {
              "parent": {
                  "database_id": NOTION_HABIT_DB
              },
              "properties": {
                  "Date": {
                      "date": {"start": date_modified}
                  },
                  "Name": {
                      "title": [
                          {
                              "text": {
                                  "content": day
                              }
                          }
                      ]
                  }
              }
          }
  add_page = requests.post(
              base_pg_url, headers=header, json=payload)