import configparser, json, struct, time, itertools, os,aiohttp, requests, asyncio
from utils.colors import Loader, print_success, print_fail, print_debug, print_warning, box, color
from ping3 import ping


class ServerHUB:
    def __init__(self):
        self.configPath = "config\\config.ini"
        self.reader = self.writer = None
        self.identifier = None
        self.readConfig()
        self.ip_hub = requests.get(r"https://raw.githubusercontent.com/kantrveysel/sroserverbrowser/refs/heads/main/hub.txt").text
        self.port_hub = int(self.config["HUB"]["port"])
    async def fetch_ip(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ipify.org') as response:
                    self.public_ip = await response.text()
                    print_success(f"[INFO] Public IP alınan: {self.public_ip}")
        except Exception as e:
            print(f"[fetch_ip] IP alınamadı: {e}")
            self.public_ip = "0.0.0.0"

    def print(self, text):
        _ = os.system('cls||clear')
        print(text)
    
    async def connect(self):
        attemp_counter = 0
        with Loader("Trying to connect to the hub", chars = Loader.side_scroll):
            while not self.writer:
                attemp_counter += 1
                try:
                    self.reader, self.writer = await asyncio.open_connection(self.ip_hub, self.port_hub)
                    print_success(f"Attempt {attemp_counter} : connected to HUB")
                except Exception as e:
                    #self.print(f"Attempt {attemp_counter} : Failed to connect to HUB\n{self.ip_hub}:{self.port_hub}\n{str(e)}")
                    self.reader = self.writer = None
                    await asyncio.sleep(attemp_counter)
    
    async def read(self):
        return await self.reader.read(1024)

    async def write(self, package):
        package = json.dumps(package).encode()
        self.writer.write(package)
        await self.writer.drain()
        
    async def handshake(self):
        data = await self.read()
        if not data:
            await connect()
            return
        self.identifier = data.decode()
        package = {
            "id": self.identifier,
            "timestamp": time.time(),
            "data": {
                    "type": "Server",
                    "client_ip": self.public_ip,
                    "settings": self.config["settings"]
                    }
                    }
        await self.write(package)
    
    async def loop(self):
        while data := await self.read():
            print(data)
    
    async def updateConfig(self):
        alldone = False
        while self.writer:
            key = next(self.iter_config)
            package = {
                        "id":self.identifier,
                        "timestamp":time.time(),
                        "data":{
                            "key": key,
                            "data": self.config[key],
                            "type":"config"
                            }
                        }
            self.print(json.dumps(package, indent=2))
            await self.write(package)
            if alldone:
                ping_hub = ping(self.ip_hub)
                ping_hub = 1 if (ping_hub or 0) == 0 else ping_hub
                print(ping_hub*1000)
                await asyncio.sleep(ping_hub*1000)
            else:
                await asyncio.sleep(1)
            if key == list(self.config)[-1]:
                self.readConfig()
                alldone = True
            
    def readConfig(self):
        self.config = configparser.ConfigParser()
        self.config.read( self.configPath )
        box.print(*[i for i in self.config["info"].values() if len(i)< 24], color_code=color.Blue)
        self.config = {section: dict(self.config[section]) for section in self.config.sections()}
        self.iter_config = itertools.cycle(self.config)
    
    async def start(self):
        await self.fetch_ip()
        await self.connect()
        await self.handshake()
        await asyncio.gather(self.loop(), self.updateConfig())
    
