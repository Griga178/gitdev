import re

class Link_viewer():
    def __init__(self, links_string):
        self.links = Link_viewer.get_links(links_string)
        if self.links:
            self.domain = Link_viewer.get_domain(self.links[0])
        else:
            self.domain = False
    def get_links(links_string):
        protocols = {'http', 'https', 'ftp'} # do not work
        links = re.findall(r'[\w:/.\-?=&+%#\[\]]+', links_string)
        return links
    def get_domain(link):
        return link.split('/')[2]
