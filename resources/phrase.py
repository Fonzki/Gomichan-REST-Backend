from flask_restful import Resource, reqparse
from models.phrase import PhraseModel

class Phrase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sound_link', type=str, required=True, help="need sound_link")
    parser.add_argument('words', action='append', required=True, help="need words")
    parser.add_argument('display', type=str, required=True, help="need display text")

    def get(self, id):
        phrase = PhraseModel.find_by_id(id)
        if not phrase:
            return {'message': f'phrase not defined.'}, 400

        return phrase.json()

    def put(self, id):
        phrase = PhraseModel.find_by_id(id)
        data = Phrase.parser.parse_args()

        if not phrase:
            phrase = PhraseModel(**data)

            try:
                phrase.save_to_db()
            except:
                return {'message': 'failed to save phrase to database.'}, 500

            return phrase.json(), 201

        phrase.sound_link = data['sound_link']
        phrase.load_words(data['words'])

        try:
            phrase.save_to_db()
        except:
            return {'message': 'failed to save phrase to database.'}, 500
        
        return phrase.json()

    def delete(self, id):
        phrase = PhraseModel.find_by_id(id)
        if phrase:
            phrase.delete_from_db()

        return {'message': f'phrase deleted.'}

class PhraseCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('words', action='append', required=True, help="need words")
    parser.add_argument('display', type=str, required=True, help="need display text")
    parser.add_argument('sound_link', type=str, required=True, help="need sound_link")

    def post(self):
        data = Phrase.parser.parse_args()
        phrase = PhraseModel(**data)

        try:
            phrase.save_to_db()
        except Exception as error:
            print(error)
            return {'message': 'failed to save phrase to database.'}, 500

        return phrase.json(), 201

class PhraseList(Resource):
    def get(self):
        return {'phrases': [phrase.json() for phrase in PhraseModel.find_all()]}
