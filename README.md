Exceptions:
SpicyUserIsNotActivated:
    This error occurs when your SpicyUser() is not activated.
    
    Solution:
    async def login():
        user = SpicyUser()
        await user.activate(refresh_token=YOUR_REFRESH_TOKEN)


For start create config.py file in root directory and paste in:
'''
#debug
DB_ECHO = False

#spicy
SPICY_CLIENT_ID = 
SPICY_ACTIVE_USER_ID = 
SPICY_DEFAULT_AI_BOT_ID = 

#db
DB_HOST = 
DB_PORT = 
DB_USER = 
DB_PASS = 
DB_NAME = 

#tg
TG_BOT_API_TOKEN = 

'''