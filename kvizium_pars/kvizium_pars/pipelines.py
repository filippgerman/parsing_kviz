# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, BIGINT, String, Integer, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from .items import KviziumItem
import pymysql

pymysql.install_as_MySQLdb()
Base = declarative_base()


class KviziumDb(Base):
    __tablename__ = 'Квизиум'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(600, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


class KviziumParsPipeline(object):

    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("mysql://huston:fil@localhost/pars", encoding="utf8")
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def process_item(self, kviz_item, spider):
        # Проверка нет ли уже такой команды
        if self.session.query(KviziumDb).filter(KviziumDb.name == kviz_item['name']).count():
            self.session.query(KviziumDb).filter(KviziumDb.name == kviz_item['name']). \
                update({KviziumDb.number_game: kviz_item['number_game'], KviziumDb.points: kviz_item['points']},
                       synchronize_session=False)

        else:
            result = KviziumDb(kviz_item['name'], kviz_item['number_game'], kviz_item['points'])
            self.session.add(result)

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
