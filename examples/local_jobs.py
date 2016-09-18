import threading
import time
import copy
from spoonybard.core.executors import SSHExecutor, LocalExecutor
from spoonybard.core.jobs import JobLoader

JOB_YAML  = """
name: test job
steps:
  - shell: |
      #!/bin/bash
      echo Running remotely
  - shell: |
      #!/bin/bash
      echo hi >> ~/thing
"""

cfg = {}

def run_job(job, executor):
	job.execute(executor)

loader = JobLoader()
job = loader.load_yaml(JOB_YAML)
print("Starting up")
for y in range(0,500):
	j = copy.deepcopy(job)
	remote = LocalExecutor(cfg)
	thread = threading.Thread(target=run_job, args=(j, remote,))
	thread.start()
print("Waiting for jobs")
