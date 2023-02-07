from typing import List

from .kkn_object import KKN
from .sample_object import Sample


class Reestr():
    def __init__(self, excel_headers: List, excel_rows: List[List]):

        self.kkns = []
        self.distribute_data(excel_headers, excel_rows)

    def distribute_data(self, excel_headers, excel_rows):
        okpd_clmn = excel_headers.index("ОКПД2") if "ОКПД2" in excel_headers else 0
        detalization_clmn = excel_headers.index("Детализация") if "Детализация" in excel_headers else 1
        kkn_name_clmn = excel_headers.index("Наименование ККН") if "Наименование ККН" in excel_headers else 2
        sample_clmn = excel_headers.index("Источник ценовой информации") if "Источник ценовой информации" in excel_headers else 5
        comp_inn_clmn = excel_headers.index("ИНН поставщика") if "ИНН поставщика" in excel_headers else 16
        comp_name_clmn = excel_headers.index("Наименование поставщика") if "Наименование поставщика" in excel_headers else 17
        links_clmn = excel_headers.index("Ссылка") if "Ссылка" in excel_headers else 18
        part_clmn = excel_headers.index("Часть") if "Часть" in excel_headers else 19

        for row in excel_rows:

            if row[kkn_name_clmn]:
                kkn_name = row[kkn_name_clmn]

                kkn_object = KKN(kkn_name,
                    okpd_2 = row[okpd_clmn],
                    detalization = row[detalization_clmn],
                    part = row[part_clmn])

                self.kkns.append(kkn_object)

            if row[sample_clmn]:
                comp_inn = row[comp_inn_clmn]
                comp_name = row[comp_name_clmn]
                links = row[links_clmn]

                sample_obj = Sample(row[sample_clmn], comp_inn, comp_name, links)

                kkn_object.add_sample(sample_obj)


    def print_rows(self):
        for kkn_obj in self.kkns:
            print(kkn_obj.part[:10], kkn_obj.okpd_2, kkn_obj.detalization, kkn_obj.name)
            for sample in kkn_obj.samples:
                print(sample.sourse.name, sample.sourse.date, sample.sourse.domain.name)

    def get_links(self):
        for links in Sample.links:
            for link in links.links:
                print(links.domain.name, link)
