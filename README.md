<div align="center">
<h1 align="center">Notion Habit Tracker</h1>
<img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"/><br><br>
A fully automated Notion Habit Tracker template with real-time performance graph and monthly analytics.<br><br>
  
[![notion_habit_tracket](/assets/notion_habit_tracker_public_page.png)](https://ashleymavericks.gumroad.com/l/notion-habit-tracker)
</div>

***
## Features
- Automated daily page addition, either via Notion template repeat feature or by running the Python script once a year
- Script will also automatically delete any previous year pages so that they won't mess up with monthly analytics
- Monthly analytics provide Habits completion percentage insights using star ratings
- Real-time daily performance charts
- Habit completion visual cues using progress bar and custom star ratings

## Setup Pre-requisites
- Duplicate this [Notion Template](https://ashleymavericks.gumroad.com/l/notion-habit-tracker) to get started.
- Use services like [Notion Charts](https://notioncharts.io/) and [Data Jumbo](https://www.datajumbo.co/) to have the monthly analytics chart for your habits database.

## No Code Approach
- With the new notion recurring template update, you can simply set an individual weekday template for a weekly repeat and it will automatically add a new page to the database.

## Find Database ID
Login Notion in a browser and viewing the database as a full page, the database ID is the part of the URL after your workspace name and the slash (acme/) and before the question mark (?). The ID is 32 characters long, containing numbers and letters. Copy the ID and paste it somewhere you can easily find later.

Repeat this process for both Habits DB and Analytics DB, and take a note of these Database IDs

```
https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...
                                  |--------- Database ID --------|
```

## Script Usage
1. Clone the repo
```bash
git clone https://github.com/ashleymavericks/notion-habit-tracker.git
```
2. Create a .env file in the project folder
3. Add NOTION_HABIT_DB, NOTION_ANALYTICS_DB and [NOTION_SECRET_KEY](https://syncwith.com/p/notion-api-key-qrsJHMnH5LuHUjDqvZnmWC) in .env file
```python
NOTION_SECRET_KEY=PASTE_KEY_HERE
NOTION_HABIT_DB=PASTE_KEY_HERE
NOTION_ANALYTICS_DB=PASTE_KEY_HERE
```
4. Run the Script called `main.py`, it may take some time to complete.
```python
python3 main.py
```
5. Due to Notion API rate throttling, the script might not able to remove a huge number of previous year records at once, in that scenario kindly run `remove_page.py` until all records get purged
```python
python3 remove_page.py
```

## Contributing
Feel free to reach out, if you want to further improve the template.

## License
This project is licensed under the MIT license
