from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import EmergRoom, User, Pending, Address
from . import bp as api

#This File handles routes that are related to the pending entries




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



@api.get('/get-pending')
@jwt_required()
def get_pending_entries():
    response = {}
    username = get_jwt_identity()
    user = User.query.filter_by(username = username).first()
    if user.admin:
        pending = Pending.query.all()
        response = {"entries": []}
        for entry in pending:
            response["entries"].append(entry.to_dict())
    else:
        response["error"] = "Error, User: %s does not have authorized access" % username
    return jsonify(response)

@api.post('/approve_pending')
@jwt_required()
def approve_pending_entry():
    data = request.json
    username = get_jwt_identity()
    user = User.query.filter_by(username = username).first()
    response = {}
    if user and user.admin:
        #convert pending information to address/emergency room, checking to see if data is duplicated. 
        #Then commit them to the tables, and calculate the google PlaceID for the address. 
        #Then return a message if it was successful. 
        pending_entry = Pending.query.filter_by(id = data["id"]).first()
        if not pending_entry:
            response["error"] = "Error, pending entry of id %s could not be found." % data["id"]
            return response
        address = Address(name = pending_entry.street_name, number = pending_entry.street_number, city = pending_entry.city, zipcode = pending_entry.zipcode, state = pending_entry.state)
        check = Address.query.filter_by(name = address.name, number = address.number, city = address.city, zipcode = address.zipcode, state = address.state).first()
        if check:
            address = check
        else:
            address.commit()

        emerg_room = EmergRoom(name = pending_entry.name, address = address.id, phone= pending_entry.phone_number, website = pending_entry.website)
        emerg_room.commit()

        return jsonify({"Success": "Emergency Room %s has been successfully added." % emerg_room.name})
    return jsonify({"error": "user of username %s does not exist, or is lacking in admin permissions." % username})

@api.post('/delete_pending')
@jwt_required()
def delete_pending_entry():
    #accepts an id and checks for admin. If the user is an admin, deletes the entry from the pending table.
    pass