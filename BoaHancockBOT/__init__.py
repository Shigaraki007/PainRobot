import logging
import os
import sys
import time
import spamwatch
from pyrogram import Client, errors
import telegram.ext as tg
from telethon import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Python_ARQ import ARQ
from redis import StrictRedis
import aiohttp
from aiohttp import ClientSession

StartTime = time.time()

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        PIRATE_KING_ID = int(os.environ.get('PIRATE_KING_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', None)
    PIRATE_KING_USERNAME = os.environ.get("PIRATE_KING_USERNAME", None)

    try:
        YONKO = set(int(x) for x in os.environ.get("YONKO", "").split())
        STRAWHATS = set(int(x) for x in os.environ.get("STRAWHATS", "").split())
    except ValueError:
        raise Exception(
            "Your younko or strawhats list does not contain valid integers.")

    try:
        ADMIRALS = set(int(x) for x in os.environ.get("ADMIRALS", "").split())
    except ValueError:
        raise Exception(
            "Your Admiral users list does not contain valid integers.")

    try:
        WARLORDS = set(int(x) for x in os.environ.get("WARLORDS", "").split())
    except ValueError:
        raise Exception(
            "Your Warlords users list does not contain valid integers.")

    try:
        VICE_ADMIRALS = set(int(x) for x in os.environ.get("VICE_ADMIRALS", "").split())
    except ValueError:
        raise Exception(
            "Your Vice Admiral users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get('INFOPIC', False))
    EVENT_LOGS = os.environ.get('EVENT_LOGS', None)
    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get('API_ID', None)
    ARQ_API = os.environ.get("ARQ_API", None)
    API_HASH = os.environ.get('API_HASH', None)
    DB_URI = os.environ.get('DATABASE_URL')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    REDIS_URL = os.environ.get('REDIS_URL')
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
    STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', True))
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER',
                                 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    TEST_STICKER = os.environ.get('TEST_STICKER', '')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
    TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    AI_API_KEY = os.environ.get('AI_API_KEY', None)
    WALL_API = os.environ.get('WALL_API', None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    SUPPORT_CHAT = os.environ.get('SUPPORT_CHAT', None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get('SPAMWATCH_SUPPORT_CHAT', None)
    SPAMWATCH_API = os.environ.get('SPAMWATCH_API', None)
    BOT_ID = 1412878118
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ARQ_API_URL = "TheARQ.Tech"

    try:
        BL_CHATS = set(int(x) for x in os.environ.get('BL_CHATS', "").split())
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

else:
    from BoaHancockBOT.config import Development as Config
    TOKEN = Config.TOKEN

    try:
        PIRATE_KING_ID = int(Config.PIRATE_KING_ID)
    except ValueError:
        raise Exception("Your PIRATE_KING_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    PIRATE_KING_USERNAME = Config.PIRATE_KING_USERNAME

    try:
        YONKO = set(int(x) for x in Config.YONKO or [])
        STRAWHATS = set(int(x) for x in Config.STRAWHATS or [])
    except ValueError:
        raise Exception(
            "Your Yonko or Strawhats user list does not contain valid integers.")

    try:
        ADMIRALS = set(int(x) for x in Config.ADMIRALS or [])
    except ValueError:
        raise Exception(
            "Your Admirals users list does not contain valid integers.")

    try:
        WARLORDS = set(int(x) for x in Config.WARLORDS or [])
    except ValueError:
        raise Exception(
            "Your Warlord users list does not contain valid integers.")

    try:
        VICE_ADMIRALS = set(int(x) for x in Config.VICE_ADMIRALS or [])
    except ValueError:
        raise Exception(
            "Your Vice Admiral users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH

    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    TEST_STICKER = Config.TEST_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    INFOPIC = Config.INFOPIC

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

YONKO.add(PIRATE_KING_ID)
STRAWHATS.add(PIRATE_KING_ID)

REDIS = StrictRedis.from_url(REDIS_URL,decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("Your redis server is now alive!")

except BaseException:

    raise Exception("Your redis server is not alive, please check again.")

finally:

   REDIS.ping()

   LOGGER.info("Your redis server is now alive!")

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config.")
else:
    sw = spamwatch.Client(SPAMWATCH_API)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("Boa", API_ID, API_HASH)
pbot = Client("BoaPyro", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
mongo_client = MongoClient(MONGO_DB_URI)
aiohttpsession = ClientSession()
arq = ARQ(ARQ_API, ARQ_API_URL, aiohttpsession)
db = mongo_client.BoaHancockBOT
dispatcher = updater.dispatcher

YONKO = list(YONKO) + list(STRAWHATS)
STRAWHATS = list(STRAWHATS)
ADMIRALS = list(ADMIRALS)
WARLORDS = list(WARLORDS)
VICE_ADMIRALS = list(VICE_ADMIRALS)

# Load at end to ensure all prev variables have been set
from BoaHancockBOT.modules.helper_funcs.handlers import (CustomCommandHandler,
                                                        CustomMessageHandler,
                                                        CustomRegexHandler)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
