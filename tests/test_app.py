import os
import sys
import pytest
import werkzeug

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Article

@pytest.fixture(autouse=True)
def _ensure_version():
    if not hasattr(werkzeug, "__version__"):
        werkzeug.__version__ = "patched"
    yield

@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
    yield app
    # Clean up database
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_article_valid(client):
    resp = client.post('/article/new', data={
        'title': 'Test',
        'content': 'Content',
        'meme_potential': '0.5',
        'reality_disruption': '42'
    })
    assert resp.status_code == 302
    with client.application.app_context():
        article = Article.query.first()
        assert article.meme_potential == 0.5
        assert article.reality_disruption == 42

def test_create_article_invalid_numbers(client):
    resp = client.post('/article/new', data={
        'title': 'Bad',
        'content': 'Bad',
        'meme_potential': 'Курический',
        'reality_disruption': 'blah'
    })
    assert resp.status_code == 302
    with client.application.app_context():
        article = Article.query.order_by(Article.id.desc()).first()
        assert article.meme_potential is None
        assert article.reality_disruption is None

def test_api_create_article_numbers(client):
    resp = client.post('/api/articles', json={
        'title': 'Api',
        'content': 'Content',
        'meme_potential': '0.7',
        'reality_disruption': '13'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['meme_potential'] == 0.7
    assert data['reality_disruption'] == 13

def test_api_create_article_invalid_numbers(client):
    resp = client.post('/api/articles', json={
        'title': 'ApiBad',
        'content': 'Content',
        'meme_potential': 'Foo',
        'reality_disruption': 'Bar'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['meme_potential'] is None
    assert data['reality_disruption'] is None


def test_language_switch_to_russian(client):
    resp = client.get('/?lang=ru')
    assert resp.status_code == 200
    body = resp.data.decode('utf-8')
    assert 'Гениально-инвертированная Вики' in body

    resp = client.get('/')
    body = resp.data.decode('utf-8')
    assert 'Гениально-инвертированная Вики' in body


def test_language_switch_back_to_english(client):
    client.get('/?lang=ru')

    resp = client.get('/?lang=en')
    assert resp.status_code == 200
    body = resp.data.decode('utf-8')
    assert 'Genius Inverted Wiki' in body

    resp = client.get('/')
    body = resp.data.decode('utf-8')
    assert 'Genius Inverted Wiki' in body


def test_list_articles_and_filter(client):
    titles = ['Alpha', 'Banana', 'Груша', '1Test']
    with client.application.app_context():
        for t in titles:
            db.session.add(Article(title=t, content='c'))
        db.session.commit()

    resp = client.get('/articles')
    assert resp.status_code == 200
    body = resp.data.decode('utf-8')
    assert 'Alpha' in body
    assert 'Banana' in body

    resp = client.get('/articles?letter=A')
    body = resp.data.decode('utf-8')
    assert 'Alpha' in body
    assert 'Banana' not in body


def test_markdown_rendering(client):
    md_content = '# Header\n\n**bold** text'
    resp = client.post('/article/new', data={'title': 'MD', 'content': md_content})
    assert resp.status_code == 302
    with client.application.app_context():
        article = Article.query.first()
        assert article.content == md_content

    resp = client.get(f'/article/1')
    assert resp.status_code == 200
    body = resp.data.decode('utf-8')
    assert '<h1>Header</h1>' in body
    assert '<strong>bold</strong>' in body

