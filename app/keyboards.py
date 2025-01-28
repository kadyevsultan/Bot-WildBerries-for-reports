from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_shops


async def add_shop_confirm_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='✔️ Подтвердить', callback_data='shopadd_confirm'))
    keyboard.add(InlineKeyboardButton(text='❌ Отмена', callback_data='shopadd_cancel'))
    return keyboard.adjust(2).as_markup()


async def get_shops_delete_keyboard(tg_id):
    keyboard = InlineKeyboardBuilder()
    shops = await get_shops(tg_id)
    for shop in shops:
        keyboard.add(InlineKeyboardButton(text=shop.shop_name, callback_data=f"shopdelete_{shop.shop_name}"))
    keyboard.add(InlineKeyboardButton(text='❌ Отмена', callback_data='shopdelete_cancel_delete'))
    return keyboard.adjust(1).as_markup()


async def get_shops_for_report_keyboard(tg_id):
    keyboard = InlineKeyboardBuilder()
    shops = await get_shops(tg_id)
    for shop in shops:
        keyboard.add(InlineKeyboardButton(text=shop.shop_name, callback_data=f"shopreport_{shop.shop_name}"))
    keyboard.add(InlineKeyboardButton(text='❌ Отмена', callback_data='shopreport_cancel_report'))
    return keyboard.adjust(1).as_markup()


async def get_date_for_report_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='За Сегодня', callback_data='shopreport_date_today'))
    keyboard.add(InlineKeyboardButton(text='За Вчера', callback_data='shopreport_date_yesterday'))
    keyboard.add(InlineKeyboardButton(text='За Неделю', callback_data='shopreport_date_week')) 
    keyboard.add(InlineKeyboardButton(text='Указать период', callback_data='shopreport_date_custom'))
    keyboard.add(InlineKeyboardButton(text='❌ Отмена', callback_data='shopreport_date_cancel_report'))
    return keyboard.adjust(2).as_markup()

async def get_type_for_report_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Общая сумма продаж', callback_data='shopreport_type_sales_sum'))
    keyboard.add(InlineKeyboardButton(text='Количество проданных единиц', callback_data='shopreport_type_sales_count_products'))
    keyboard.add(InlineKeyboardButton(text='Средняя цена продажи', callback_data='shopreport_type_avg_price'))
    keyboard.add(InlineKeyboardButton(text='Коммиссия WildBerries', callback_data='shopreport_type_wb_commission'))
    keyboard.add(InlineKeyboardButton(text='Скидка Wildberries', callback_data='shopreport_type_wb_discount'))
    keyboard.add(InlineKeyboardButton(text='Коммиссия эквайринга', callback_data='shopreport_type_acquiring_commission'))
    keyboard.add(InlineKeyboardButton(text='Стоимость логистики', callback_data='shopreport_type_logistics_cost'))
    keyboard.add(InlineKeyboardButton(text='Стоимость хранения', callback_data='shopreport_type_storage_cost'))
    keyboard.add(InlineKeyboardButton(text='❌ Отмена', callback_data='shopreport_type_cancel_report'))
    return keyboard.adjust(2).as_markup()