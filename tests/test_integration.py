import testtools
from spoonybard.core.jobs import JobLoader
from spoonybard.core.executors import LocalExecutor

JOB_YAML="""
name: test job
steps:
  - shell: |
      #!/bin/bash

      echo I AM JOB HEAR ME RUN
"""


class LoadJobAndRunLocallyTestCase(testtools.TestCase):
	def test_local_job_run(self):
		loader = JobLoader()
		job = loader.load_yaml(JOB_YAML)
		executor = LocalExecutor()
		job.execute(executor)
		self.assertTrue(job.success())
		self.assertEqual(
			[b'I AM JOB HEAR ME RUN\n'],
			executor.get_log())
