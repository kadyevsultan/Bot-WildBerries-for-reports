import aiohttp

from aiogram.fsm.state import State, StatesGroup

from datetime import datetime
from dateutil.relativedelta import relativedelta

# AddShop states and functions
class AddShop(StatesGroup):
    api_key = State()
    shop_name = State()
    
    
shop_info_url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"

async def get_shop_name(api_key):
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    
    params = {
    "dateFrom": (datetime.today() - relativedelta(months=1)).strftime("%Y-%m-%d"),  
    "dateTo": datetime.today().strftime("%Y-%m-%d"),  
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(shop_info_url, headers=headers, params=params) as response:
            if response.status == 200:
                return (await response.json())[0]["brand"]
            else:
                return "Error"
    

class Report(StatesGroup):
    shop = State()
    date_from = State()
    date_to = State()
    custom_date = State()
    type_report = State()
