from flask import Blueprint
from app.article.views import ArticleAPI

article_bp = Blueprint('article', __name__)

article_view = ArticleAPI.as_view('article_api')

article_bp.add_url_rule('/articles', view_func=article_view, methods=['GET', 'POST'])
article_bp.add_url_rule('/articles/<int:article_id>', view_func=article_view, methods=['GET', 'PUT', 'DELETE'])
