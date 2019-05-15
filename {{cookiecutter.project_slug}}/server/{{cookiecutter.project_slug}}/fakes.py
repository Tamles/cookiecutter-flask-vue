import arrow
from bangumi import db
from {{cookiecutter.project_slug}}.models import Bangumi

bangumis = [{
    "id": 1,
    "name": "辉夜大小姐想让我告白～天才们的恋爱头脑战～",
    "time": "2019-01-12",
    "company": "A-1 Pictures"
}, {
    "id": 2,
    "name": "五等分的新娘",
    "time": "2019-01-10",
    "company": "手冢Production"
}, {
    "id": 3,
    "name": "青春期笨蛋不做兔女郎学姐的梦",
    "time": "2018-10-03",
    "company": "CloverWorks"
}]

def fake_bangumi():
    for b in bangumis:
        bangumi = Bangumi(name=b['name'], time=arrow.get(b['time']).naive, company=b['company'])
        db.session.add(bangumi)
    db.session.commit()
