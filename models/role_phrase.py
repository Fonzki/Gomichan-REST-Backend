from db import db
from models.phrase import PhraseModel

class RolePhraseModel(db.Model):
    __tablename__ = 'role_phrases'

    id=db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(400))
    role = db.Column(db.String(20))
    phrase = db.Column(db.Integer)
    phrase_string = db.Column(db.String(400))

    def make_phrase_string(self):
        pstring = ""
        phrase = PhraseModel.find_by_id(self.phrase).json()
        words = phrase['words']

        for word in words:
            pstring += (word['display'] + " ")

        pstring = pstring[0:-1]

        if self.punctuation and not self.punctuation == "None":
            pstring += self.punctuation

        return pstring

    def __init__(self, phrase, role, note, punctuation):
        self.phrase = phrase
        self.note = note
        self.role = role
        self.punctuation = punctuation
        self.phrase_string = self.make_phrase_string()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_role(cls, role):
        return cls.query.filter_by(role=role)
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {
            'id': self.id,
            'role': self.role,
            'note': self.note,
            'phrase_string': self.phrase_string,
            'phrase': PhraseModel.find_by_id(self.phrase).json(),
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
