from .source_object import Source
from .link_objects import Links
from .domain_object import Domain

class Sample():
    """ Прототип ккн / экземпляр из источника ценовой инфы
    """
    sources = []
    links = []
    def __init__(self, source_cell: str, comp_inn: str, comp_name: str, links: str):
        self.links = Links(links)
        Sample.links.append(self.links)

        if self.links.domain:
            domain_obj = Domain(self.links.domain)
            self.links.domain = domain_obj
            
        for source_obj in Sample.sources:
            if source_obj.company.inn == comp_inn:
                self.sourse = source_obj
                break
        else:
            self.sourse = Source(source_cell, comp_inn, comp_name, domain_obj)
            Sample.sources.append(self.sourse)
