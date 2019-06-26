import json
from pathlib import Path
import arrow
from {{cookiecutter.project_slug}} import db
from {{cookiecutter.project_slug}}.models import Bangumi

bangumis = json.loads(Path('bangumi.json').read_text(encoding='utf-8'), encoding='utf-8')

def fake_bangumi():
    for b in bangumis:
        bangumi = Bangumi(name=b['title'], time=arrow.get(b['date']).naive, url=b['url'])
        db.session.add(bangumi)
    db.session.commit()
