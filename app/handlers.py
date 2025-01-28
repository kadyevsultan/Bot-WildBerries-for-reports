from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.models import async_session
import app.database.requests as db

from app.states import AddShop, Report #Состояния
from app.states import get_shop_name #Функции

#Функции для отчетов
from app.reports import (
    get_sales_sum,
    get_average_price_for_product,
    get_count_products_sold,
    get_commission_acquiring,
    get_discount_wb,
    get_price_delivery,
    get_price_storage,
    get_wb_commission,
)

from app.keyboards import (
    add_shop_confirm_keyboard,
    get_shops_delete_keyboard, 
    get_shops_for_report_keyboard, 
    get_date_for_report_keyboard,
    get_type_for_report_keyboard
    )

from datetime import datetime, timedelta
router = Router()


@router.message(CommandStart())
async def cmd_start(message):
    await db.set_user(message.from_user.id)
    await message.answer("Привет! 👋\n\n"
                         "Я - бот для аналитики продаж на Wildberries. С моей помощью вы можете:\n"
                         "- 📊 Получать отчеты о продажах ваших магазинов.\n"
                         "- 🏪 Управлять списком магазинов (добавлять или удалять магазины).\n"
                         "- 📜 Смотреть список подключенных магазинов.\n\n"
                         "Для начала работы добавьте магазин с помощью команды /addshop 🚀\n"
                         "Для просмотра доступных комманд используйте команду /help")
    
    
@router.message(Command("help"))
async def cmd_help(message):
    await message.answer("Вот что я умею:\n\n"
                         "1️⃣ Добавить магазин: Используйте команду /addshop, чтобы добавить магазин, введя API-ключ и его имя.\n"
                         "2️⃣ Удалить магазин: Команда /delshop поможет удалить магазин.\n"
                         "3️⃣ Список магазинов: Команда /shops покажет все добавленные магазины.\n"
                         "4️⃣ Получить отчет: С помощью /report вы можете запросить отчет о продажах за любой период.\n\n"
                         "🔒 Все данные о ваших магазинах хранятся локально и конфиденциально.\n\n"
                         "Попробуйте добавить первый магазин с помощью команды /addshop и начните анализировать продажи! 🚀"
                         )
    
    
@router.message(Command("addshop"))
async def cmd_addshop(message, state: FSMContext):
    await state.set_state(AddShop.api_key)
    await message.answer("Введите API-ключ магазина Wildberries(После ввода ключа, нужно немного подождать!):")
    
    
@router.message(AddShop.api_key)
async def cmd_addshop_api_key(message, state: FSMContext):
    api_key = message.text.strip()
    
    shop_name = await get_shop_name(api_key)
    
    if shop_name == "Error":
        await message.answer("Не удалось получить информацию о магазине. Проверьте правильность API-ключа и попробуйте снова.")
        await state.clear()  
    else:
        await state.update_data(api_key=api_key, shop_name=shop_name)
        await state.set_state(AddShop.shop_name)
        await message.answer(f"Магазин найден: {shop_name}\nХотите добавить его?", reply_markup=await add_shop_confirm_keyboard())
        
@router.callback_query(F.data.startswith("shopadd_"), AddShop.shop_name)
async def cmd_confirm_shop_name(callback_query: CallbackQuery, state: FSMContext):
    user_answer = callback_query.data

    if user_answer == "shopadd_confirm":
        # Сохраняем данные магазина, если пользователь подтвердил
        user_data = await state.get_data()
        api_key = user_data["api_key"]
        shop_name = user_data["shop_name"]
        tg_id = callback_query.from_user.id

        # Добавляем магазин в базу данных
        await db.add_shop(tg_id, api_key, shop_name)

        await callback_query.message.edit_text(f"Магазин {shop_name} успешно добавлен.")
        await state.clear()  # Завершаем процесс добавления магазина

    elif user_answer == "shopadd_cancel":
        await callback_query.message.edit_text("Магазин не был добавлен. Вы можете попробовать снова с помощью команды /addshop.")
        await state.clear()  # Завершаем процесс добавления магазина
        

@router.message(Command("shops"))
async def cmd_shops(message):
    shops = await db.get_shops(message.from_user.id)
    if not shops:
        await message.answer("Список магазинов пока что пуст")
        return
    
    shop_list = "\n".join([f"• {shop.shop_name}" for shop in shops])
    await message.answer(f"Список магазинов:\n{shop_list}")


@router.message(Command("delshop"))
async def cmd_delshop(message):
    shops = await db.get_shops(message.from_user.id)
    if not shops:
        await message.answer("Список магазинов пока что пуст")
        return
    
    await message.answer("Выберите магазин для удаления:", reply_markup=await get_shops_delete_keyboard(message.from_user.id))
    
@router.callback_query(F.data.startswith("shopdelete_"))
async def cmd_delshop_callback(callback_query: CallbackQuery):
    data = callback_query.data
    tg_id = callback_query.from_user.id
    shop_name = data[len("shopdelete_"):]
    
    if data == 'shopdelete_cancel_delete':
        await callback_query.message.edit_text("Удаление магазина отменено.")
        return 
    
    try:
        await db.del_shop(tg_id, shop_name)
        await callback_query.message.edit_text(f"Магазин {shop_name} успешно удален.")
    except Exception as e:
        await callback_query.message.edit_text(f"Произошла ошибка при удалении магазина: {e}")
    
    
@router.message(Command("report"))
async def cmd_report(message, state: FSMContext):
    shops = await db.get_shops(message.from_user.id)
    if not shops:
        await message.answer("Список магазинов пока что пуст")
        return
    await state.set_state(Report.shop)
    await message.answer(
        "Помните, что отчеты могут занимать некоторое время!\n"
        "Также обратите внимание, что API WB имеет ограничение по количеству запросов.\n "
        "Не стоит отправлять запросы слишком часто, чтобы избежать блокировки.\n "
        "Пожалуйста, подождите, если возникнут проблемы с запросом.\n"
    )
    await message.answer("Выберите магазин для отчета:", reply_markup=await get_shops_for_report_keyboard(message.from_user.id))
    
    
@router.callback_query(F.data.startswith("shopreport_"), Report.shop)
async def cmd_report_callback(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    shop_name = data[len("shopreport_"):]
    
    if data == 'shopreport_cancel_report':
        await callback_query.message.edit_text("Отчет отменен.")
        await state.clear()
        return 
    
    try:
        await state.update_data(shop=shop_name)
        await state.set_state(Report.date_from)
        await callback_query.message.edit_text(f'Выберите дату для отчета:', reply_markup=await get_date_for_report_keyboard())
    except Exception as e:
        await callback_query.message.edit_text(f"Произошла ошибка при отправке отчета: {e}")
        await state.clear()
        
@router.callback_query(F.data.startswith("shopreport_date_"), Report.date_from)
async def cmd_report_date_callback(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    dateFrom = ''
    dateTo = ''
    
    if data == 'shopreport_date_cancel_report':
        await callback_query.message.edit_text("Отчет отменен.")
        await state.clear()
        return 
    
    try:
        if data == 'shopreport_date_today':
            dateFrom = datetime.now().strftime("%Y-%m-%d")
            dateTo = dateFrom
            
        elif data == 'shopreport_date_yesterday':
            dateFrom = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            dateTo = dateFrom

        elif data == 'shopreport_date_week':
            dateFrom = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            dateTo = datetime.now().strftime("%Y-%m-%d")
            
        elif data == 'shopreport_date_custom':
            await callback_query.message.edit_text(f'Для начала введите начальную дату отчета в формате ГГГГ-ММ-ДД(например: 2025-01-01)')
            await state.set_state(Report.custom_date)
            return
            
        await state.update_data(date_from=dateFrom, date_to=dateTo)
        
        await state.set_state(Report.type_report)
        
        await callback_query.message.edit_text(f'Выберите тип отчета:', reply_markup=await get_type_for_report_keyboard())
        
    except Exception as e:
        await callback_query.message.edit_text(f"Произошла ошибка при отправке отчета: {e}")
        await state.clear()
        

@router.message(Report.custom_date)
async def cmd_report_custom_date(message, state: FSMContext):
    try:
        custom_date = message.text.strip()
        datetime.strptime(custom_date, "%Y-%m-%d")
        
        await state.update_data(date_from=message.text)
        await state.set_state(Report.date_to)
        await message.answer(f'Введите конечную дату отчета в формате ГГГГ-ММ-ДД(например: 2025-01-02)')
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД(например: 2025-01-01)")
    except Exception as e:
        await message.answer(f"Произошла ошибка при отправке отчета: {e}")
        await state.clear()


@router.message(Report.date_to)
async def cmd_report_date_to(message, state: FSMContext):
    try:
        date_to = message.text.strip()
        datetime.strptime(date_to, "%Y-%m-%d")
        
        await state.update_data(date_to=message.text)
        await state.set_state(Report.type_report)
        await message.answer(f'Выберите тип отчета:', reply_markup=await get_type_for_report_keyboard())
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД(например: 2025-01-01)")
    except Exception as e:
        await message.answer(f"Произошла ошибка при отправке отчета: {e}")
        await state.clear()

@router.callback_query(F.data.startswith("shopreport_type_"), Report.type_report)
async def cmd_report_type_callback(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    tg_id = callback_query.from_user.id
    state_data = await state.get_data()
    shop_name = state_data.get("shop")
    date_from = state_data.get("date_from")
    date_to = state_data.get("date_to")
    api_key = await db.get_api_by_shop_name(session=async_session, shop_name=shop_name, tg_id=tg_id)
    
    if data == 'shopreport_type_cancel_report':
        await callback_query.message.edit_text("Отчет отменен.")
        await state.clear()
        return 
    
    try:
        await state.update_data(type_report=data[len("shopreport_type_"):])
        await state.clear()
        if data == 'shopreport_type_sales_sum':
            result = await get_sales_sum(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        elif data == 'shopreport_type_sales_count_products':
            result = await get_count_products_sold(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        elif data == 'shopreport_type_avg_price':
            result = await get_average_price_for_product(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        elif data == 'shopreport_type_wb_commission':
            result = await get_wb_commission(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        elif data == 'shopreport_type_wb_discount':
            result = await get_discount_wb(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        elif data == 'shopreport_type_acquiring_commission':
            result = await get_commission_acquiring(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        elif data == 'shopreport_type_logistics_cost':
            result = await get_price_delivery(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        elif data == 'shopreport_type_storage_cost':
            result = await get_price_storage(api_key=api_key, dateFrom=date_from, dateTo=date_to)
            await callback_query.message.edit_text(result)
        
    except Exception as e:
        await callback_query.message.edit_text(f"Произошла ошибка при отправке отчета: {e}")
        await state.clear()
        
        
@router.message(F.text)
async def cmd_unknown_text(message):
    await message.answer("Пожалуйста, выберите команду из меню.")
    
    
@router.message(F.text.startswith("/"))
async def cmd_unknown_command(message):
    await message.answer("Пожалуйста, выберите команду из меню.")