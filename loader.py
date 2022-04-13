from aiogram import Bot, Dispatcher, types
import requests
import config
from colorama import Fore, Style
from aiogram.contrib.fsm_storage.memory import MemoryStorage

""" Get bot name with telegram api """
bot_name = requests.get(f"https://api.telegram.org/bot{config.TOKEN}/getMe").json()
bot_name = bot_name['result']['username']
print(f"{Fore.YELLOW}<======{Style.RESET_ALL} INFO {Fore.YELLOW}======>{Style.RESET_ALL}")
print(f"  {Fore.YELLOW}|{Style.RESET_ALL} Bot name:", bot_name)
print(f"  {Fore.YELLOW}|{Style.RESET_ALL} Bot token:", config.TOKEN)
print(f"  {Fore.YELLOW}|{Style.RESET_ALL} Bot app_id:", config.APP_ID)
print(f"  {Fore.YELLOW}|{Style.RESET_ALL} Bot api_hash:", config.API_HASH)
print(f"{Fore.YELLOW}<====================>{Style.RESET_ALL}")


""" Initialize bot """
bot = Bot(token= config.TOKEN , parse_mode=types.ParseMode.HTML) 
storage = MemoryStorage()  # For storing FSM data
dp = Dispatcher(bot, storage=storage)  # For handling messages
print(f"[{Fore.GREEN}INFO{Style.RESET_ALL}] Bot started!")