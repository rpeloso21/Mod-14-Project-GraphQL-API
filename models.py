from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255))
    description: Mapped[str] = mapped_column(db.String(255))
    year: Mapped[int] = mapped_column(db.Integer)
    genre_id: Mapped[int] = mapped_column(db.ForeignKey('genres.id'))



class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255))
