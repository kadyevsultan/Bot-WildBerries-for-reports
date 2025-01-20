import aiohttp

shop_report_url = 'https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod'


#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ ОБЩЕЙ СУММЫ ПРОДАЖ

async def get_sales_sum(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key,  # Ваш API-ключ
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_price = 0
                            currency_name = 'руб.'

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    finished_price = sale.get('ppvz_for_pay', 0)
                                    total_price += finished_price
                                    currency_name = sale.get('currency_name', 'руб.')

                            return f'Сумма продаж за указанный период составило: {total_price} {currency_name}'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"
            



#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ КОМИССИИ WB ЗА УКАЗАННЫЙ ПЕРИОД

async def get_wb_commission(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key, 
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_commission_wb = 0
                            currency_name = 'руб.'

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    finished_price = sale.get('ppvz_for_pay', 0)
                                    commission_wb_percent = sale.get('commission_percent', 0)
                                    total_commission_wb = (finished_price * commission_wb_percent) / 100
                                    currency_name = sale.get('currency_name', 'руб.')

                            return f'Комиссия WildBerries за указанный период составило: {total_commission_wb} {currency_name}'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"



#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ СКИДКИ WB

async def get_discount_wb(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_discount_wb = 0
                            currency_name = 'руб.'

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    finished_price = sale.get('ppvz_for_pay', 0)
                                    discount_wb = sale.get('sale_percent', 0)
                                    total_discount_wb += (finished_price * discount_wb) / 100
                                    currency_name = sale.get('currency_name', 'руб.')

                            return f'Скидка WildBerries за указанный период составило: {total_discount_wb} {currency_name}'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"



#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ КОМИССИИ ЭКВАЙРИНГА

async def get_commission_acquiring(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key,  
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_commission_acquiring = 0
                            currency_name = 'руб.'

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    finished_price = sale.get('ppvz_for_pay', 0)
                                    commission_acquiring = sale.get('acquiring_percent', 0)
                                    total_commission_acquiring += (finished_price * commission_acquiring) / 100
                                    currency_name = sale.get('currency_name', 'руб.')

                            return f'Комиссия эквайринга за указанный период составило: {total_commission_acquiring} {currency_name}'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"


#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ СТОИМОСТИ ЛОГИСТИКИ(ДОСТАВКА, ПЕРЕВОЗКА)

async def get_price_delivery(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key,  
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_price_delivery = 0
                            currency_name = 'руб.'

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    count_delivery = sale.get('delivery_amount', 0)
                                    price_delivery = sale.get('delivery_rub', 0)
                                    total_price_delivery += price_delivery
                                    currency_name = sale.get('currency_name', 'руб.')
                                    
                            return f'Стоимость логистики за указанный период составило: {total_price_delivery} {currency_name}, Всего доставок было {count_delivery}.'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"


#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ СТОИМОСТИ ХРАНЕНИЯ(В ПУНКТАХ ВЫДАЧИ)

async def get_price_storage(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key,  
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_price_storage = 0
                            currency_name = 'руб.'

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    price_storage = sale.get('storage_fee', 0)
                                    total_price_storage += price_storage
                                    currency_name = sale.get('currency_name', 'руб.')
                                    
                            return f'Стоимость хранения за указанный период составило: {total_price_storage} {currency_name}'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"


#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ КОЛИЧЕСТВА ПРОДАННЫЙ ТОВАРОВ

async def get_count_products_sold(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key, 
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_count_products = 0

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    finished_count = sale.get('quantity', 0)
                                    total_count_products += finished_count

                            return f'Количество проданных товаров за указанный период составило: {total_count_products}'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"


#ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ СРЕДНЕЙ СТОИМОСТИ 1 ПРОДАЖИ

async def get_average_price_for_product(api_key, dateFrom, dateTo, url=shop_report_url):
    # Заголовки запроса
    headers = {
        "Authorization": api_key, 
        "Content-Type": "application/json"
    }

    # Параметры запроса (например, отчет за месяц)
    params = {
        "dateFrom": dateFrom,  # Начало периода
        "dateTo": dateTo,  # Конец периода
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    try:
                        sales_data = await response.json()

                        if sales_data:
                            total_price = 0
                            total_sales = 0

                            for sale in sales_data:
                                if sale.get('supplier_oper_name') == "Продажа":
                                    finished_price = sale.get('ppvz_for_pay', 0)
                                    total_price += finished_price
                                    total_sales += 1

                            if total_sales >= 1:
                                average_price = total_price / total_sales
                                return f'Средняя стоимость одной продажи за указанный период составила: {round(average_price, 2)} {sale.get("currency_name", "руб.")}'
                            else:
                                return 'Не было продаж за указанный период.'
                        else:
                            return 'Не было продаж за указанный период.'
                    except ValueError:
                        return 'Ошибка обработки данных: не удалось отправить ответ в JSON.'
                else:
                    error_text = await response.text()
                    return f"Ошибка {response.status}: {error_text}"
        except aiohttp.ClientError as e:
            return f"Ошибка запроса: {str(e)}"
