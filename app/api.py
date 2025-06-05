from flask import Blueprint, jsonify, request, abort
from .models import Article
from . import db

bp = Blueprint('api', __name__)

@bp.route('/articles')
def list_articles():
    """List all articles
    ---
    responses:
      200:
        description: Returns a list of articles
    """
    articles = Article.query.all()
    return jsonify([serialize_article(a) for a in articles])

@bp.route('/articles/<int:article_id>')
def get_article(article_id):
    """Retrieve an article by id
    ---
    parameters:
      - name: article_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: The requested article
    """
    article = Article.query.get_or_404(article_id)
    return jsonify(serialize_article(article))

@bp.route('/articles', methods=['POST'])
def create_article():
    """Create a new article
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
    responses:
      201:
        description: Article created
    """
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        abort(400)
    article = Article(title=data['title'], content=data['content'])

    for field in ['loss_index', 'meme_potential', 'reality_disruption', 'legal_risk',
                  'ethical_toxicity', 'scalability', 'user_retention',
                  'implementation_cost', 'side_effect_index', 'inverse_genius_rating']:
        if field in data:
            value = data[field]
            if field == 'meme_potential':
                try:
                    value = float(value) if value not in (None, '', 'None') else None
                except (TypeError, ValueError):
                    value = None
            elif field == 'reality_disruption':
                try:
                    value = int(value) if value not in (None, '', 'None') else None
                except (TypeError, ValueError):
                    value = None
            setattr(article, field, value)
    db.session.add(article)
    db.session.commit()
    return jsonify(serialize_article(article)), 201

def serialize_article(article):
    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'created_at': article.created_at.isoformat(),
        'updated_at': article.updated_at.isoformat() if article.updated_at else None,
        'loss_index': article.loss_index,
        'meme_potential': article.meme_potential,
        'reality_disruption': article.reality_disruption,
        'legal_risk': article.legal_risk,
        'ethical_toxicity': article.ethical_toxicity,
        'scalability': article.scalability,
        'user_retention': article.user_retention,
        'implementation_cost': article.implementation_cost,
        'side_effect_index': article.side_effect_index,
        'inverse_genius_rating': article.inverse_genius_rating,
    }
