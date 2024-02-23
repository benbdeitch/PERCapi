from flask_jwt_extended import jwt_required
from . import bp as api

#This File adds routes that handle adding and retrieving information from the database. 




@api.post('/add-entry')
@jwt_required()
def add_pending_entry(request):
    """ Accepts requests of the form: 
    {[
        {
            "name": String,
            "street_number": Integer,
            "street_name": String,
            "state": String,
            "website": String
        }
    ]
} """
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