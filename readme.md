# Telegram bot that alerts new Savings deals on Binance

Binance has some short term saving plans that pay attractive interest rates. Especially in the savings categorized as "activities". However, they are offered in very limited quantties.

This script sends you alert messages via Telegram when new "Activities" become available. 

Existing saving plans are stored locally in history_activity.json.

### Example telegram bot message:
> New items detected: 
PIVX  |  projectId: HPIVX14DAYSS002K 
FRONT  |  projectId: HFRONT30DAYSS002K 
VITE  |  projectId: HVITE30DAYSS007K 
>
>All active activities: 
PIVX | duration: 14 | APY: 0.3 | lotSize: 100 | projectId: HPIVX14DAYSS002K
FRONT | duration: 30 | APY: 1.825 | lotSize: 10 | projectId: HFRONT30DAYSS002K
VITE | duration: 30 | APY: 0.16 | lotSize: 100 | projectId: HVITE30DAYSS007K

## Setup
You just need to set up 2 things:



#### Keys
Fill in your keys in config.py.

From Binance, you need to fetch your API keys.
From Telegram, you need to create a bot and fetch corresponding token IDs and chatIDs. 
Read this for more details on that: https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e


#### Cron
You need to schedule your script to run every few minutes. 

If you're unsure how this works, google "how to set up cron job."

## Ideas for improvement
- Track other savings deals like short term fixed savings, variable rate savings etc.
- Option to execute trade from Telegram bot (or just execute immediately upon detection)
