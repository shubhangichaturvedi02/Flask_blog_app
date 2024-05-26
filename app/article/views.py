from flask.views import MethodView
from flask import request, jsonify
from app import db
from app.models import Article, User
from flask_jwt_extended import jwt_required, get_jwt_identity

class ArticleAPI(MethodView):
    def get(self, article_id=None):
        if article_id is None:
            articles = Article.query.all()
            output = []
            for article in articles:
                article_data = {
                    'title': article.title,
                    'content': article.content,
                    'author': article.author.username,
                    'date_posted': article.date_posted
                }
                output.append(article_data)
            return jsonify(output), 200
        else:
            article = Article.query.get_or_404(article_id)
            article_data = {
                'title': article.title,
                'content': article.content,
                'author': article.author.username,
                'date_posted': article.date_posted
            }
            return jsonify(article_data), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        print("FFFFFFF", data)
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user['email']).first()
        article = Article(title=data['title'], content=data['content'], author=user)
        print("dssssssssssssssssss")
        db.session.add(article)
        db.session.commit()
        return jsonify(message="Article created"), 201

    @jwt_required()
    def put(self, article_id):
        data = request.get_json()
        article = Article.query.get_or_404(article_id)
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user['email']).first()
        if article.author != user:
            return jsonify(message="Permission denied"), 403

        article.title = data['title']
        article.content = data['content']
        db.session.commit()
        return jsonify(message="Article updated"), 200

    @jwt_required()
    def delete(self, article_id):
        article = Article.query.get_or_404(article_id)
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user['email']).first()
        if article.author != user:
            return jsonify(message="Permission denied"), 403

        db.session.delete(article)
        db.session.commit()
        return jsonify(message="Article deleted"), 200
