import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save(album_data):
    """
    Сохраняет альбом в БД
    """
    session = connect_db()
    albums_in_db = session.query(
                                    Album.album, Album.artist
                                ).filter(
                                    and_(
                                        Album.artist == album_data["artist"], 
                                        Album.album == album_data["album"]
                                    )
                                ).first()
    
    if albums_in_db:
        print(albums_in_db.album, albums_in_db.artist)
        return "Этот альбом уже есть в базе данных"
    album = Album(
        year = album_data["year"],
        artist = album_data["artist"],
        genre = album_data["genre"],
        album = album_data["album"]
    )
    session.add(album)
    session.commit()

    result = "Альбом сохранен в базу данных"

    return result