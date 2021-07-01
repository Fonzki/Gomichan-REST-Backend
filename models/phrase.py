from db import db
from models.word import WordInstanceModel

words=db.Table('word_phrase',
    db.Column(
        'word_id',
        db.Integer,
        db.ForeignKey('word_instances.id'),
        primary_key=True
    ),
    db.Column(
        'phrase_id',
        db.Integer,
        db.ForeignKey('phrases.id'),
        primary_key=True
    )
)

class PhraseModel(db.Model):
    __tablename__ = 'phrases'

    id=db.Column(db.Integer, primary_key=True)
    sound_link = db.Column(db.String(200))
    words=db.relationship(
        'WordInstanceModel',
        secondary=words,
        lazy='subquery',
        backref=db.backref('phrases', lazy=True)
    )
    display = db.Column(db.String(400))

    def load_words(self, words):
        self.words.clear()
        for word in words:
            word = WordInstanceModel.find_by_id(word)
            self.words.append(word)

    def __init__(self, words, display, sound_link):
        self.load_words(words)
        self.sound_link = sound_link
        self.display = display

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {
            'id': self.id,
            'display': self.display,
            'sound_link': self.sound_link,
            'words': [word.json() for word in self.words]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
