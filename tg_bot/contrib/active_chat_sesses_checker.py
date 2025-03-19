class ActiveChatSessesChecker:
    def __init__(self):
        pass

    active_users = []

    def add(self, user_id: int) -> bool:
        self.active_users.append(user_id)
    
    def check(self, user_id: int) -> bool:
        return (user_id in self.active_users)

    def remove(self, user_id: int) -> None:
        self.active_users.remove(user_id)
    
    def count(self) -> int:
        return len(self.active_users)


active_chats_sesses_checker = ActiveChatSessesChecker()