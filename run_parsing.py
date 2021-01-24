import time
import subprocess

NAME_KVIZ = ('brainboy', 'eni', 'kviz_please', 'kvizium', 'mozgva', 'squiz')

time.sleep(30)
for name in NAME_KVIZ:
    subprocess.call(
        [f'scrapy crawl {name}'], shell=True, stdout=subprocess.PIPE, cwd=f'{name}'
    )
