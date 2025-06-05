import random
from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Article, ArticleVersion

bp = Blueprint('web', __name__)

@bp.route('/')
def index():
    articles = Article.query.order_by(Article.created_at.desc()).limit(5).all()
    count = Article.query.count()
    random_article = None
    if count:
        random_article = Article.query.offset(random.randrange(count)).first()
    return render_template('index.html', articles=articles, random_article=random_article)

@bp.route('/article/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    versions = ArticleVersion.query.filter_by(article_id=article_id).order_by(ArticleVersion.version.desc()).all()
    return render_template('article.html', article=article, versions=versions)

@bp.route('/article/new', methods=['GET', 'POST'])
@bp.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id=None):
    article = Article.query.get(article_id) if article_id else Article()
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.loss_index = request.form.get('loss_index')
        article.meme_potential = request.form.get('meme_potential')
        article.reality_disruption = request.form.get('reality_disruption')
        article.legal_risk = request.form.get('legal_risk')
        article.ethical_toxicity = request.form.get('ethical_toxicity')
        article.scalability = request.form.get('scalability')
        article.user_retention = request.form.get('user_retention')
        article.implementation_cost = request.form.get('implementation_cost')
        article.side_effect_index = request.form.get('side_effect_index')
        article.inverse_genius_rating = request.form.get('inverse_genius_rating')

        if not article.id:
            db.session.add(article)
            version_number = 1
        else:
            latest_version = ArticleVersion.query.filter_by(article_id=article.id).order_by(ArticleVersion.version.desc()).first()
            version_number = latest_version.version + 1 if latest_version else 1

        db.session.commit()
        version = ArticleVersion(article_id=article.id, content=article.content, version=version_number)
        db.session.add(version)
        db.session.commit()
        return redirect(url_for('web.view_article', article_id=article.id))
    return render_template('edit.html', article=article)
