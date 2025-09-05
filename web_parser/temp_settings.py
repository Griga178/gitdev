
if __name__ == '__main__':
    from services.domain import get_domain
else:
    from web_parser.services.domain import get_domain


url = 'https://www.ozon.ru/product/huawei-smartfon-pura-80-ultra-16-gb-512-gb-chernyy-smart-chasy-watch-gt-5-pro-46-mm-chernyy-2445751960/'

domain = get_domain(url)

parse_setting = {
    "www.ozon.ru": {
        "url": '', "domain": '', "date": '', "screenshot": '',
        "search_data": [
            {
            "name": "name",
            "type": "str",
            "is_expected": True,
            "rules": {
                "search_index": 0,
                "tag_name": "div",
                "recursive": True,
                "expected_amount": None,
                "attr_name": "data-widget",
                "attr_value": "webProductHeading",
                "target_point": {
                    "search_index": 0,
                    "recursive": True,
                    "expected_amount": None,
                    "tag_name": "h1",
                    "attr_name": None,
                    "attr_value": None,
                    "target_point": True
                    }
                },
            },
            {
            "name": "price",
            "type": "float",
            "is_expected": True,
            "rules": {
                "search_index": 0,
                "recursive": True,
                "expected_amount": None,
                "tag_name": "div",
                "attr_name": "data-widget",
                "attr_value": "webPrice",
                "target_point": {
                    "search_index": 0,
                    "recursive": False,
                    "expected_amount": None,
                    "tag_name": "div",
                    "attr_name": None,
                    "attr_value": None,
                    "target_point": {
                        "search_index": -1,
                        "recursive": False,
                        "expected_amount": None,
                        "tag_name": "div",
                        "attr_name": None,
                        "attr_value": None,
                        "target_point": {
                            "search_index": 0,
                            "recursive": True,
                            "expected_amount": None,
                            "tag_name": "span",
                            "attr_name": None,
                            "attr_value": None,
                            "target_point": True
                            }
                        }
                    }
                },
            },
            {
            "name": "price_vs_card",
            "type": "float",
            "is_expected": True,
            "rules": {
                "search_index": 0,
                "recursive": True,
                "expected_amount": None,
                "tag_name": "div",
                "attr_name": "data-widget",
                "attr_value": "webPrice",
                "target_point": {
                    "search_index": 0,
                    "recursive": True,
                    "expected_amount": None,
                    "tag_name": "div",
                    "attr_name": None,
                    "attr_value": None,
                    "target_point": {
                        "search_index": 0,
                        "recursive": False,
                        "expected_amount": 2,
                        "tag_name": "div",
                        "attr_name": None,
                        "attr_value": None,
                        "target_point": {
                            "search_index": 1,
                            "recursive": True,
                            "expected_amount": None,
                            "tag_name": "span",
                            "attr_name": None,
                            "attr_value": None,
                            "target_point": True
                            }
                        }
                    }
                },
            },
        ],
    },
}
