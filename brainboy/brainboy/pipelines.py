# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, BIGINT, String, Integer, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from .items import BrainboyItem
import pymysql

pymysql.install_as_MySQLdb()
Base = declarative_base()


class Data(Base):
    __tablename__ = 'BrainBoy'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(1000, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


class BrainboyPipeline(object):

    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("mysql://huston:fil@localhost/pars", encoding="utf8")
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def process_item(self, item, spider):
        # Проверка нет ли уже такой команды
        if self.session.query(Data).filter(Data.name == item['name']).count():
            self.session.query(Data).filter(Data.name == item['name']). \
                update({Data.number_game: item['number_game'], Data.points: item['points']}, synchronize_session=False)

        else:
            result = Data(item['name'], item['number_game'], item['points'])
            self.session.add(result)

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

