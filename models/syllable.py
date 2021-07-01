from db import db
from models.phoneme import PhonemeInstanceModel

phonemes= db.Table('phoneme_syllable',
    db.Column(
        'phoneme_id', 
        db.Integer, 
        db.ForeignKey('phoneme_instances.id'), 
        primary_key=True
    ),
    db.Column(
        'syllable_def_id', 
        db.Integer, 
        db.ForeignKey('syllable_defs.id'), 
        primary_key=True
    )
)

class SyllableModel(db.Model):
    __tablename__ = 'syllable_defs'

    id=db.Column(db.Integer, primary_key=True)
    spelling=db.Column(db.String(10))
    sound_link=db.Column(db.String(200))
    phonemes=db.relationship(
        'PhonemeInstanceModel', 
        secondary=phonemes, 
        lazy='subquery',
        backref=db.backref('syllables', lazy=True)
    )

    def load_phonemes(self, phonemes):
        self.phonemes.clear()
        for p_id in phonemes:
            phoneme = PhonemeInstanceModel.find_by_id(p_id)
            self.phonemes.append(phoneme)

    def __init__(self, spelling, sound_link, phonemes):
        self.spelling = spelling
        self.sound_link = sound_link
        self.load_phonemes(phonemes)

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
            'sound_link': self.sound_link,
            'phonemes': [phoneme.json() for phoneme in self.phonemes]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class SyllableInstanceModel(db.Model):
    __tablename__ = 'syllable_instances'
    
    id = db.Column(db.Integer, primary_key=True)
    syllable_id = db.Column(db.Integer)

    def __init__(self, syllable_id):
        self.syllable_id = syllable_id

    def json(self):
        return {
            'id': self.id,
            'syllable': SyllableModel.find_by_id(self.syllable_id).json()
        }

    @classmethod
    def find_by_id(cls, id):
        return SyllableInstanceModel.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
