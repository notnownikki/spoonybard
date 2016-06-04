import testtools
from spoonybard.core.jobs import JobLoader, Job
from spoonybard import plugins

JOB_SCRIPT = "ls /"

JOB_YAML = """
name: test_job
steps:
  - script: |
      %s""" % JOB_SCRIPT

JOB_MULTISTEP_YAML = """
name: test_job
steps:
  - fail: Dummy plugin that will fail
  - script: |
      %s""" % JOB_SCRIPT

class JobLoaderTestCase(testtools.TestCase):
    def test_job_from_yaml_returns_job(self):
        loader = JobLoader()
        job = loader.load_yaml(JOB_YAML)
        self.assertEqual(
            type(job),
            Job)

    def test_job_from_yaml_has_plugins_in_steps(self):
        loader = JobLoader()
        job = loader.load_yaml(JOB_YAML)
        steps = job.steps
        self.assertEqual(
            JobLoaderTestPlugin,
            type(steps[0]))

    def test_job_from_yaml_has_plugin_args_from_yaml(self):
        loader = JobLoader()
        job = loader.load_yaml(JOB_YAML)
        steps = job.steps
        self.assertEqual(
            JOB_SCRIPT,
            steps[0].args)

    def test_job_gets_all_steps(self):
        loader = JobLoader()
        job = loader.load_yaml(JOB_MULTISTEP_YAML)
        steps = job.steps
        self.assertEqual(
            2,
            len(job.steps))
        self.assertEqual(
            type(steps[0]),
            FailingJobLoaderTestPlugin)
        self.assertEqual(
            type(steps[1]),
            JobLoaderTestPlugin)


class JobTestCase(testtools.TestCase):
    def test_job_runs_steps_on_executor(self):
        loader = JobLoader()
        executor = DummyExecutor()
        job = loader.load_yaml(JOB_YAML)
        job.execute(executor)
        for step in job.steps:
            self.assertEqual(
                executor,
                step.executor_used)

    def test_job_success_or_fail(self):
        loader = JobLoader()
        executor = DummyExecutor()
        job = loader.load_yaml(JOB_YAML)
        job.execute(executor)
        self.assertEqual(
            True,
            job.success())

    def test_job_success_or_fail_multistep(self):
        loader = JobLoader()
        executor = DummyExecutor()
        job = loader.load_yaml(JOB_MULTISTEP_YAML)
        job.execute(executor)
        self.assertEqual(
            False,
            job.success())


# ============================================
# Dummy plugins and executors for use in tests

class DummyExecutor(object):
    def __init__(self):
        self.script_executed = False

    def run(self, script):
        self.script_executed = script


class JobLoaderTestPlugin(object):
    def __init__(self, args):
        self.args = args
        self.executor_used = False
        self._exit_code = 0

    def run(self, executor):
        self.executor_used = executor
        return self._exit_code


class FailingJobLoaderTestPlugin(JobLoaderTestPlugin):
    def __init__(self, args):
        super(FailingJobLoaderTestPlugin, self).__init__(args)
        self._exit_code = 127


plugins.register_job_handler(
    'script', 'tests.test_jobs.JobLoaderTestPlugin')
plugins.register_job_handler(
    'fail', 'tests.test_jobs.FailingJobLoaderTestPlugin')
