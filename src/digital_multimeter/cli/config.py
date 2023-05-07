import configparser
import functools
import logging
import os

from digital_multimeter import (
    __config_file_system__ as CONFIG_FILE_SYSTEM,
    __config_file_user__ as CONFIG_FILE_USER,
    __config_section_name__ as CONFIG_SECTION_NAME,
    __env_connect__ as ENV_CONNECT,
    __env_model__ as ENV_MODEL,
)
from digital_multimeter.exceptions import MultimeterException

logger = logging.getLogger(__name__)


class ConfigException(MultimeterException):
    pass


class Config:
    session_config_file = None

    def __init__(self, session_config_file=None):
        self.session_config_file = session_config_file

    def __getattr__(self, item):
        return self.get(item)

    @functools.lru_cache()
    def get(self, item):
        if not self.session_config_file:
            if item == "connect":  # serial port
                env_name = ENV_CONNECT
            elif item == "model":  # dmm model
                env_name = ENV_MODEL
            else:
                raise ConfigException("Unknown configuration attribute requested.", item)

            # Environment variable
            if os.environ.get(env_name):
                logger.debug('"{}" returned from environment variable: {}'.format(item, env_name))
                return os.environ.get(env_name)

        # Configuration file based config setting
        return self.__get_config_from_file(item)

    @functools.lru_cache()
    def __get_config_from_file(self, item):
        config = None

        if self.session_config_file and not os.path.isfile(os.path.expanduser(self.session_config_file)):
            raise ConfigException("Unable to find the configuration filename supplied.", self.session_config_file)

        config_files = [self.session_config_file, CONFIG_FILE_USER, CONFIG_FILE_SYSTEM]

        for config_file in config_files:
            if config_file and os.path.isfile(os.path.expanduser(config_file)):
                config = self.__load_config_file(config_file)
                break

        if type(config) is not dict:
            logger.debug('"{}" unset because no configuration file found.'.format(item))
            return None

        _item = item.replace("_", "").replace("-", "")
        if _item not in config.keys():
            logger.debug('Unable to find "{}" setting in the configuration file.'.format(item))
            return None

        logger.debug('"{}" returned from the configuration file.'.format(item))
        return config[_item]

    @functools.lru_cache()
    def __load_config_file(self, filename, section=CONFIG_SECTION_NAME):
        filename = os.path.expanduser(filename)
        if os.path.isfile(filename):
            cp = configparser.ConfigParser()

            try:
                cp.read(filename)
            except Exception as e:
                raise ConfigException("Unable to correctly parse the configuration file provided.", e)

            if section not in cp.sections():
                raise ConfigException(
                    'Unable to locate the "{}" section in configuration file.'.format(section), filename
                )
            config = {}
            for option in cp.options(section):
                config[str(option).replace("_", "").replace("-", "")] = cp.get(section, option)
            logger.debug("configuration file read: {}".format(filename))
            return config

        raise ConfigException("Unable to find the configuration filename supplied.", filename)
