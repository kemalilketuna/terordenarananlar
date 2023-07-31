from models import *


def insert_person_to_db(name, surname, birth_year, birth_place):
    person = Person(
        name=name, surname=surname, birth_year=birth_year, birth_place=birth_place
    )
    session.add(person)
    session.commit()
    return person


def insert_category_to_db(category_name):
    category = Category(category_name=category_name)
    session.add(category)
    session.commit()
    return category


def insert_t_o_to_db(t_o_name):
    t_o = T_o(t_o_name=t_o_name)
    session.add(t_o)
    session.commit()
    return t_o


def insert_record_to_db(person_id, t_o_id, category_id, is_active):
    record = Record(
        id=person_id, t_o_id=t_o_id, category_id=category_id, is_active=is_active
    )
    session.add(record)
    session.commit()
    return record


def insert_picture_to_db(person_id, picture_url):
    picture = Picture(id=person_id, picture_url=picture_url)
    session.add(picture)
    session.commit()
    return picture


def get_person_id(name, surname, birth_year, birth_place):
    person = (
        session.query(Person)
        .filter_by(
            name=name, surname=surname, birth_year=birth_year, birth_place=birth_place
        )
        .first()
    )
    if person is None:
        person = insert_person_to_db(name, surname, birth_year, birth_place)
    return person.id


def get_category_id(category_name):
    category = session.query(Category).filter_by(category_name=category_name).first()
    if category is None:
        category = insert_category_to_db(category_name)
    return category.category_id


def get_t_o_id(t_o_name):
    t_o = session.query(T_o).filter_by(t_o_name=t_o_name).first()
    if t_o is None:
        t_o = insert_t_o_to_db(t_o_name)
    return t_o.t_o_id


def get_last_record(person_id):
    record = (
        session.query(Record)
        .filter_by(id=person_id)
        .order_by(Record.record_id.desc())
        .first()
    )
    return record


def get_all_pictures(person_id):
    pictures = session.query(Picture).filter_by(id=person_id).all()
    return pictures
