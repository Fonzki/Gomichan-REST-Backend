from flask_restful import Resource, Api, reqparse
from models.role_phrase import RolePhraseModel

class RolePhrase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('role', type=str, required=True, help="need role")
    parser.add_argument('note', type=str, required=True, help="need note")
    parser.add_argument('phrase', type=int, required=True, help="need phrase id")
    parser.add_argument('punctuation', type=str, required=True, help="need punctuation")

    def get(self, id):
        phrase = RolePhraseModel.find_by_id(id)
        if not phrase:
            return {'message': f'phrase not defined.'}, 400

        return phrase.json()

    def put(self, id):
        phrase = RolePhraseModel.find_by_id(id)
        data = RolePhrase.parser.parse_args()

        if not phrase:
            phrase = RolePhraseModel(**data)

            try:
                phrase.save_to_db()
            except:
                return {'message': 'failed to save phrase to database.'}, 500

            return phrase.json(), 201

        phrase.note = data['note']
        phrase.role = data['role']
        phrase.phrase = data['phrase']

        try:
            phrase.save_to_db()
        except:
            return {'message': 'failed to save phrase to database.'}, 500
        
        return phrase.json()

    def delete(self, id):
        phrase = RolePhraseModel.find_by_id(id)
        if phrase:
            phrase.delete_from_db()

        return {'message': f'phrase deleted.'}

class RolePhraseByRole(Resource):
    def get(self, role):
        return {'role_phrases': [role_phrase.json() for role_phrase in RolePhraseModel.find_by_role(role)]}

class RolePhraseCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('role', type=str, required=True, help="need role")
    parser.add_argument('note', type=str, required=True, help="need note")
    parser.add_argument('phrase', type=int, required=True, help="need phrase id")

    def post(self):
        data = RolePhrase.parser.parse_args()
        phrase = RolePhraseModel(**data)

        try:
            phrase.save_to_db()
        except:
            return {'message': 'failed to save phrase to database.'}, 500

        return phrase.json(), 201

class RolePhraseList(Resource):
    def get(self):
        return {'role_phrases': [role_phrase.json() for role_phrase in RolePhraseModel.find_all()]}
