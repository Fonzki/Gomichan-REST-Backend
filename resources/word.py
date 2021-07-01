from flask_restful import Resource, Api, reqparse
from models.word import WordModel, WordInstanceModel

class Word(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('display', type=str, required=True, help="need display text")
    parser.add_argument('sound_link', type=str, required=True, help="need sound link")
    parser.add_argument('syllables', action='append',type=int, required=True, help="need syllables")
    parser.add_argument('stress', type=int, required=True, help="need stress position")

    def post(self, spelling):
        word = WordModel.find_by_spelling(spelling)
        if word:
            return {'message': f'{spelling} is defined.'}, 400

        data = Word.parser.parse_args()
        word = WordModel(spelling, **data)

        try:
            word.save_to_db()
        except Exception as error:
            print(error)
            return {'message': "ur fucked bro lol"}, 500

        return word.json(), 201

    def get(self, spelling):
        word = WordModel.find_by_spelling(spelling)
        if not word:
            return {'message': f'{spelling} not defined.'}, 400

        return word.json()

    def put(self, spelling):
        word = WordModel.find_by_spelling(spelling)
        data = Word.parser.parse_args()

        if not word:
            word = WordModel(spelling, **data)

            try:
                word.save_to_db()
            except:
                return {'message': 'failed to save word to database.'}, 500

            return word.json(), 201

        word.sound = data['sound_link']
        word.stress = data['stress']
        word.load_syllables(data['syllables'])

        try:
            word.save_to_db()
        except:
            return {'message': 'failed to save word to database.'}, 500
        
        return word.json()

    def delete(self, spelling):
        word = WordModel.find_by_spelling(spelling)
        if word:
            word.delete_from_db()

        return {'message': f'{spelling} deleted.'}

class WordList(Resource):
    def get(self):
        return {'words': [word.json() for word in WordModel.find_all()]}

class WordInstance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('word_id', type=int, required=True, help="need word_id")

    def get(self, id):
        word_instance = WordInstanceModel.find_by_id(id)
        if not word_instance:
            return {'message': f'word_instance not defined.'}, 400

        return word_instance.json()

    def put(self, id):
        word_instance = WordInstanceModel.find_by_id(id)
        data = WordInstance.parser.parse_args()

        if not word_instance:
            word_instance = WordInstanceModel(**data)

            try:
                word_instance.save_to_db()
            except:
                return {'message': 'failed to save word_instance to database.'}, 500

            return word_instance.json(), 201

        word_instance.word_id = data['word_id']

        try:
            word_instance.save_to_db()
        except:
            return {'message': 'failed to save word_instance to database.'}, 500
        
        return word_instance.json()

    def delete(self, id):
        word_instance = WordInstanceModel.find_by_id(id)
        if word_instance:
            word_instance.delete_from_db()

        return {'message': f'word_instance deleted.'}

class WordInstanceCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('word_id', type=int, required=True, help="need word_id")

    def post(self):
        data = WordInstance.parser.parse_args()
        word_instance = WordInstanceModel(**data)

        try:
            word_instance.save_to_db()
        except:
            return {'message': 'failed to save word_instance to database.'}, 500

        return word_instance.json(), 201

class WordInstancesCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('word_ids', action='append', required=True, help="need word ids")

    def post(self):
        data = self.parser.parse_args()
        id_list = []

        for w_id in data['word_ids']:
            word = WordModel.find_by_id(w_id)
            if not word:
                return {'message': f"{w_id} doesn't exist. No instances made."}, 400

        for w_id in data['word_ids']:
            instance = WordInstanceModel(w_id)

            try:
                instance.save_to_db()
            except:
                return {'message': 'failed to save ({w_id}) instance to database.'}, 500
            
            id_list.append(instance.id)
        
        return {'id_list': id_list}

class WordInstanceList(Resource):
    def get(self):
        return {'word_instances': [word_instance.json() for word_instance in WordInstanceModel.find_all()]}
