from db import db
from models.role_phrase import RolePhraseModel

role_phrases=db.Table('role_phrase_line',
    db.Column(
        'role_phrase_id',
        db.Integer,
        db.ForeignKey('role_phrases.id'),
        primary_key=True
    ),
    db.Column(
        'line_id',
        db.Integer,
        db.ForeignKey('lines.id'),
        primary_key=True
    )
)

class LineModel(db.Model):
    __tablename__ = 'lines'

    id=db.Column(db.Integer, primary_key=True)

    translation = db.Column(db.String(400))
    start = db.Column(db.Float)
    duration = db.Column(db.Float)
    video_link = db.Column(db.String(200))
    role_phrases=db.relationship(
        'RolePhraseModel',
        secondary=role_phrases,
        lazy='subquery',
        backref=db.backref('lines', lazy=True)
    )

    def load_role_phrases(self, role_phrases):
        self.role_phrases.clear()
        for role_phrase in role_phrases:
            role_phrase = RolePhraseModel.find_by_id(role_phrase)
            self.role_phrases.append(role_phrase)

    def __init__(self, translation, role_phrases, video_link, start, duration):
        self.translation = translation
        self.load_role_phrases(role_phrases)
        self.video_link = video_link
        self.start = start
        self.duration = duration

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {
            'id': self.id,
            'video_link': self.video_link,
            'start': self.start,
            'duration': self.duration,
            'translation': self.translation,
            'role_phrases': [role_phrase.json() for role_phrase in self.role_phrases],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
