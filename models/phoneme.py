from db import db

class PhonemeModel(db.Model):
    __tablename__ = 'phonemes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    symbol = db.Column(db.String(10))
    aiueo_link = db.Column(db.String(200))
    daijiro_link = db.Column(db.String(200))

    def __init__(self, name, symbol, aiueo_link, daijiro_link):
        self.name = name
        self.symbol = symbol
        self.aiueo_link = aiueo_link
        self.daijiro_link = daijiro_link

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'aiueo_link': self.aiueo_link,
            'daijiro_link': self.daijiro_link
        }

    @classmethod
    def find_by_name(self, name):
        return PhonemeModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(self, id):
        return PhonemeModel.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class PhonemeInstanceModel(db.Model):
    __tablename__ = 'phoneme_instances'
    
    id = db.Column(db.Integer, primary_key=True)
    phoneme_id = db.Column(db.Integer)

    def __init__(self, phoneme_id):
        self.phoneme_id = phoneme_id

    def json(self):
        return {
            'id': self.id,
            'phoneme': PhonemeModel.find_by_id(self.phoneme_id).json()
        }

    @classmethod
    def find_by_id(cls, id):
        return PhonemeInstanceModel.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
