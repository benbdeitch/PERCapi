from app import db
from app.models import EmergRoom, Address, State, Confirmation

#These helper functions are used to ease the process of fetching the emergency rooms from the database. 



def get_rooms_by_state(state):
    state_id = State.query.filter_by()