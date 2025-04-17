# src/core/hub_client.py
import aiohttp
import asyncio
import json
import time
import requests
from ping3 import ping
from utils.colors import Loader, print_success, print_fail

class HubClient:
    def __init__(self, config_manager, logger):
        self.config_manager = config_manager
        self.logger = logger
        self.ip_hub = self._get_hub_ip()
        self.port_hub = int(self.config_manager.get_config("HUB").get("port", 8888))
        self.reader = None
        self.writer = None
        self.identifier = None
        self.public_ip = None
        self.max_reconnect_attempts = 5

    def _get_hub_ip(self):
        """HUB IP adresini alır, hata durumunda varsayılan bir değer döner."""
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/SRO-Server-Browser/sro-browser-web/refs/heads/main/data/server.txt",
                timeout=5
            )
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            self.logger.fail(f"[HUB] Failed to fetch HUB IP")
            return "127.0.0.1"  # Varsayılan IP, gerektiğinde değiştir

    async def fetch_ip(self):
        """Genel IP adresini asenkron olarak alır."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.ipify.org", timeout=5) as response:
                    self.public_ip = await response.text()
                    self.logger.success(f"[INFO] Public IP fetched: {self.public_ip}")
        except aiohttp.ClientError as e:
            self.logger.fail(f"[fetch_ip] Failed to fetch IP: {e}")
            self.public_ip = "0.0.0.0"

    async def connect(self):
        """HUB'a bağlanmayı dener, üstel geri çekilme ile yeniden bağlanır."""
        attempt = 0
        with Loader("Trying to connect to the hub", chars=Loader.side_scroll):
            while not self.writer and attempt < self.max_reconnect_attempts:
                attempt += 1
                try:
                    self.reader, self.writer = await asyncio.open_connection(self.ip_hub, self.port_hub)
                    self.logger.success(f"Attempt {attempt}: Connected to HUB ({self.ip_hub}:{self.port_hub})")
                    return
                except (OSError, asyncio.TimeoutError) as e:
                    self.logger.fail(f"Attempt {attempt}: Failed to connect to HUB - {e}")
                    self.reader = self.writer = None
                    await asyncio.sleep(min(2 ** attempt, 32))  # Üstel geri çekilme
            self.logger.fail(f"[HUB] Max reconnect attempts ({self.max_reconnect_attempts}) reached.")

    async def read(self):
        """HUB'dan veri okur."""
        try:
            return await self.reader.read(1024)
        except (AttributeError, asyncio.CancelledError):
            return b""

    async def write(self, package):
        """HUB'a veri yazar."""
        if not self.writer:
            self.logger.fail("[HUB] No connection to write to.")
            return
        try:
            package_data = json.dumps(package).encode()
            self.writer.write(package_data)
            await self.writer.drain()
        except (AttributeError, asyncio.CancelledError) as e:
            self.logger.fail(f"[HUB] Failed to write package: {e}")

    async def handshake(self):
        """HUB ile el sıkışma işlemini gerçekleştirir."""
        data = await self.read()
        if not data:
            self.logger.warning("[HUB] No handshake data received, reconnecting...")
            await self.connect()
            return
        self.identifier = data.decode().strip()
        package = {
            "id": self.identifier,
            "timestamp": time.time(),
            "data": {
                "type": "Server",
                "client_ip": self.public_ip,
                "settings": self.config_manager.get_config("settings")
            }
        }
        await self.write(package)
        self.logger.success(f"[HUB] Handshake completed with ID: {self.identifier}")

    async def loop(self):
        """HUB'dan gelen verileri sürekli dinler."""
        while self.writer:
            data = await self.read()
            if not data:
                self.logger.warning("[HUB] Connection lost, reconnecting...")
                await self.connect()
                await self.handshake()
                continue
            self.logger.debug(f"[HUB] Received: {data.decode()}")

    async def update_config(self):
        """Config verilerini periyodik olarak HUB'a gönderir."""
        import itertools
        config_keys = itertools.cycle(self.config_manager.get_config().keys())
        is_initial_cycle = True
        while self.writer:
            key = next(config_keys)
            package = {
                "id": self.identifier,
                "timestamp": time.time(),
                "data": {
                    "key": key,
                    "data": self.config_manager.get_config(key),
                    "type": "config"
                }
            }
            self.logger.debug(json.dumps(package, indent=2))
            await self.write(package)

            if is_initial_cycle and key == list(self.config_manager.get_config())[-1]:
                is_initial_cycle = False
                ping_hub = ping(self.ip_hub) or 1
                await asyncio.sleep(ping_hub * 1000)
            else:
                await asyncio.sleep(1)

    async def start(self):
        """HUB istemcisini başlatır."""
        await self.fetch_ip()
        await self.connect()
        await self.handshake()
        await asyncio.gather(self.loop(), self.update_config())

    async def stop(self):
        """HUB bağlantısını kapatır."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.logger.success("[HUB] Connection closed.")