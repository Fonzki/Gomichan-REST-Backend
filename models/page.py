from db import db
from models.line import LineModel

lines=db.Table('line_page',
    db.Column(
        'line_id',
        db.Integer,
        db.ForeignKey('lines.id'),
        primary_key=True
    ),
    db.Column(
        'page_id',
        db.Integer,
        db.ForeignKey('pages.id'),
        primary_key=True
    )
)

class PageModel(db.Model):
    __tablename__ = 'pages'

    id=db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(400))
    lines=db.relationship(
        'LineModel',
        secondary=lines,
        lazy='subquery',
        backref=db.backref('pages', lazy=True)
    )

    def load_lines(self, lines):
        self.lines.clear()
        for line in lines:
            line = LineModel.find_by_id(line)
            self.lines.append(line)

    def __init__(self, title, lines):
        self.title = title
        self.load_lines(lines)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'lines': [line.json() for line in self.lines]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
