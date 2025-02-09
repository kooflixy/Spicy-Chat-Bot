Exceptions:
SpicyUserIsNotActivated:
    This error occurs when your SpicyUser() is not activated.
    
    Solution:
    async def login():
        user = SpicyUser()
        await user.activate(refresh_token=YOUR_REFRESH_TOKEN)
    