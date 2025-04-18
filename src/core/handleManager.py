import json
import asyncio

from utils.helpers import create_message
from utils.colors import Loader
from core.client_manager import Client


class MessageHandler:
    def __init__(self, parent):
        self.parent = parent
        self.logger = parent.logger
        
    async def handle(self, data):
        try:
            self.jdata = json.loads(data.decode())
            try:
                _id = self.jdata.get("id")
                _time = self.jdata.get("timestamp",None)
                if _id != self.parent.identifier:
                    raise ValueError("ID miss-match error on incoming message")
                if _time is None:
                    raise ValueError("Missing Timestamp on incoming message")
                data = self.jdata.get("data")
                type = data.get("type","log")
                await self.forward_message(type, data)
            except ValueError as e:
                self.logger.fail(str(e))
        except Exception as e:
            self.logger.fail(f"Failed to handle the message {str(e)}")
            
    async def loginPlayer(self, data):
        _client = Client(data.get("from"), data, self.parent)
        package = {"status":1, "to":_client.id}
        _package = create_message(self.parent.identifier, "info", package)
        await self.parent.write(_package)
        
    async def forward_message(self, type, data):
        if type == "log":
            self.logger.log(data.get("content","No content"))
            return True
        if type == "info":
            self.logger.debug(data.get("content","No info"))
            return True
        if type == "request":
            self.logger.warning(data.get("content","No info"))
            return False
        if type == "join":
            username = data.get("username")
            password = data.get("password")
            ip = data.get("ip")
            ping = data.get("ping")
            if username and password:
                self.logger.success(f"{username} logged in [{ping} ms]")
                await self.loginPlayer(data)