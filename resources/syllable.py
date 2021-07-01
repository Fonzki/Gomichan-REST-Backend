from flask_restful import Resource, Api, reqparse
from models.syllable import SyllableModel, SyllableInstanceModel

class Syllable(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sound_link', type=str, required=True, help="need sound link")
    parser.add_argument('phonemes', action='append', required=True, help="need phenomes")

    def post(self, spelling):
        s = SyllableModel.find_by_spelling(spelling)
        if s:
            return s.json(), 400
            
        data = Syllable.parser.parse_args()
        syllable_def = SyllableModel(spelling, **data)
        
        try:
            syllable_def.save_to_db()
        except:
            return {'message': 'failed to save syllable_def to database.'}, 500

        return syllable_def.json(), 201

    def get(self, spelling):
        sdef = SyllableModel.find_by_spelling(spelling)
        if not sdef:
            return {'message': f"syllable is undefined."}, 400
        return sdef.json()
        
    def put(self, spelling):
        sdef = SyllableModel.find_by_spelling(spelling)
        data = Syllable.parser.parse_args()

        if not sdef:
            syllable_def = SyllableModel(spelling, **data)
            
            try:
                syllable_def.save_to_db()
            except:
                return {'message': 'failed to save syllable_def to database.'}, 500

            return syllable_def.json(), 201

        sdef.sound = data['sound_link']
        #safety check for phoneme list function TODO
        sdef.load_phonemes(data['phonemes'])

        try:
            sdef.save_to_db()
        except:
            return {'message': 'failed to save syllable_def to database.'}, 500

        return sdef.json()

    def delete(self, spelling):
        sdef = SyllableModel.find_by_spelling(spelling)
        if sdef:
            sdef.delete_from_db()
        return {'message': f"'{spelling}' deleted."}

class SyllableList(Resource):
    def get(self):
        return {'syllables': [syllable.json() for syllable in SyllableModel.find_all()]}

class SyllableInstance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('syllable_id', type=int, required=True, help="need syllable_id")

    def get(self, id):
        syllable_instance = SyllableInstanceModel.find_by_id(id)
        if not syllable_instance:
            return {'message': f'syllable_instance not defined.'}, 400

        return syllable_instance.json()

    def put(self, id):
        syllable_instance = SyllableInstanceModel.find_by_id(id)
        data = SyllableInstance.parser.parse_args()

        if not syllable_instance:
            syllable_instance = SyllableInstanceModel(**data)

            try:
                syllable_instance.save_to_db()
            except:
                return {'message': 'failed to save syllable_instance to database.'}, 500

            return syllable_instance.json(), 201

        syllable_instance.syllable_id = data['syllable_id']

        try:
            syllable_instance.save_to_db()
        except:
            return {'message': 'failed to save syllable_instance to database.'}, 500
        
        return syllable_instance.json()

    def delete(self, id):
        syllable_instance = SyllableInstanceModel.find_by_id(id)
        if syllable_instance:
            syllable_instance.delete_from_db()

        return {'message': f'syllable_instance deleted.'}

class SyllableInstanceCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('syllable_id', type=int, required=True, help="need syllable_id")

    def post(self):
        data = SyllableInstance.parser.parse_args()
        syllable_instance = SyllableInstanceModel(**data)

        try:
            syllable_instance.save_to_db()
        except:
            return {'message': 'failed to save syllable_instance to database.'}, 500

        return syllable_instance.json(), 201

class SyllableInstancesCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('syllable_spellings', action='append', required=True, help="need syllable spellings")

    def post(self):
        data = self.parser.parse_args()
        id_list = []

        for spelling in data['syllable_spellings']:
            syllable = SyllableModel.find_by_spelling(spelling)
            if not syllable:
                return {'message': f"{spelling} doesn't exist. No instances made."}, 400

        for spelling in data['syllable_spellings']:
            pid = SyllableModel.find_by_spelling(spelling).id
            instance = SyllableInstanceModel(pid)

            try:
                instance.save_to_db()
            except:
                return {'message': 'failed to save ({spelling}) instance to database.'}, 500
            
            id_list.append(instance.id)
        
        return {'id_list': id_list}

class SyllableInstanceList(Resource):
    def get(self):
        return {'syllable_instances': [syllable_instance.json() for syllable_instance in SyllableInstanceModel.find_all()]}
