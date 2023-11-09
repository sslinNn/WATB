import pandas as pd
import sqlalchemy as db
from collections import Counter
from db_control import get_connetion_with_db
from sqlalchemy import inspect, create_engine, insert
from dotenv import load_dotenv
from bot.schedule.selected_schedule_parser import parse_all_subjects, parse_subject_teacher
from bot.schedule.all_schedule_parser import getScheduleNHTK_teachers, getScheduleNHTK_groups
import datetime
import os


def create_table():
    engine = get_connetion_with_db()
    connection = engine.connect()
    metadata = db.MetaData()

    table = db.Table('schedule', metadata,
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('subject_id', db.Integer),
                     db.Column('teacher_id', db.Integer),
                     db.Column('group_id', db.Integer),
                     db.Column('lesson_number_id', db.Integer),
                     db.Column('time', db.Time),
                     db.Column('date', db.Date),)
    metadata.create_all(engine)


def insert_into_table():
    subjects = parse_subject_teacher()
    engine = get_connetion_with_db()
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('teacher_subject', metadata, autoload_with=engine)
    table_t = db.Table('teachers', metadata, autoload_with=engine)
    table_s = db.Table('subjects', metadata, autoload_with=engine)
    for teach, less in subjects.items():
        t = teach.split('/')[0]
        select_stmt_t = db.select(table_t.c.id).where(table_t.c.name == t)
        result_t = connection.execute(select_stmt_t)
        t_id = result_t.fetchone()
        select_stmt_s = db.select(table_s.c.id).where(table_s.c.title == less)
        result_s = connection.execute(select_stmt_s)
        s_id = result_s.fetchone()
        connection.execute(table.insert().values([{'subject_id': s_id[0], 'teacher_id': t_id[0]}]))
    connection.commit()
    connection.close()


def check_and_insert_teacher_subject():
    table_name = 'teacher_subject'
    engine = get_connetion_with_db()
    connection = engine.connect()
    metadata = db.MetaData()
    subjects = parse_subject_teacher()
    table = db.Table('teacher_subject', metadata, autoload_with=engine)
    table_t = db.Table('teachers', metadata, autoload_with=engine)
    table_s = db.Table('subjects', metadata, autoload_with=engine)
    for teach, less in subjects.items():
        select_stmt_s = db.select(table_s.c.id).where(table.c.title == less)
        result_s = connection.execute(select_stmt_s)
        row_s = result_s.fetchone()
        select_stmt_t = db.select(table_t.c.id).where(table.c.title == teach)
        result_t = connection.execute(select_stmt_t)
        row_t = result_t.fetchone()
        select_stmt = db.select(table).where(table.c.subject_id == row_s and table.c.teacher_id == row_t)
        result = connection.execute(select_stmt)
        row = result_s.fetchone()
        if not row:
            connection.execute(table.insert().values([{'subject_id': row_s, 'teacher_id': row_t}]))
            connection.commit()
        connection.close()


def check_and_insert_subjects():
    table_name = 'subjects'
    engine = get_connetion_with_db()
    connection = engine.connect()
    metadata = db.MetaData()
    subjects = parse_all_subjects()
    table = db.Table(table_name, metadata, autoload_with=engine)
    for s in subjects:
        select_stmt = db.select(table).where(table.c.title == s)
        result = connection.execute(select_stmt)
        row = result.fetchone()
        if not row:
            connection.execute(table.insert().values([{'title': s}]))
            connection.commit()
        connection.close()


def check_and_insert_teachers():
    table_name = 'teachers'
    engine = get_connetion_with_db()
    connection = engine.connect()
    metadata = db.MetaData()
    df = getScheduleNHTK_teachers()
    peoples = list(df['Name'])
    table = db.Table(table_name, metadata, autoload_with=engine)
    for p in peoples:
        select_stmt = db.select(table).where(table.c.name == p)
        result = connection.execute(select_stmt)
        row = result.fetchone()
        if not row:
            connection.execute(table.insert().values([{'name': p}]))
            connection.commit()
    connection.close()


def check_and_insert_groups():
    table_name = 'groups'
    engine = get_connetion_with_db()
    connection = engine.connect()
    metadata = db.MetaData()
    df = getScheduleNHTK_groups()
    groups = list(df['GroupName'])
    groups.append('66.66.66')
    table = db.Table(table_name, metadata, autoload_with=engine)
    for g in groups:
        select_stmt = db.select(table).where(table.c.title == g)
        result = connection.execute(select_stmt)
        row = result.fetchone()
        if not row:
            connection.execute(table.insert().values([{'title': g}]))
            connection.commit()
    connection.close()


def delete():
    engine = get_connetion_with_db()
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('teachers', metadata, autoload_with=engine)
    del_q = db.delete(table).where(table.c.id >= 0)
    connection.execute(del_q)
    connection.commit()





if __name__ == "__main__":
    insert_into_table()

