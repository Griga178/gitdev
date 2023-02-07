class KKN():
    def __init__(self, kkn_name: str, **kwargs):
        self.name = kkn_name
        self.okpd_2 = kwargs.get("okpd_2", False)
        self.detalization = kwargs.get("detalization", False)
        self.part = kwargs.get("part", False)

        self.samples = []

    def add_sample(self, sample_object):
        self.samples.append(sample_object)
        # if kwargs.get("sources", False):
        #     self.sourses = [Source(sours_info) for sours_info in kwargs['sources']]
