from env_vars import *
import datetime
from datetime import date, timedelta
import requests
import json
from json import JSONEncoder

secret_key = NOTION_SECRET_KEY
habit_db_id = NOTION_HABIT_DB
analytics_db_id = NOTION_ANALYTICS_DB

base_db_url = "https://api.notion.com/v1/databases/"
base_pg_url = "https://api.notion.com/v1/pages/"

header = {"Authorization": secret_key,
          "Notion-Version": "2021-05-13", "Content-Type": "application/json"}

response_habits_db = requests.post(
    base_db_url + habit_db_id + "/query", headers=header)

response_analytics_db = requests.post(
    base_db_url + analytics_db_id + "/query", headers=header)

# define no. of new pages/records to be added in Tracker
days_count = 30

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

date_list = list()
month_dict = dict()

# Creating list of datetime.date objects for current month pages/records
for page in response_habits_db.json()['results']:
    page_id = page['id']
    props = page['properties']
    current_month = props['Date']['date']['start']
    date_object = date.fromisoformat(current_month)

    if date_object.month == date.today().month:
        date_list.append(date_object)

if not date_list:
    start_date = date.today()
else:
    start_date = max(date_list) + timedelta(days=1)

# Creating dict of page name and id for monthly analytics db
for page in response_analytics_db.json()['results']:
    page_id = page['id']
    props = page['properties']
    page_name = props['Name']['title'][0]['text']['content']
    month_dict[page_name] = page_id

for date in (start_date + timedelta(n) for n in range(days_count)):
    day = date.strftime('%A')
    month = date.strftime('%B')
    relation_id = month_dict[month]
    date_string = date.strftime('%B %-d, %Y')

    # To make datetime.date object JSON serializable
    date_json = json.dumps(date, indent=4, cls=DateTimeEncoder)
    date_modified = date_json[1:11]
    payload = {
        "parent": {
            "database_id": NOTION_HABIT_DB
        },
        "cover": {
            "type": "external",
            "external": {
                "url": "https://github.com/ashleymavericks/notion-habit-tracker/blob/master/assets/"+ day +".png?raw=true"
            }
        },
        "properties": {
            "Date": {
                "date": {"start": date_modified}
            },
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": date_string
                        }
                    }
                ]
            },
            "Relation": {
                "relation": [
                    {
                        "id": relation_id
                    }
                ]
            }
        }
    }
    add_page = requests.post(
        base_pg_url, headers=header, json=payload)
