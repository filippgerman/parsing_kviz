import time
import subprocess

NAME_KVIZ = ('brainboy', 'eni', 'kviz_please', 'kvizium', 'mozgva', 'squiz')

time.sleep(60)
while True:
    for name in NAME_KVIZ:
        subprocess.call(
            [f'scrapy crawl {name}'], shell=True, stdout=subprocess.PIPE, cwd=f'{name}'
        )
    time.sleep(43200)  # сапыает на 12 часов.
