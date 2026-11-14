from flask_restful import Resource, Api, fields, marshal_with, abort, reqparse, inputs
from main import db, app, Cafe


# TODO: Step 2 - Wake up the API manager by connecting Flask-RESTful to your app
api = Api(app)

# TODO: Step 3 - Write the security guard's rulebook using RequestParser and add_argument for your fields

# Add your arguments here (name, map_url, img_url, location, seats, etc.)

cafe_args = reqparse.RequestParser()
cafe_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
cafe_args.add_argument('map_url', type=str, required=True, help="Map URL cannot be blank")
cafe_args.add_argument('img_url', type=str, required=True, help="Image URL cannot be blank")
cafe_args.add_argument('location', type=str, required=True, help="Location cannot be blank")
cafe_args.add_argument('seats', type=str, required=True, help="Seats info cannot be blank")
cafe_args.add_argument('has_toilet', type=inputs.boolean, required=True, help="Toilet availability is required (True/False)")
cafe_args.add_argument('has_wifi', type=inputs.boolean, required=True, help="WiFi availability is required (True/False)")
cafe_args.add_argument('has_sockets', type=inputs.boolean, required=True, help="Socket availability is required (True/False)")
cafe_args.add_argument('can_take_calls', type=inputs.boolean, required=True, help="Call capability is required (True/False)")
cafe_args.add_argument('coffee_price', type=str, required=False, help="Coffee price info")
# TODO: Step 4 - Pack the lunchbox by creating the cafe_fields dictionary for clean JSON responses

# Define fields here (id, name, map_url, etc.)
cafe_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'map_url': fields.String,
    'img_url': fields.String,
    'location': fields.String,
    'seats': fields.String,
    'has_toilet': fields.Boolean,
    'has_wifi': fields.Boolean,
    'has_sockets': fields.Boolean,
    'can_take_calls': fields.Boolean,
    'coffee_price': fields.String,
}



# TODO: Step 5 - Build the headquarters for ALL cafes (Cafes Resource class with get and post methods)
class Cafes(Resource):
    @marshal_with(cafe_fields)
    def get(self):
        # TODO: Write code to fetch all cafes from the database and return them
        all_cafes = Cafe.query.all()
        return all_cafes

    @marshal_with(cafe_fields)
    def post(self):
        # TODO: Write code to parse arguments, create a new cafe, add it to the db, and commit
        args = cafe_args.parse_args()
        new_cafe = Cafe(
            name=args['name'],
            map_url=args['map_url'],
            img_url=args['img_url'],
            location=args['location'],
            seats=args['seats'],
            has_toilet=args['has_toilet'],
            has_wifi=args['has_wifi'],
            has_sockets=args['has_sockets'],
            can_take_calls=args['can_take_calls'],
            coffee_price=args['coffee_price']
        )
        db.session.add(new_cafe)
        db.session.commit()
        return new_cafe, 201



# TODO: Step 6 - Build the house for a SINGLE cafe (SingleCafe Resource class with get, put, and delete methods)
class SingleCafe(Resource):
    @marshal_with(cafe_fields)
    def get(self, cafe_id):
        # TODO: Write code to fetch a single cafe by ID or return a 404 error
        cafe = db.get_or_404(Cafe,cafe_id)
        return cafe

    @marshal_with(cafe_fields)
    def put(self, cafe_id):
        # TODO: Write code to update an existing cafe by ID
        args = cafe_args.parse_args()
        cafe = db.get_or_404(Cafe,cafe_id)
        cafe.name = args['name']
        cafe.map_url = args['map_url']
        cafe.img_url = args['img_url']
        cafe.location = args['location']
        cafe.seats = args['seats']
        cafe.has_toilet = args['has_toilet']
        cafe.has_wifi = args['has_wifi']
        cafe.has_sockets = args['has_sockets']
        cafe.can_take_calls = args['can_take_calls']
        cafe.coffee_price = args['coffee_price']
        db.session.commit()
        return cafe, 200

    def delete(self, cafe_id):
        # TODO: Write code to delete a cafe by ID and return a 204 status code
        cafe = db.get_or_404(Cafe, cafe_id)
        db.session.delete(cafe)
        db.session.commit()
        return '', 204


# TODO: Step 7 - Give your API street addresses using api.add_resource()
api.add_resource(Cafes, '/api/cafes/')
api.add_resource(SingleCafe, '/api/cafes/<int:cafe_id>/')


# TODO: Step 8 - Turn on the machine with app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)