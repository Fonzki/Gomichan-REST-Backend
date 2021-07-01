from flask_restful import Resource, Api, reqparse
from models.line import LineModel

class Line(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('translation', type=str, required=True, help="need translation")
    parser.add_argument('video_link', type=str, required=True, help="need video link")
    parser.add_argument('start', type=float, required=True, help="need start time")
    parser.add_argument('duration', type=float, required=True, help="need duration")
    parser.add_argument('role_phrases', action='append', required=True, help="need role phrases")

    def get(self, id):
        line = LineModel.find_by_id(id)
        if not line:
            return {'message': f'line not defined.'}, 400

        return {'line':line.json()}, 200

    def put(self, id):
        line = LineModel.find_by_id(id)
        data = Line.parser.parse_args()

        if not line:
            line = LineModel(**data)

            try:
                line.save_to_db()
            except:
                return {'message': 'failed to save line to database.'}, 500

            return line.json(), 201

        line.translation = data['translation']
        line.video_link = data['video_link']
        line.start = data['start']
        line.duration = data['duration']
        line.load_role_phrases(data['role_phrases'])

        try:
            line.save_to_db()
        except:
            return {'message': 'failed to save line to database.'}, 500
        
        return line.json()

    def delete(self, id):
        line = LineModel.find_by_id(id)
        if line:
            line.delete_from_db()

        return {'message': f'line deleted.'}

class LineCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('translation', type=str, required=True, help="need translation")
    parser.add_argument('video_link', type=str, required=True, help="need video link")
    parser.add_argument('start', type=float, required=True, help="need start time")
    parser.add_argument('duration', type=float, required=True, help="need duration")
    parser.add_argument('role_phrases', type=int, action='append', required=True, help="need role phrases")

    def post(self):
        data = Line.parser.parse_args()
        line = LineModel(**data)

        print(data['role_phrases'])

        try:
            line.save_to_db()
        except Exception as error:
            print(error)
            return {'message': 'failed to save line to database.'}, 500

        return line.json(), 201

class LineList(Resource):
    def get(self):
        return {'lines': [line.json() for line in LineModel.find_all()]}
