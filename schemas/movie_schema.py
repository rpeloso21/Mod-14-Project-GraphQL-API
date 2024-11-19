import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie as MovieModel, db
from sqlalchemy.orm import Session

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class Query(graphene.ObjectType):
    movies = graphene.List(Movie)

    query_by_genre_id = graphene.List(Movie, genre_id=graphene.Int(required=True))

    def resolve_movies(self, info):
        return db.session.execute(db.select(MovieModel)).scalars()
    
    def resolve_query_by_genre_id(self, info, genre_id):
        return db.session.execute(db.select(MovieModel).where(MovieModel.genre_id == genre_id)).scalars()
    
class GetMoviesByGenre(graphene.ObjectType):
    movies = graphene.List(Movie)

    genre_id = graphene.Int(required=True)

    def resolve_movies(self, info, genre_id):
        return db.session.execute(db.select(MovieModel).where(MovieModel.genre_id == genre_id)).scalars()
    
class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_id = graphene.Int(required=True)


    movie = graphene.Field(Movie)

    def mutate(self, info, title, description, year, genre_id):
        with Session(db.engine) as session:
            with session.begin():
                movie = MovieModel(title=title, description=description, year=year, genre_id=genre_id)
                session.add(movie)
                session.commit()

            session.refresh(movie)
            return AddMovie(movie=movie)

class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_id = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, title, description, year, genre_id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    movie.title = title
                    movie.description = description
                    movie.year = year
                    movie.genre_id = genre_id
                else:
                    return None

            session.refresh(movie)
            return UpdateMovie(movie=movie)
        
class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    session.delete(movie)
                else:
                    return None
            session.refresh(movie)
            return DeleteMovie(movie=movie)                

        
class Mutation(graphene.ObjectType):
    create_movie = AddMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()
