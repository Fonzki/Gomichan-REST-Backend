from flask_restful import Resource, Api, reqparse
from models.phoneme import PhonemeModel, PhonemeInstanceModel
import json

class Phoneme(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('symbol', type=str, required=True, help="need symbol")
    parser.add_argument('aiueo_link', type=str)
    parser.add_argument('daijiro_link', type=str)

    def post(self, name):
        if PhonemeModel.find_by_name(name):
            return {'message': f"phoneme is defined."}, 400
        
        data = Phoneme.parser.parse_args()
        if not data['aiueo_link'] and not data['daijiro_link']:
            return {'message': 'needs at least one pronunciation link'}, 400

        phoneme = PhonemeModel(name, **data)
        
        try:
            phoneme.save_to_db()
        except:
            return {'message': 'failed to save phoneme to database.'}, 500

        return phoneme.json(), 201

    def get(self, name):
        phoneme = PhonemeModel.find_by_name(name)

        if phoneme:
            return phoneme.json()
        return {'message': 'phoneme not defined.'}, 404
    
    def put(self, name):
        phoneme = PhonemeModel.find_by_name(name)

        data = Phoneme.parser.parse_args()
        if phoneme:
            phoneme.symbol = data['symbol']
            phoneme.aiueo_link = data['aiueo_link']
            phoneme.daijiro_link = data['daijiro_link']
            return phoneme.json()
        
        phoneme = PhonemeModel(name, **data)
        
        try:
            phoneme.save_to_db()
        except:
            return {'message': 'failed to save phoneme to database.'}, 500

        return phoneme.json(), 201

    def delete(self, name):
        phoneme = PhonemeModel.find_by_name(name)

        if phoneme:
            phoneme.delete_from_db()
        return {'message': f'{name} deleted.'} 
    
class PhonemeList(Resource):
    def get(self):
        return {'phonemes': [phoneme.json() for phoneme in PhonemeModel.find_all()]}

    def post(self):
        with open('phonemes.json') as f:
            data = json.load(f)

        count = 0 
        for p in data['phonemes']:
            phoneme = PhonemeModel(p['name'], p['symbol'], p['aiueo_link'], p['daijiro_link'])
            phoneme.save_to_db()
            count += 1

        return {'phonemes_added': count}

class PhonemeInstance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phoneme_id', type=int, required=True, help="need phoneme_id")

    def get(self, id):
        phoneme_instance = PhonemeInstanceModel.find_by_id(id)
        if not phoneme_instance:
            return {'message': f'phoneme_instance not defined.'}, 400

        return phoneme_instance.json()

    def put(self, id):
        phoneme_instance = PhonemeInstanceModel.find_by_id(id)
        data = PhonemeInstance.parser.parse_args()

        if not phoneme_instance:
            phoneme_instance = PhonemeInstanceModel(**data)

            try:
                phoneme_instance.save_to_db()
            except:
                return {'message': 'failed to save phoneme_instance to database.'}, 500

            return phoneme_instance.json(), 201

        phoneme_instance.phoneme_id = data['phoneme_id']

        try:
            phoneme_instance.save_to_db()
        except:
            return {'message': 'failed to save phoneme_instance to database.'}, 500
        
        return phoneme_instance.json()

    def delete(self, id):
        phoneme_instance = PhonemeInstanceModel.find_by_id(id)
        if phoneme_instance:
            phoneme_instance.delete_from_db()

        return {'message': f'phoneme_instance deleted.'}

class PhonemeInstanceCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phoneme_id', type=int, required=True, help="need phoneme_id")

    def post(self):
        data = PhonemeInstance.parser.parse_args()
        phoneme_instance = PhonemeInstanceModel(**data)

        try:
            phoneme_instance.save_to_db()
        except:
            return {'message': 'failed to save phoneme_instance to database.'}, 500

        return phoneme_instance.json(), 201

class PhonemeInstanceList(Resource):
    def get(self):
        return {'phoneme_instances': [phoneme_instance.json() for phoneme_instance in PhonemeInstanceModel.find_all()]}


class PhonemeIdConverter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phoneme_names', action='append', required=True, help="need phoneme names")

    def post(self):
        data = self.parser.parse_args()
        id_list = ""
        for name in data['phoneme_names']:
            id_list += (str(PhonemeModel.find_by_name(name).id)+", ")

        return {'id_list': id_list[0:-2]}

class PhonemeNameConverter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phoneme_names', action='append', required=True, help="need phoneme names")

    def post(self):
        data = self.parser.parse_args()
        id_list = []

        for name in data['phoneme_names']:
            phoneme = PhonemeModel.find_by_name(name)
            if not phoneme:
                return {'message': f"{name} doesn't exist. No instances made."}, 400

        for name in data['phoneme_names']:
            pid = PhonemeModel.find_by_name(name).id
            instance = PhonemeInstanceModel(pid)

            try:
                instance.save_to_db()
            except:
                return {'message': 'failed to save ({name}) instance to database.'}, 500
            
            id_list.append(instance.id)
        
        return {'id_list': id_list}
