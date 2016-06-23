from spoonybard import engine


class ShellHandler(object):
    def __init__(self, script):
        self.script = script

    def run(self, executor):
        return executor.run(self.script)


engine.plugins.register_job_handler(
    'shell', ShellHandler)
