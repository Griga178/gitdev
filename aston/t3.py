import datetime

from sqlalchemy import (
    create_engine, Column, Integer,  ForeignKey, Text, Table
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# 1. Необходимо создать базу данных, которая хранит информацию о книгах и авторах.
Base = declarative_base()

db_path_ram = "sqlite:///:memory:"

# 2. Смоделировать отношение "многие ко многим" между книгами и авторами (т.е., одна книга может быть написана несколькими авторами, и один автор может написать несколько книг).
book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)

    books = relationship("Book", secondary=book_author, back_populates="authors")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(Text) # название книги

    authors = relationship("Author", secondary=book_author, back_populates="books")


def init_db():
    engine = create_engine(db_path_ram)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

# 3. Написать Python-скрипт, который:
def load_authors_books(session):
    # добавляет авторов и книги в базу данных.
    author_list = [
        Author(name="Лев", surname="Толстой"),
        Author(name="Фёдор", surname="Достоевский"),
        Author(name="Иван", surname="Тургенев"),
        Author(name="Антон", surname="Чехов"),
        Author(name="Михаил", surname="Булгаков"),
    ]

    book_list = [
        Book(title="Война и мир"),
        Book(title="Преступление и наказание"),
        Book(title="Отцы и дети"),
        Book(title="Вишнёвый сад"),
        Book(title="Сборник русской классики"),
    ]
    session.add_all(author_list + book_list)
    session.commit()

def connect_book_author(session):
    # связи книга — автор (id известны)
    connections = [
        (1, 1),  # Война и мир — Толстой
        (2, 2),  # Преступление и наказание — Достоевский
        (3, 3),  # Отцы и дети — Тургенев
        (4, 4),  # Вишнёвый сад — Чехов
        # Сборник — сразу несколько авторов
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
    ]
    books = {b.id: b for b in session.query(Book).all()}
    authors = {a.id: a for a in session.query(Author).all()}

    for book_id, author_id in connections:
        book = books[book_id]
        author = authors[author_id]
        if author not in book.authors:
            book.authors.append(author)

    session.commit()


# выводит информацию о том, какие книги написал каждый автор.
def get_info(session):
    print("Автор: книга")
    for a in session.query(Author).all():
        print(f"{a.name} {a.surname}: {', '.join(b.title for b in a.books)}")

    print("\nКнига: Автор")
    for b in session.query(Book).all():
        print(f"{b.title}: {', '.join(f'{a.name} {a.surname}' for a in b.authors)}")

if __name__ == "__main__":
    Session = init_db()
    session = Session()

    load_authors_books(session)
    connect_book_author(session)
    get_info(session)

# Вывод:
# Автор: книга
# Лев Толстой: Война и мир, Сборник русской классики
# Фёдор Достоевский: Преступление и наказание, Сборник русской классики
# Иван Тургенев: Отцы и дети, Сборник русской классики
# Антон Чехов: Вишнёвый сад, Сборник русской классики
# Михаил Булгаков: Сборник русской классики
#
# Книга: Автор
# Война и мир: Лев Толстой
# Преступление и наказание: Фёдор Достоевский
# Отцы и дети: Иван Тургенев
# Вишнёвый сад: Антон Чехов
# Сборник русской классики: Лев Толстой, Фёдор Достоевский, Иван Тургенев, Антон Чехов, Михаил Булгаков
