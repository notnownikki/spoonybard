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
      for i in 1 2 3 4 5 6 7 8 9 0; do sleep 1; echo $i; done
"""

cfg = {}
cfg['hostname'] = '192.168.0.103'
cfg['username'] = 'nicola'
cfg['key'] = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAqtxvx4dSCKKfPufKt0O3gDb+MASZT/isyEo+7sypcdFQa9uu
GtMSyKp9lI+6d240/+cV5bcHrHnWRCbjAflKg6Ay5KexCEAIhicTmTprJ9YT4ub9
JpBfKG3K3Mtr4TI03p6xbgpJdRWZt9sKfYAjgIvU/yAHMl0XfMWfS2J3UyPmv3g8
zbM14Y7cwA5TRo0t8AsBBOK6HkCDKHmGVb1RRdofrEkiMijVSWf827MsF9dp+ng6
P3IGiq/Hn5DsKb0H4oQmv9NRpIaufOz+b3+0Rvti6oR3XGT8GB7IXtCtdm60Sjv3
6DPrO0aP2l9IVhYt3CWm4p3NTnuHImqeZ7PpVwIDAQABAoIBAEXvbo1kFS7VqYrt
A2uZ+x0u5UIwT7SNG+Prh/DksqKUw28yfwQZy0F5j2dkoTVLVcQ9CRh6n1h4kjxZ
Emf3awmPY+V1wh+XXiXTDtGUONIYbRFd7NaBF4IL1pIjbWfCziMlH4jkCwcyrTW1
IYkXDvEJy0gWCvwRYJDAryADEMZlazCrbMR6oB13o6bMAAxap8uuXBxavXH23+6D
zPqwuOoME95YF6fY/X5O/oAqlVaxIJ5x++kPF0Kadk4G0FSaFitO1HpSuqQSrD6u
Yzpb/U4DoPHFAEdRuvEFx5o7ErIcHjMt0CwnyIMGkUp1c3Spg12WripnlLv/KvAi
HzhpGPECgYEA2Yd8B4r60LoG/2Zxda00+z6MinPZt2N7f2DpPHu6/iijRToEbHhM
l+OTHli9CWfHlJ43xI2NCm512cQZmVzOOcfwMwGT75sm1jnylP6HbrOeGwPDfsQk
7Sfri17dvbn9tx1mRHRa+dCZeC7HZVj1yvBxduumnLha7QLL9nCO0B8CgYEAyRQT
yRQKQwHpyaYAPeqgwSwRLzRGgBMXEcG+p6OJ31iaP3pGj6/VacCaY7JkG6u3FkTH
axAuwHK/su6b4Wv1gbcWsqf4siBN1V3bEBlXQBGwrjO//Nak/Hb5S3LEmEAmlg56
L8OrFymUjbO3lygGK6xiJUjvi1QZEq5+EmDJX8kCgYBUarCmWLf3MoouqTnUug/6
hI6T2FugQJoXl6tLzpSFt42M+vPmiFTpCOb5+uP5d23Lbg8kVu5qIu3XQbPRgWOC
puW/VZhsfuB2eGx8h75VJp1vzGkck8/kvP46yujwjPI6Es2yORlpIxu7uSOmX/ya
8e6GgPLalOysV86BZ7L0bwKBgDe2Nl0qDkXOi+Xw9nQxQ+UBvqkjhL0LjQLAeYCd
ESAuvl4EFPTOtQSd9qjUzmPUSeADonUJgMqVgIOlFM96SAVuov1RCNjhlm8dmAp3
2vLHc/pwICt/lSrWE/BRliLQ81/0FuqQ/iBmxuAUATQCRONo2bCW6rfhzyib7BZP
drvxAoGAObl6Pbip/YlYvnxIs+JtI/pYA19QmVubfAiw9KTaurOJ/Sv6KvZnPXKo
4cHPyFsDWEZFZrRUoI0BepZ3rbunJ4Gs/VegNhobb1rEGu1UXY8RjfiLnjSghv6N
VuK+9pS5kP8KKaWfRKR608v8D3QBOzhTlo49wByix2XxZRq+AOw=
-----END RSA PRIVATE KEY-----"""

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