from db import db

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.phoneme import Phoneme, PhonemeList
from resources.phoneme import PhonemeInstance, PhonemeInstanceList, PhonemeInstanceCreate
from resources.phoneme import PhonemeIdConverter, PhonemeNameConverter

from resources.syllable import Syllable, SyllableList
from resources.syllable import SyllableInstance, SyllableInstanceList, SyllableInstanceCreate
from resources.syllable import SyllableInstancesCreate

from resources.word import Word, WordList
from resources.word import WordInstance, WordInstanceList, WordInstanceCreate
from resources.word import WordInstancesCreate

from resources.phrase import Phrase, PhraseList, PhraseCreate
from resources.role_phrase import RolePhrase, RolePhraseList, RolePhraseCreate
from resources.role_phrase import RolePhraseByRole

from resources.line import Line, LineList, LineCreate
from resources.line_builder import LineBuilder
from resources.page import Page, PageList, PageCreate

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)
app.secret_key = "secret_key"
api = Api(app)

@app.before_first_request
def make_tables():
    db.create_all()


api.add_resource(Phoneme, '/phoneme/<string:name>')
api.add_resource(PhonemeList, '/phonemes')
api.add_resource(PhonemeInstance, '/phoneme/instance/<int:id>')
api.add_resource(PhonemeInstanceCreate, '/phoneme/instance/create')
api.add_resource(PhonemeInstanceList, '/phoneme/instances')
api.add_resource(PhonemeIdConverter, '/phoneme/name-to-id')
api.add_resource(PhonemeNameConverter, '/phoneme/name-to-instance')

api.add_resource(Syllable, '/syllable/<string:spelling>')
api.add_resource(SyllableList, '/syllables')
api.add_resource(SyllableInstance, '/syllable/instance/<int:id>')
api.add_resource(SyllableInstanceCreate, '/syllable/instance/create')
api.add_resource(SyllableInstancesCreate, '/syllable/instances/create')
api.add_resource(SyllableInstanceList, '/syllable/instances')

api.add_resource(Word, '/word/<string:spelling>')
api.add_resource(WordList, '/words')
api.add_resource(WordInstance, '/word/instance/<int:id>')
api.add_resource(WordInstanceCreate, '/word/instance/create')
api.add_resource(WordInstancesCreate, '/word/instances/create')
api.add_resource(WordInstanceList, '/word/instances')

api.add_resource(Phrase, '/phrase/<int:id>')
api.add_resource(PhraseCreate, '/phrase/create')
api.add_resource(PhraseList, '/phrases')
api.add_resource(RolePhrase, '/role-phrase/<int:id>')
api.add_resource(RolePhraseCreate, '/role-phrase/create')
api.add_resource(RolePhraseList, '/role-phrases')
api.add_resource(RolePhraseByRole, '/role-phrases/role/<string:role>')

api.add_resource(Line, '/line/<int:id>')
api.add_resource(LineCreate, '/line/create')
api.add_resource(LineList, '/lines')
api.add_resource(LineBuilder, '/line/builder')

api.add_resource(Page, '/page/<int:id>')
api.add_resource(PageCreate, '/page/create')
api.add_resource(PageList, '/pages')


