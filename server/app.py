#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    all_articles = [articles.to_dict() for articles in Article.query.all()]

    response = make_response(
        all_articles,
        200
    )

    return response


@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0

    session['page_views'] += 1

    if session['page_views'] < 4:
        article_dict = Article.query.filter(Article.id == id).first().to_dict()
        print(session['page_views'])

        if article_dict:
            response = make_response(
                article_dict,
                200
            )
        else:
            response = make_response(
                {'error': 'Article not found'},
                400
            )
    else:
        response = make_response(
            {'message': 'Maximum pageview limit reached'},
            401
            )
        
    return response
      
if __name__ == '__main__':
    app.run(port=5555)
