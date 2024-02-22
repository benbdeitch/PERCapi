from . import bp as api






@api.post
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

