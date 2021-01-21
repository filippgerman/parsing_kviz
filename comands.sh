#!/bin/bash

# Запуск Эйнштейн пати
# shellcheck disable=SC2164
cd eni/
scrapy crawl eni

## Запуск квиз-плиза
#cd ../kviz_please/
#scrapy crawl kviz_please
#
#
## Запуск Квизиума
#cd ../kvizium_pars/
#scrapy crawl kvizium
#
#
## Запуск Брэйнбой
#cd ../brainboy/
#scrapy crawl brainboy
#
## Запуск Мозгвы
#cd ../mozgva/
#scrapy crawl mozgva
#
#
## Запуск Сквиз
#cd ../squiz/
#scrapy crawl squiz


echo 'Парсинг закончен'
