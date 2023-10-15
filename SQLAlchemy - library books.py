# Uvoz potrebnih modula i biblioteka
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# Kreiranje veze (connection) sa bazom podataka library.db putem SQLAlchemy
engine = create_engine('sqlite:///library.db', echo=False)

# Kreiranje instance MetaData koja ce sadrzati informacije o tabelama
meta = MetaData()

# Definisanje tabele books sa kolonama id, title, i year
books = Table(
    'books', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('year', Integer)
)

# Kreiranje tabele u bazi podataka
meta.create_all(engine)

# Lista za cuvanje unesenih knjiga
book_list = []

while True:
    # Unos podataka o knjizi od strane korisnika
    book_id = input("Type id number of the book (or press Enter to finish): ")
    if not book_id:
        break

    book_title = input(" Type the title of the book: ")
    book_year = input(" Type the year of publication of the book: ")

    # Kreiranje SQL upita za unos podataka u tabelu books
    data_entry = books.insert().values(id=book_id, title=book_title, year=book_year)

    # Povezivanje sa bazom podataka
    with engine.connect() as conn:
        # Izvrsavanje SQL upita za unos podataka
        conn.execute(data_entry)

    # Dodavanje podataka u listu
    book_list.append((book_id, book_title, book_year))

# Prikazivanje svih unesenih knjiga
if book_list:
    print(" Entered books: ")
    for book in book_list:
        print(" Id number of the book: {} | Book title: {} | Year of publication of the book: {} ".format(book[0],
                                                                                                            book[1],
                                                                                                            book[2]))
else:
    print(" No books were entered. ")

# Prikazivanje svih knjiga u bazi podataka
with engine.connect() as conn:
    reading_data = books.select()
    result = conn.execute(reading_data).fetchall()

    # Prikazivanje rezultata
    print(" \nBooks in the database: ")
    for row in result:
        print(
            " Id number of the book: {} | Book title: {} | Year of publication of the book: {} ".format(row[0], row[1],
                                                                                                        row[2]))
