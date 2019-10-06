from test_intelimetrica import app
from .models.restaurant import get_all_restaurants as get_restaurants_db
from .models.restaurant import create_new_restaurant as create_new_restaurant_db
from .models.restaurant import update_all_restaurants as update_all_restaurants_db
from .models.restaurant import erase_all_restaurants as erase_all_restaurants_db
from .models.restaurant import get_one_restaurant, update_one_restaurant, delete_one_restaurant, search_radius
from .utils.statistics import get_average_rating, get_standard_deviation
from flask import jsonify, request


# The route /api/restaurants is used to obtain the interact with the Restaurants table from the database

# It only allows the GET http verb
# It returns JSON data containing an array of all restaurants
# Example request [GET /api/restaurants]
# Example response: Success: [{"city": "Mérida Alfredotown", "email": "Anita_Mata71@hotmail.com",
#         "id": "851f799f-0852-439e-b9b2-df92c43e7672", "lat": 19.4400570537131, "lng": -99.1270470974249,
#         "name": "Barajas, Bahena and Kano", "phone": "534 814 204", "rating": 1, "site": "https://federico.com",
#         "state": "Durango", "street": "82247 Mariano Entrada"},
#         {"city": "Mateofurt", "email": "Brandon_Vigil@hotmail.com", "id": "4e17896d-a26f-44ae-a8a4-5fbd5cde79b0",
#          "lat": 19.437904276995, "lng": -99.1286576775023, "name": "Hernández - Lira", "phone": "570 746 998",
#          "rating": 0, "site": "http://graciela.com.mx", "state": "Hidalgo", "street": "93725 Erick Arroyo"
#          }, ... ]
#                   Fail: {'message': 'Internal Server Error'}
@app.route('/api/restaurants', methods=['GET'])
def get_all_restaurants():
    try:
        list_restaurants = get_restaurants_db(request.args)
    except:
        # TODO: Handle models exceptions properly
        return {'message': 'Internal Server Error'}, 500
    return jsonify(list_restaurants)


# This route will only accept the POST http verb
# It creates a new restaurant row using the information contained in the form data
# For the moment this route only allows to create a new restaurant when all its information is known
# Example request [POST /api/restaurants]
# Example response: Success: {'message': 'The restaurant was created correctly'}
#                   Fail: {'message': 'Internal Server Error'} or {'message': 'Missing Form Data'}
@app.route('/api/restaurants', methods=['POST'])
def create_new_restaurant():
    try:
        args = {'id': request.form['id'], 'rating': request.form['rating'], 'name': request.form['name'],
                'site': request.form['site'], 'email': request.form['email'],
                'phone': request.form['phone'], 'street': request.form['street'], 'city': request.form['city'],
                'state': request.form['state'], 'lat': request.form['lat'], 'lng': request.form['lng']}
    except:
        return {'message': 'Missing Form Data'}, 400
    try:
        create_new_restaurant_db(args)
    except:
        # TODO: Handle models exceptions properly
        return {'message': 'Internal Server Error'}, 500

    return {'message': 'The restaurant was created correctly'}, 201


# This route will only accept the PUT http verb
# It updates all the restaurants according to the parameters in the URL
# Example request [PUT /api/restaurants?rating=3]
# Example response: Success: {'message': 'Bulk update processed'}
#                   Fail: {'message': 'Internal Server Error'} or {'message': 'No parameters were passed'}
@app.route('/api/restaurants', methods=['PUT'])
def update_all_restaurants():
    try:
        # Checks if any parameters were passed and if not it raises an exception
        if len(request.args) == 0:
            return {'message': 'No parameters were passed'}, 400

        update_all_restaurants_db(request.args)
    except:
        # TODO: Handle each database exception properly
        return {'message': 'Internal Server Error'}, 500
    return {'message': 'Bulk update processed'}


# This route will only accept the DELETE http verb
# This route deletes all restaurant entries in the database. It will leave the empty Restaurants table that can be
# loaded with initial data using the ./util/load_database.py script
# Example request [DELETE /api/restaurants]
# Example response: Success: {'message': 'Successfully erased all restaurant entries.'}
#                   Fail: {'message': 'Internal Server Error'}
@app.route('/api/restaurants', methods=['DELETE'])
def delete_all_restaurants():
    try:
        erase_all_restaurants_db()
    except:
        return {'message': 'Internal Server Error'}, 500
    return {'message': 'Successfully erased all restaurant entries.'}


# This route will only accept the GET http verb
# This route is used to obtain the information of a certain restaurant that is identified by its id
# Example request [GET /api/restaurants/030eaf75-da6e-4748-9727-f2704f831498]
# Example response: Success: {"city": "Querétaro Saratown", "email": "Luz_Sevilla@gmail.com",
#                             "id": "030eaf75-da6e-4748-9727-f2704f831498", "lat": 19.4416814748901,
#                             "lng": -99.1265732438097, "name": "Niño - Negrete", "phone": "5178-668-409",
#                             "rating": 2, "site": "https://elizabeth.gob.mx", "state": "Oaxaca",
#                             "street": "3041 Gael Torrente"}
#                   Fail: {'message': 'Internal Server Error'}
@app.route('/api/restaurants/<id>', methods=['GET'])
def retrieve_restaurant(id):
    # Get restaurant from the database
    try:
        restaurant = get_one_restaurant(id)
    except:
        return {'message': 'Internal Server Error'}, 500
    # Send the restaurant back
    return jsonify(restaurant)


# This route will only accept the PUT http verb
# This route is used to update the information of a certain restaurant that is identified by its id
# Example request [PUT /api/restaurants/030eaf75-da6e-4748-9727-f2704f831498]
# Example response: Success: {'message': 'Restaurant with id 030eaf75-da6e-4748-9727-f2704f831498 has been updated'}
#                   Fail: {'message': 'Internal Server Error'}
@app.route('/api/restaurants/<id>', methods=['PUT'])
def update_restaurant(id):
    try:
        # Checks if any parameters were passed and if not it raises an exception
        if len(request.args) == 0:
            return {'message': 'No parameters were passed'}, 400

        update_one_restaurant(request.args, id)
    except:
        # TODO: Handle each database exception properly
        return {'message': 'Internal Server Error'}, 500
    return {'message': 'Restaurant with id {} has been updated'.format(id)}


# This route will only accept the DELETE http verb
# This route is used to update the information of a certain restaurant that is identified by its id
# Example request [DELETE /api/restaurants/030eaf75-da6e-4748-9727-f2704f831498]
# Example response: Success: {'message': 'Restaurant with id 030eaf75-da6e-4748-9727-f2704f831498 has been deleted'}
#                   Fail: {'message': 'Internal Server Error'}
@app.route('/api/restaurants/<id>', methods=['DELETE'])
def delete_restaurant(id):
    try:
        delete_one_restaurant(id)
    except:
        # TODO: Handle each database exception properly
        return {'message': 'Internal Server Error'}, 500
    return {'message': 'Restaurant with id {} has been deleted'.format(id)}


# This route will only accept the GET http verb
# This route is used to obtain the statistic information of the restaurants contained in a radius
# Example request [GET /restaurants/statistics/?latitude=19.4380931173689&longitude=-99.1334110923394&radius=4500]
# Example response: Success: {"avg": 1.72, "count": 100, "std": 1.4496896219536104}
#                   Fail: {'message': 'Internal Server Error'} or {'message': 'Missing parameters'}
@app.route('/restaurants/statistics', methods=['GET'])
def radius_search_statistics():
    if ('latitude' in request.args) and ('longitude' in request.args) and ('radius' in request.args):
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius')
    else:
        return {'message': 'Missing parameters'}, 400

    try:
        list_restaurants = search_radius(latitude, longitude, radius)
    except:
        # TODO: Handle each database exception properly
        return {'message': 'Internal Server Error'}, 500
    # Check if there are restaurants within the circle if not return a count of 0 and N/A for all other parameters
    if len(list_restaurants) == 0:
        return {'count': 0, 'avg': 'N/A', 'std': 'N/A'}, 400

    # Once obtained the list with the required restaurants we can statistically analyze them
    # Obtain the average using the function in the utils module
    average = get_average_rating(list_restaurants)
    # Obtain the standard deviation using the function in the utils module
    standard_deviation = get_standard_deviation(list_restaurants, average)

    # return results
    return {'count': len(list_restaurants), 'avg': average, 'std': standard_deviation}
