from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hh_rest import parse
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import exists
#import sqlite3
engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()

Vacancyskill = Table('vacancyskill', Base.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('vacancy_id', Integer, ForeignKey('vacancy.id')),
                     Column('skill_id', Integer, ForeignKey('skill.id'))
                     )

class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Integer)
    # Связь 1 - много, связь внешний ключ
    region_id = Column(Integer, ForeignKey('region.id'))
    skills = relationship("Skill", secondary=Vacancyskill, backref='skill')

    def __init__(self, name, salary, region_id):
        self.name = name
        self.salary = salary
        self.region_id = region_id

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer, nullable=True)

    # note = Column(String, nullable=True)

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f'{self.id}) {self.name}: {self.number}'

# class Association(Base):
#     __tablename__ = 'association'
#     left_id = Column(ForeignKey('vacancy_id'), primary_key=True)
#     right_id = Column(ForeignKey('skill_id'), primary_key=True)
#     count = Column(Integer)
#     child = relationship("skill")


def init():
    # Создание таблицы
    Base.metadata.create_all(engine)

    # Заполняем таблицы
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    # Регионы

    if session.query(Region).count()==0:

        session.add_all([Region('Москва', 0), Region('Питер', 78), Region('Нижний Новгород', 52)])

    # Скилы
    # session.add_all([Skill('python'), Skill('java')])

    session.commit()

# Создадим вакансии в разных регионах
# выбираем регионы
# regions = session.query(Region).all()
#
# for region in regions:
#     new_vacancy = Vacancy('какое то название', region.id)
#     session.add(new_vacancy)
#
# session.commit()
#
# # Выборка данных в регионе Москва
# # 1. id региона москва
# moscow = session.query(Region).filter(Region.name == 'Москва').first()
# print(moscow)
#
# # 2. вакансии в регионе москва
# vacancies = session.query(Vacancy).filter(Vacancy.region_id == moscow.id).all()
#
# print(len(vacancies))
# print(vacancies[0].region_id)

def search(text):
    # Заполняем таблицы
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()




    if session.query(Vacancy).filter(Vacancy.name == text).count() == 0:
        rez = parse(text)
        new_vacancy = Vacancy(text, rez['salary'], 3)

        # vac_id=session.query(Vacancy).filter(Vacancy.name == text).first().id

        for s in rez['requirements']:

            if session.query(Skill).filter(Skill.name == s[0]).count() == 0:
                ska = Skill(s[0])
                session.add(ska)
            else:
                ska = session.query(Skill).filter(Skill.name == s[0]).first()
            new_vacancy.skills.append(ska)

            # sk_id = session.query(Skill).filter(Skill.name == s[0]).first().id
            # Подключение к базе данных
            # conn = sqlite3.connect('orm.sqlite')

            # Создаем курсор
            # cursor = conn.cursor()
            # cursor.execute("insert into Vacancyskill (vacancy_id, skill_id) VALUES (?, ?)", (vac_id, sk_id))
            # insert_table=Vacancyskill.insert(vacancy_id = vac_id, skill_id=sk_id)
            # engine.execute(insert_table)
            # session.commit()
            # print(vac_id, sk_id)
        session.add(new_vacancy)

        session.commit()


def search_history():
    # Заполняем таблицы
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()
    # query1=session.query(Vacancy.name, Vacancy.salary, Region.name, Skill.name).join(Skill).\
    #     filter(Vacancy.region_id == Region.number).all()

    # query1 = session.query(Vacancy).join(Skill). \
    #     join(Region).all()
    query1 = session.query(Vacancy.name, Vacancy.salary, Region.name, Skill.name).join(Region).join(Vacancy.skills)
    # print(query1)
    return query1.all()