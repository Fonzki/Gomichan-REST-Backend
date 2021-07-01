from db import db
from models.syllable import SyllableInstanceModel

syllables = db.Table('syllable_word',
    db.Column(
        'syllable_id', 
        db.Integer, 
        db.ForeignKey('syllable_instances.id'), 
        primary_key=True
    ),
    db.Column(
        'word_id', 
        db.Integer, 
        db.ForeignKey('words.id'), 
        primary_key=True
    )
)

class WordModel(db.Model):
    __tablename__ = 'words'

    id=db.Column(db.Integer, primary_key=True)
    spelling=db.Column(db.String(100))
    display=db.Column(db.String(200))
    sound_link=db.Column(db.String(200))
    syllables=db.relationship(
        'SyllableInstanceModel', 
        secondary=syllables, 
        lazy='subquery',
        backref=db.backref('words', lazy=True)
    )
    stress = db.Column(db.Integer)

    def load_syllables(self, syllables):
        self.syllables.clear()
        for s_id in syllables:
            syllable = SyllableInstanceModel.find_by_id(s_id)
            self.syllables.append(syllable)

    def __init__(self, spelling, display, sound_link, syllables, stress):
        self.spelling = spelling
        self.display = display
        self.sound_link = sound_link
        self.load_syllables(syllables)
        self.stress = stress

    @classmethod
    def find_by_spelling(cls, spelling):
        return cls.query.filter_by(spelling=spelling).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {
            'id': self.id,
            'spelling': self.spelling,
            'display': self.display,
            'sound_link': self.sound_link,
            'stress': self.stress,
            'syllables': [syllable.json() for syllable in self.syllables]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class WordInstanceModel(db.Model):
    __tablename__ = 'word_instances'
    
    id = db.Column(db.Integer, primary_key=True)
    display = db.Column(db.String(200))
    word_id = db.Column(db.Integer)

    def __init__(self, word_id, display):
        self.word_id = word_id
        self.display = display

    def json(self):
        return {
            'id': self.id,
            'display': self.display,
            'word': WordModel.find_by_id(self.word_id).json()
        }

    @classmethod
    def find_by_id(cls, id):
        return WordInstanceModel.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
