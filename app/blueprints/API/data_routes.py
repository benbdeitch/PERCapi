from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import User, Pending
from . import bp as api

#This File adds routes that handle adding and retrieving information from the database. 




@api.post('/add-entry')
@jwt_required()
def add_pending_entry():
    """ Accepts requests of the form: 
    {[
        {
            "name": String,
            "street_number": Integer,
            "street_name": String,
            "city": string,
            "zipcode":
            "state": String,
            "phone_number": String
            "website": String
        }
    ]
} """
    data = request.json
    print(type(data))
    username = get_jwt_identity()
    user = User.query.filter_by(username = username).first()
    try:
        entry = Pending(name = data.get("name"), 
                        street_number = int(data.get("street_number")), 
                        street_name = data.get("street_name"),
                        state = data.get("state"),
                        city = data.get("city"),
                        zipcode = int(data.get("zipcode")),
                        phone_number = data.get("phone_number"),
                        website = data.get("website"),
                        uploader = user.id)
        entry.commit()
        return jsonify({"Success": f'New Entry for {data["name"]} has been added to our pending table.'}),200
    #TODO: replace this error return with something more informative. 
    except:
         return jsonify({"Error": "Improperly formatted request."}), 400


@api.post('/approve_entry')
@jwt_required()
def approve_pending_entry():
    pass


@api.post('/get-by-state')
@jwt_required()
def get_data_by_state(request):
    """Returns all current emergency rooms for a given state in JSON format
    State is required to be in a 2 letter Abbreviation format for proper response."""
    pass

@api.post('/get-rooms')
@jwt_required()
def get_emergency_rooms(request):
    """Like get_data_by_state, except that it will also grab all pediatric emergency room data for neighboring
    states as well.  This should be the default route used, for accessing this information.""" 
    pass