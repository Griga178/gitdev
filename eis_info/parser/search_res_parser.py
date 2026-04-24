from bs4 import BeautifulSoup
import re

def parse_contract_reestr(html):
    """
    Извлекает данные о контрактах из результата parse_contract_reestr.

    Args:
        текст - формат html

    Returns:
        Dict{'amount': int, 'data': contracts, 'max': max_price, 'min': min_price}

        contracts = list[dict]: список контрактов, каждый с полями:
            - contract_type: тип закупки
            - contract_number: номер закупки
            - object: объект закупки
            - customer: заказчик
            - customer_id: id в системе eis
            - start_price: начальная цена (число или строка)
            - published_date: дата размещения
            - updated_date: дата обновления
            - submission_deadline: окончание подачи заявок
            - order_stage: Этап закупки
    """
    soup = BeautifulSoup(html, 'html.parser')
    # блок - кол-во элементов-контрактов
    contract_amount_block = soup.find("div", {"class": "search-results__total"})
    if contract_amount_block:
        contract_amount = re.sub(r'[^0-9]', '', contract_amount_block.get_text(strip=True))
        contract_amount = int(contract_amount)
    else:
        return {'amount': None, 'data': None, 'max': None, 'min': None}

    # список блоков с инфой по контракту
    elems = soup.find_all("div", {"class": "search-registry-entry-block"})

    contracts = []
    max_price = 0
    min_price = None
    for elem in elems:
        # тип закупки (44 / 223 и прочее)
        contract_type_elem = elem.find('div', class_='registry-entry__header-top__title')
        if contract_type_elem:
            contract_type_str = contract_type_elem.get_text()
            contract_type = re.sub(r'\s+', ' ', contract_type_str).strip()
        else:
            contract_type = None

        # Номер закупки
        reg_number_elem = elem.find('div', class_='registry-entry__header-mid__number')
        if reg_number_elem:
            contract_number = re.sub(r'[^0-9]', '', reg_number_elem.get_text(strip=True))
        else:
            contract_number = None

        # Этап закупки
        order_stage_elem = elem.find('div', class_='registry-entry__header-mid__title text-normal')
        if order_stage_elem:
            order_stage = order_stage_elem.get_text(strip=True)
        else:
            order_stage = None

        # Объект закупки
        object_elem = elem.find('div', class_='registry-entry__body-block')
        object_text = None
        if object_elem and 'Объект закупки' in object_elem.get_text():
            object_value = object_elem.find('div', class_='registry-entry__body-value')
            if object_value:
                object_text = object_value.get_text(strip=True) if object_value else None

        # Заказчик
        customer_text = None
        customer_id = None
        customer_block = elem.find('div', class_='registry-entry__body-href')
        if customer_block:
            customer_link = customer_block.find('a')
            if customer_link:
                customer_text = customer_link.get_text(strip=True)
                # Извлекаем href
                href = customer_link.get('href', '')
                if href:
                    # Ищем параметр agencyId=... (цифры после agencyId=) -> v2
                    # reg_ex = r'Id=(\d+)'
                    reg_ex = r'(?:Id|organizationCode)=(\d+)'
                    match = re.search(reg_ex, href)
                    customer_id = match.group(1) if match else href
            else:
                customer_text = customer_block.get_text(strip=True)

        # Начальная цена
        price_elem = elem.find('div', class_='price-block__value')
        if price_elem:
            price_text = re.sub(r'[^0-9,-]', '', price_elem.get_text())

            price_clean = price_text.replace(',', '.')
            try:
                start_price = float(price_clean)
                # контракты отсортированы по цене
                max_price = start_price
                min_price = start_price if not min_price else min_price
            except ValueError:
                start_price = price_text
        else:
            start_price = None

        # Даты
        submission_deadline = None
        updated_date = None
        published_date = None
        data_block = elem.find('div', class_='data-block')
        if data_block:
            # Ищем все заголовки
            titles = data_block.find_all('div', class_='data-block__title')
            for title in titles:
                title_text = title.get_text(strip=True)
                # После заголовка обычно идёт div с классом data-block__value
                # (может быть следующим sibling или внутри того же родителя)
                value_elem = title.find_next_sibling('div', class_='data-block__value')
                if not value_elem:
                    # Если не нашли как sibling, ищем внутри родителя
                    value_elem = title.parent.find('div', class_='data-block__value')
                if not value_elem:
                    continue
                value = value_elem.get_text(strip=True)

                if 'Размещено' in title_text:
                    published_date = value
                elif 'Обновлено' in title_text:
                    updated_date = value
                elif 'Окончание подачи заявок' in title_text:
                    submission_deadline = value

        contracts.append({
            'contract_type': contract_type,
            'contract_number': contract_number,
            'object': object_text,
            'customer': customer_text,
            'customer_id': customer_id,
            'start_price': start_price,
            'published_date': published_date,
            'updated_date': updated_date,
            'submission_deadline': submission_deadline,
            'order_stage': order_stage
        })

    return {'amount': contract_amount, 'data': contracts, 'max': max_price, 'min': min_price}
