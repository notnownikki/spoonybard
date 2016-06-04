class Job(object):
    def run(self):
        pass


class JobFactory(object):
    def create(self):
        return Job()
