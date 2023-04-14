import re
from work_data_base import Link_object

class Link():

    def __init__(self, link):
        self.link = link
        self.object = Link_object(link)
        self.define_domain()

    def define_links(str_links):
        # links = re.findall(r'[\w:/.\-?=&+%#\[\]]+', str_links)
        protocols = {'http', 'https', 'ftp'}
        links = re.findall(r'[\w:/.\-?=&+%#\[\]]+', str_links)
        return links

    def define_domain(self):
        # '*//domain/*'
        self.domain = self.link.split('/')[2]
