import os
import subprocess

os.chdir('brainboy')
subprocess.call(
    ['scrapy', 'crawl', 'brainboy']
)
#
# os.chdir('../eni')
# subprocess.call(
#     ['scrapy', 'crawl', 'eni']
# )
#
# os.chdir('../kviz_please')
# subprocess.call(
#     ['scrapy', 'crawl', 'kviz_please']
# )
#
#
# os.chdir('../kvizium_pars')
# subprocess.call(
#     ['scrapy', 'crawl', 'kvizium']
# )
#
#
# os.chdir('../mozgva')
# subprocess.call(
#     ['scrapy', 'crawl', 'mozgva']
# )
#
#
# os.chdir('../squiz')
# subprocess.call(
#     ['scrapy', 'crawl', 'squiz']
# )
