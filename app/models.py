from datetime import datetime
from . import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Characteristics
    loss_index = db.Column(db.String(50))
    meme_potential = db.Column(db.Float)
    reality_disruption = db.Column(db.Integer)
    legal_risk = db.Column(db.String(50))
    ethical_toxicity = db.Column(db.String(50))
    scalability = db.Column(db.String(50))
    user_retention = db.Column(db.String(50))
    implementation_cost = db.Column(db.String(50))
    side_effect_index = db.Column(db.String(50))
    inverse_genius_rating = db.Column(db.String(50))

    versions = db.relationship('ArticleVersion', backref='article', lazy=True, cascade='all, delete-orphan')

class ArticleVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.Integer, nullable=False)
