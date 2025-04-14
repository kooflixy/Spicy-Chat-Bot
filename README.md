
# Spicy-Chat-Bot

Spicy-Chat-Bot - telegram bot that allows users to communicate with SpicyChat bots using SpicyAPI.


## Authors

- [@kooflixy](https://www.github.com/kooflixy)


## Installation

Install my-project with npm

```bash
  git clone https://github.com/kooflixy/Spicy-Chat-Bot
  pip install -r requirements.txt
```
    
## Usage/Examples
To start, you need to create a config.py file in the root folder of the project and enter this data into it:

```Python
# debug
DB_ECHO = False
SPICY_LOGS = False

# spicy
SPICY_CLIENT_ID = ''
SPICY_ACTIVE_USER_ID = ''
SPICY_CURRENT_REFRESH_TOKEN = '' 
#During the program's operation, SPICY_CURRENT_REFRESH_TOKEN can change more than once, so the current SPICY_CURRENT_REFRESH_TOKEN is only in the database.
SPICY_DEFAULT_AI_BOT_ID = ''

# db
DB_HOST = ''
DB_PORT = 
DB_USER = ''
DB_PASS = ''
DB_NAME = ''

MAX_HISTORY_BOTS_COUNT = 5

# tg
TG_BOT_API_TOKEN = ''
TG_ADMINS: list[int] = []
```


## Tech Stack

**Client:** Aiogram, AIOHTTP, Asyncpg, Pydantic, Requests, SQLAlchemy

**Server:** PostgreSQL

