from configparser import SafeConfigParser

class ConfigDataException(Exception):
    pass

SECTION = 'garage_bot'

class Config:
    def __init__(self, path):
        self.parser = SafeConfigParser()
        self.parser.read(path)

    @property
    def log_level(self):
        return self.parser.get(SECTION, "log_level", fallback="INFO")

    @property
    def bot_token(self):
        return self.get('bot_token')

    @property
    def group_chat_id(self):
        return self.get('group_chat_id')

    def get(self, key):
        if not self.parser.has_option(SECTION, key):
            raise ConfigDataException("section '%s' does not have value for '%s".format(SECTION, key))

        return self.parser.get(SECTION, key)
