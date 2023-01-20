import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json

from models import create_tables, Publisher, Shop, Book, Stock, Sale

# DSN = ' '
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


def get_info_buying_books(publisher_name):
    if publisher_name.isnumeric():
        for i in session.query(Book.title, Shop.name, (Sale.count*Sale.price),
                               Sale.date_sale).\
                join(Stock.shops).join(Stock.books).join(Book.publishers).\
                join(Stock.sales).filter(Publisher.id == int(publisher_name)):
            print(i)
    else:
        for i in session.query(Book.title, Shop.name, (Sale.count*Sale.price),
                               Sale.date_sale).\
                join(Stock.shops).join(Stock.books).join(Book.publishers).\
                join(Stock.sales).filter(Publisher.name.like(publisher_name)):
            print(i)

session.close()

if __name__ == '__main__':
    publisher_name = input('Введите имя или id издателя: ')
    get_info_buying_books(publisher_name)