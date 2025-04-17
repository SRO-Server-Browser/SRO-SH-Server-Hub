# src/core/config_manager.py
import configparser
import os

class ConfigManager:
    def __init__(self, config_path="config/config.ini", special_config_path="config/special_config.ini"):
        self.config_path = config_path
        self.special_config_path = special_config_path
        self.config = self._load_config()
        self.special_config = self._load_special_config()

    def _load_config(self):
        config = configparser.ConfigParser()
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        config.read(self.config_path)
        return {section: dict(config[section]) for section in config.sections()}

    def _load_special_config(self):
        config = configparser.ConfigParser()
        if not os.path.exists(self.special_config_path):
            raise FileNotFoundError(f"Special config file not found: {self.special_config_path}")
        config.read(self.special_config_path)
        return {section: dict(config[section]) for section in config.sections()}

    def get_config(self, section=None):
        if section:
            return self.config.get(section, {})
        return self.config

    def get_special_config(self, section=None):
        if section:
            return self.special_config.get(section, {})
        return self.special_config