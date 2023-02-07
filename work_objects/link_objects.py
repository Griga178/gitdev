import re

class Links():

    def __init__(self, link_row):
        self.source = False
        self.define_link(link_row)
        if self.links:
            self.define_domain()

    def define_link(self, link_row):
        self.links = re.findall(r'[\w:/.\-?=&+%#\[\]]+', link_row)

    def define_domain(self):
        '''    Определение домена из списка ссылок    '''
        domains = set()
        protocols = {'http', 'https', 'ftp'}
        for link in self.links:
            split_link = link.split("/")
            current_protocol = split_link[0][:-1]
            if current_protocol in protocols:
                domains.add(split_link[2])

        if len(domains) != 1:
            self.domain = False
        else:
            self.domain = ''.join(domains)

# class Link():
#
#     def __init__(self, link):
#         self.link = link
