from spoonybard import plugins


class ShellHandler(object):
	def __init__(self, script):
		self.script = script
	
	def run(self, executor):
		return executor.run(self.script)


plugins.register_job_handler(
	'shell', 'spoonybard.core.handlers.ShellHandler')
