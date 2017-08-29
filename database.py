#!/usr/bin/python3
import sqlite3
import datetime
import settings


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_sql(name):
    name += '.sql' if not name.endswith('.sql') else ''
    try:
        with open(settings.SQL_PATH + '/' + name, 'r') as f:
            return ''.join(f.readlines())
    except Exception as e:
        return None


def create_database():
    CREATE_DATABASE = get_sql('create_database')
    try:
        with sqlite3.connect(settings.DB_NAME) as db:
            c = db.cursor()
            for create_table in CREATE_DATABASE.split(';'):
                c.execute(create_table)
            c.close()
            db.commit()
        # Заполнение примерными данными
        add_region('Краснодарский край', ['Краснодар', 'Кропоткин', 'Славянск'])
        add_region('Ростовская область', ['Ростов', 'Шахты', 'Батайск'])
        add_region('Ставропольский край', ['Ставрополь', 'Пятигорск', 'Кисловодск'])
        add_region('Марий Эл', ['Йошкар-Ола', 'Волжск', 'Звенигово', 'Козьмодемьянск'])
    except Exception as e:
        return e


def get_regions():
    """Получить список регионов
    """
    regions = None
    with sqlite3.connect(settings.DB_NAME) as db:
        SELECT_REGIONS = get_sql('select_regions')
        db.row_factory = dict_factory
        c = db.cursor()
        c.execute(SELECT_REGIONS)
        regions = c.fetchall()
        c.close()
    for r in regions:
        yield r


def get_villages(region_id=None):
    """Получить список регионов для region_id
    """
    if not isinstance(region_id, (int,)):
        raise

    with sqlite3.connect(settings.DB_NAME) as db:
        SELECT_VILLAGES = get_sql('select_villages')
        db.row_factory = dict_factory
        c = db.cursor()
        c.execute(SELECT_VILLAGES, (region_id,))
        villages = c.fetchall()
        c.close()
    for v in villages:
        yield v


def select_user(email):
    """Выбрать пользователя по email
    """
    pass


def add_villages(region_id, villages):
    if not isinstance(villages, (list,)):
        raise

    # print('add_villages', villages)
    try:
        with sqlite3.connect(settings.DB_NAME) as db:
            INSERT_VILLAGES = get_sql('insert_villages')
            c = db.cursor()
            c.executemany(INSERT_VILLAGES, [(region_id, village) for village in villages])
            c.close()
            db.commit()
    except Exception as e:
        print('add_village exception:', e)


def add_region(region_name, villages=[]):
    """Добавить регион и населённые пункты
    """
    if not isinstance(region_name, (str,)) and region_name == '':
        raise

    try:
        with sqlite3.connect(settings.DB_NAME) as db:
            INSERT_REGION = get_sql('insert_region')
            # print(INSERT_REGION, region_name, villages)
            c = db.cursor()
            c.execute(INSERT_REGION, (region_name,))
            region_id = c.lastrowid
            # print(region_name, region_id)
            c.close()
            db.commit()
        add_villages(region_id, villages)
        return region_id
    except Exception as e:
        print('add_region exception:', e)
        return e


def add_comment(comment):
    """
    comment: dict('text', user_id, region_id, village_id, email, phone)
    """
    pass


def get_comments():
    with sqlite3.connect(settings.DB_NAME) as db:
        try:
            db.row_factory = dict_factory
            c = db.cursor()
            c.execute(get_sql('select_comments'))
            comments = c.fetchall()
            c.close()
            for c in comments:
                yield c
        except Exception as e:
            print('get_comments:', e)


def insert_comment(comment_data):
    with sqlite3.connect(settings.DB_NAME) as db:
        try:
            c = db.cursor()
            c.execute(get_sql('insert_comment'), comment_data)
            c.close()
            db.commit()
        except Exception as e:
            db.rollback()
            print('insert_comment:', e)


def delete_comment(comment_id):
    # print('delete_comment:', comment_id)
    with sqlite3.connect(settings.DB_NAME) as db:
        try:
            c = db.cursor()
            c.execute(get_sql('delete_comment'), comment_id)
            c.close()
            db.commit()
        except Exception as e:
            db.rollback()
            print('delete_comment:', e)


def get_stat():
    with sqlite3.connect(settings.DB_NAME) as db:
        try:
            db.row_factory = dict_factory
            c = db.cursor()
            c.execute(get_sql('select_stat'), {'stat_count': settings.STAT_COUNT})
            comments = c.fetchall()
            c.close()
            for c in comments:
                yield c
        except Exception as e:
            print('get_stat:', e)


def get_stat_region(select_args):
    select_args.update(stat_count=settings.STAT_COUNT)
    with sqlite3.connect(settings.DB_NAME) as db:
        try:
            db.row_factory = dict_factory
            c = db.cursor()
            c.execute(get_sql('select_stat_region'), select_args)
            comments = c.fetchall()
            c.close()
            for c in comments:
                yield c
        except Exception as e:
            print('get_stat_region:', e)


if __name__ == '__main__':
    create_database()
    for c in get_stat():
        print(c)
        for v in get_stat_region({'region_id': c['region_id']}):
            print('\t', v)
