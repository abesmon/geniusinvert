from flask import Flask, request, session
from markupsafe import Markup
import markdown
from flask_babel import Babel
from flasgger import Swagger
from pathlib import Path
import subprocess
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


babel = Babel()
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'change-me'
    app.config.setdefault('BABEL_DEFAULT_LOCALE', 'en')
    default_trans_dir = Path(__file__).resolve().parent.parent / 'translations'
    app.config.setdefault('BABEL_TRANSLATION_DIRECTORIES', str(default_trans_dir))

    trans_dir = app.config['BABEL_TRANSLATION_DIRECTORIES']
    po_files = list(Path(trans_dir).rglob('*.po'))
    if po_files:
        subprocess.run(['pybabel', 'compile', '-d', trans_dir], check=False)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    Swagger(app, config={"specs_route": "/swagger"}, merge=True)

    @app.template_filter('markdown')
    def markdown_filter(text: str) -> Markup:
        """Render Markdown text into HTML for templates."""
        if text is None:
            return Markup("")
        return Markup(markdown.markdown(text))

    def get_locale() -> str:
        lang = request.args.get('lang')
        if lang:
            session['lang'] = lang
        return session.get('lang', app.config['BABEL_DEFAULT_LOCALE'])

    babel.init_app(app, locale_selector=get_locale)

    from . import routes, api
    app.register_blueprint(routes.bp)
    app.register_blueprint(api.bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
