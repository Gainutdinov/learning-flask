from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__='movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    identity = db.Column(db.Integer)

    def json(self):
        return {'name': self.name, 'price': self.price, 'identity': self.identity}

    def add_movie(_name, _price, _identity):
        new_movie = Movie(name=_name, price=_price, identity=_identity)
        db.session.add(new_movie)
        db.session.commit()
    
    def get_all_movies():
        return [Movie.json(movie) for movie in Movie.query.all()]
    
    def get_movie(_identity):
        return Movie.query.filter_by(identity=_identity).first()

    def delete_movie(_identity):
        is_successful = Movie.query.filter_by(identity=_identity).delete()
        db.session.commit()
        return bool(is_successful)

    def update_movie_price(_identity, _price):
        movie_to_update = Movie.query.filter_by(identity=_identity).first()
        movie_to_update.price = _price
        db.session.commit()

    def update_movie_name(_identity, _name):
        movie_to_update = Movie.query.filter_by(identity=_identity).first()
        movie_to_update.name = _name
        db.session.commit()

    def replace_movie(_identity, _name, _price):
        movie_to_replace = Movie.query.filter_by(identity=_identity).first()
        movie_to_replace.price = _price
        movie_to_replace.name = _name
        db.session.commit()



    def __repr__(self):
        movie_object = {
            'name': self.name,
            'price': self.price,
            'identity': self.identity
        }
        return json.dumps(movie_object)
