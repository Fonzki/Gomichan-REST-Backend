from flask_restful import Resource, Api, reqparse
from models.page import PageModel

class Page(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="need title")
    parser.add_argument('lines', action='append', required=True, help="need lines")

    def get(self, id):
        page = PageModel.find_by_id(id)
        if not page:
            return {'message': f'page not defined.'}, 400

        return page.json()

    def put(self, id):
        page = PageModel.find_by_id(id)
        data = Page.parser.parse_args()

        if not page:
            page = PageModel(**data)

            try:
                page.save_to_db()
            except:
                return {'message': 'failed to save page to database.'}, 500

            return page.json(), 201

        page.title = data['title']
        page.load_lines(data['lines'])

        try:
            page.save_to_db()
        except:
            return {'message': 'failed to save page to database.'}, 500
        
        return page.json()

    def delete(self, id):
        page = PageModel.find_by_id(id)
        if page:
            page.delete_from_db()

        return {'message': f'page deleted.'}

class PageCreate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="need title")
    parser.add_argument('lines', action='append', required=True, help="need lines")

    def post(self):
        data = Page.parser.parse_args()
        page = PageModel(**data)

        try:
            page.save_to_db()
        except:
            return {'message': 'failed to save page to database.'}, 500

        return page.json(), 201

class PageList(Resource):
    def get(self):
        return {'pages': [page.json() for page in PageModel.find_all()]}
