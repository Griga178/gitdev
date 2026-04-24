import asyncio
import aiohttp
from typing import List, Tuple, Dict

class EisFetcher():
    """
        e.fetch_all([param,...])
        принимает список из param
        param = {'date': str, 'min': float, 'max': float}
        выдает список кортежей
        (param:dict, html_page: str)
    """
    def __init__(self):
        # постоянные параметры
        self.url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            }
        self.BASE_PARAMS = {
            'fz44': 'on',
            'customerPlace': '47000000000%2C78000000000', # СПБ, Лен. обл
            'recordsPerPage': '500',     # 10,20, 50, 100, 500
            # 'sortBy': 'PUBLISH_DATE', # по дате размещения
            'sortBy': 'PRICE',
            'sortDirection': 'true', # от старых к новым
            'af': 'on',     # Подача заявок
            'ca': 'on',     # Работа комиссии
            'pc': 'on',     # Закупка завершена
            'pa': 'on',     # Закупка отменена
        }
        # ограничение по одновременным запросам
        self.semaphore_limit = 10

        variable_param_example = {
            'publishDateFrom': '13.04.2026',
            'publishDateTo': '14.04.2026',
            'priceFromGeneral': '',
            'priceToGeneral': '',
            'pageNumber': '1'
        }
    async def _get_semaphore(self):
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(20)   # 20 одновременных запросов
        return self._semaphore

    async def eis_fetch_page(self, params: Dict, semaphore: asyncio.Semaphore) -> Tuple[Dict, str]:
        """Асинхронно загружает страницу с указанными параметрами."""
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, params=params, headers=self.HEADERS) as resp:
                    if resp.status != 200:
                        params['resp_status'] = resp.status
                        return params, None
                    html = await resp.text()
                    return params, html

    async def _fetch_many(self, params_list: List[Dict]) -> List[Tuple[Dict, str]]:
        """Запускает несколько асинхронных запросов параллельно."""
        semaphore = asyncio.Semaphore(self.semaphore_limit)
        tasks = [self.eis_fetch_page(params, semaphore) for params in params_list]
        return await asyncio.gather(*tasks)

    def fetch_all(self, items: List[Dict], chunk_size: int = 100) -> List[Tuple[Dict, str]]:
        """Синхронная обёртка для вызова из не-асинхронного кода."""
        params_list = self.prepare_params(items)
        # return asyncio.run(self._fetch_many(params_list))
        all_results = []
        for i in range(0, len(params_list), chunk_size):
            chunk = params_list[i:i+chunk_size]
            results = asyncio.run(self._fetch_many(chunk))
            all_results.extend(results)
        return all_results

    def prepare_params(self, items: List[Dict]) -> List[Dict]:
        """
        Принимает список словарей с ключами 'date', 'min', 'max'.
        Возвращает список полных параметров для каждого запроса.
        """
        params_list = []
        for item in items:
            params = self.BASE_PARAMS.copy()
            params['publishDateFrom'] = item['publishDateFrom']
            params['publishDateTo'] = item.get('publishDateTo', '')
            params['priceFromGeneral'] = item.get('priceFromGeneral', '')
            params['priceToGeneral'] = item.get('priceToGeneral', '')
            params['pageNumber'] = item.get('pageNumber', '1')
            params_list.append(params)
        return params_list

# Пример использования
if __name__ == '__main__':
    e_fetcher = EisFetcher()
    items = [
        {'date': '2026-04-20'},
        {'date': '2026-04-21', 'min': '', 'max': ''},
        # {'date': '2026-04-19', 'min': '1000', 'max': '5000'}
    ]
    # print(e_fetcher.prepare_params(items))
    # quit()
    results = e_fetcher.fetch_all(items)
    for params, html in results:
        print(f"Дата: {params['publishDateFrom']}, Размер HTML: {len(html)}")
