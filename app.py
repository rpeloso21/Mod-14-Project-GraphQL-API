from flask import Flask
from flask_graphql import  GraphQLView
import graphene
from schemas.movie_schema import Query as MovieQuery, Mutation as MovieMutation
from schemas.genre_schema import Query as GenreQuery, Mutation as GenreMutation
from models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Tsrost007!@localhost/movie_db'
db.init_app(app)

class Query(MovieQuery, GenreQuery, graphene.ObjectType):
    pass

class Mutation(MovieMutation, GenreMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)