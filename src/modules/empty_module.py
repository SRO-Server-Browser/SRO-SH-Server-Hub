import asyncio

# This is the base class for creating a module.
class Module:
    # The name of the module, can be used for identification.
    NAME = "Example Module"
    
    def __init__(self, interval=0.1, sql_manager=None, config_manage=None, hub_client=None):
        """
        Initializes the module with required dependencies and settings.
        
        :param interval: The interval at which the loop should run (in seconds).
        :param sql_manager: An optional object for managing SQL database operations (default is None).
        :param config_manage: An optional object for managing configurations (default is None).
        :param hub_client: An optional object for handling hub client connections (default is None).
        """
        self.sql_manager = sql_manager  # SQL manager for database interaction
        self.config_manage = config_manage  # Config manager for handling configurations
        self.hub_client = hub_client  # Hub client for handling external connections
        self.interval = interval  # The interval for the async loop to wait before each iteration
        self.running = False  # State variable to control the loop execution

    async def loop(self):
        """
        The main asynchronous loop that runs continuously while the module is active.
        It runs every 'interval' seconds and can be customized by overriding this method.
        """
        while self.running:  # The loop runs as long as the module is running
            await asyncio.sleep(self.interval)  # Wait for the specified interval
            print("Here is loop")  # Example action during each loop iteration
    
    def start(self):
        """
        Starts the module by creating a new asynchronous task to run the loop.
        """
        print("Starting the module...")  # Inform about the start of the module
        self.running = True  # Set the module state to running
        asyncio.create_task(self.loop())  # Start the async loop in the background
    
    def stop(self):
        """
        Stops the module by setting the running state to False.
        The loop will exit after the current iteration.
        """
        print("Stopping the module...")  # Inform about stopping the module
        self.running = False  # Set the module state to stopped
