from utils.colors import print_success, print_fail


class Client:
    def __init__(self, id, data, hub):
        self.id = id
        self.data = data
        self.username = data.get("username")
        self.password = data.get("password")
        self.ip = data.get("ip")
        self.ping = data.get("ping")
        self.hub = hub
        self.hub.client_list.append(self)
        self.register()
        
    def register(self):
        _sql_manager = self.hub.sql_manager
        _ret = _sql_manager.execute_sql_file("login.sql",params = 
                    (self.username, self.password, self.ip))        
    
    async def handle(self, data):
        pass