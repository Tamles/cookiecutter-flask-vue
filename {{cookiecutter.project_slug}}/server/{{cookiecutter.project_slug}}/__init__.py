import os
import click
from flask import Flask
from {{cookiecutter.project_slug}}.config import config
from {{cookiecutter.project_slug}}.extensions import *
from {{cookiecutter.project_slug}}.models import Bangumi
from {{cookiecutter.project_slug}}.apis.v1 import bp as api_v1_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_cli(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Bangumi': Bangumi}


def register_cli(app):
    @app.cli.command()
    def forge():
        """Generate fake data."""
        from {{cookiecutter.project_slug}}.fakes import fake_bangumi

        db.drop_all()
        db.create_all()

        click.echo('Generating fake bangumis...')
        fake_bangumi()

        click.echo('Done.')


    @app.cli.command()
    def ptshell():
        """Use ptpython as shell."""
        try:
            from ptpython.repl import embed
            if not app.config['TESTING']:
                embed(app.make_shell_context())
        except ImportError:
            click.echo('ptpython not installed! Use the default shell instead.')
