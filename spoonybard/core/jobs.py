import yaml
from spoonybard import plugins


class Job(object):
    def __init__(self):
        self.steps = []
        self._exit_code = None

    def execute(self, executor):
        executor.open()
        for step in self.steps:
            self._exit_code = self._exit_code or step.run(executor)
        executor.close()

    def success(self):
        return self._exit_code == 0


class JobLoader(object):
    """
    Takes a yaml file and returns a job with all plugins loaded
    """
    def load_yaml(self, job_yaml):
        obj = yaml.load(job_yaml)
        job_steps = []
        for step in obj['steps']:
            handler_name = list(step.keys())[0]
            plugin = plugins.get_job_handler(handler_name)
            job_steps.append(plugin(step[handler_name]))
        job = Job()
        job.steps = job_steps
        return job
