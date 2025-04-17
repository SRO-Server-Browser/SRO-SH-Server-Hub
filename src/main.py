import asyncio,sys
from utils.helpers import is_admin, request_admin
from core.config_manager import ConfigManager
from core.sql_manager import SQLManager
from core.hub_client import HubClient
from core.logger import Logger
from utils.colors import box

if not is_admin():
    request_admin(sys.executable, __file__)
    sys.exit()
    
async def main():
    box.print("Server Hub","initilization started")
    logger = Logger()
    config_manager = ConfigManager()
    sql_manager = SQLManager(config_manager)
    hub_client = HubClient(config_manager, logger)

    try:
        await hub_client.start()
    finally:
        sql_manager.close()

if __name__ == "__main__":
    asyncio.run(main())