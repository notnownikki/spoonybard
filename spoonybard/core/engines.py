class BardCore(object):
    def __init__(self):
        self.plugins = None
        self.config = None
        self.webserver = None

    # --------------------------------
    # Thread control

    def start_webserver(self):
        pass

    def stop_webserver(self):
        pass

    def start_sshserver(self):
        pass

    def stop_sshserver(self):
        pass

    def start_processing(self):
        pass

    def stop_processing(self):
        pass
