from app import db
from app.models import EmergRoom, Address, Confirmation
import json 
#These helper functions are used to ease the process of fetching the emergency rooms from the database. 

neighboring_states = {'AK': ['WA', 'AK'], 
                      'AL': ['FL', 'GA', 'MS', 'TN', 'AL'], 
                      'AR': ['LA', 'MO', 'MS', 'OK', 'TN', 'TX', 'AR'], 
                      'AZ': ['CA', 'CO', 'NM', 'NV', 'UT', 'AZ'], 
                      'CA': ['AZ', 'HI', 'NV', 'OR', 'CA'], 
                      'CO': ['AZ', 'KS', 'NE', 'NM', 'OK', 'UT', 'WY', 'CO'], 
                      'CT': ['MA', 'NY', 'RI', 'CT'], 
                      'DC': ['MD', 'VA', 'DC'], 
                      'DE': ['MD', 'NJ', 'PA', 'DE'], 
                      'FL': ['AL', 'GA', 'FL'], 
                      'GA': ['AL', 'FL', 'NC', 'SC', 'TN', 'GA'], 
                      'HI': ['CA', 'HI'], 
                      'IA': ['IL', 'MN', 'MO', 'NE', 'SD', 'WI', 'IA'], 
                      'ID': ['MT', 'NV', 'OR', 'UT', 'WA', 'WY', 'ID'], 
                      'IL': ['IA', 'IN', 'KY', 'MO', 'WI', 'IL'], 
                      'IN': ['IL', 'KY', 'MO', 'WI', 'IN'], 
                      'KS': ['CO', 'MO', 'NE', 'OK', 'KS'], 
                      'KY': ['IL', 'IN', 'MO', 'OH', 'TN', 'VA', 'WV', 'KY'], 
                      'LA': ['AR', 'MS', 'TX', 'LA'], 
                      'MA': ['CT', 'NH', 'NY', 'RI', 'VT', 'MA'], 
                      'MD': ['DC', 'DE', 'PA', 'VA', 'WV', 'MD'], 
                      'ME': ['NH', 'ME'], 
                      'MI': ['IN', 'OH', 'WI', 'MI'], 
                      'MN': ['IA', 'ND', 'SD', 'WI', 'MN'], 
                      'MO': ['AR', 'IA', 'IL', 'KS', 'KY', 'NE', 'OK', 'TN', 'MO'], 
                      'MS': ['AL', 'AR', 'LA', 'TN', 'MS'], 
                      'MT': ['ID', 'ND', 'SD', 'WY', 'MT'], 
                      'NC': ['GA', 'SC', 'TN', 'VA', 'NC'], 
                      'ND': ['MN', 'MT', 'SD', 'ND'], 
                      'NE': ['CO', 'IA', 'KS', 'MO', 'SD', 'WY', 'NE'], 
                      'NH': ['MA', 'ME', 'VT', 'NH'], 
                      'NJ': ['DE', 'NY', 'PA', 'NJ'], 
                      'NM': ['AZ', 'CO', 'OK', 'TX', 'UT', 'NM'], 
                      'NV': ['AZ', 'CA', 'ID', 'OR', 'UT', 'NV'], 
                      'NY': ['CT', 'MA', 'NJ', 'PA', 'VT', 'NY'], 
                      'OH': ['IN', 'KY', 'MI', 'PA', 'WV', 'OH'], 
                      'OK': ['AR', 'CO', 'KS', 'MO', 'NM', 'TX', 'OK'], 
                      'OR': ['CA', 'ID', 'NV', 'WA', 'OR'], 
                      'PA': ['DE', 'MD', 'NJ', 'NY', 'OH', 'WV', 'PA'], 
                      'RI': ['CT', 'MA', 'RI'], 
                      'SC': ['GA', 'NC', 'SC'], 
                      'SD': ['IA', 'MN', 'MT', 'ND', 'NE', 'WY', 'SD'], 
                      'TN': ['AL', 'AR', 'GA', 'KY', 'MO', 'MS', 'NC', 'VA', 'TN'], 
                      'TX': ['AR', 'LA', 'NM', 'OK', 'TX'], 
                      'UT': ['AZ', 'CO', 'ID', 'NM', 'NV', 'WY', 'UT'], 
                      'VA': ['DC', 'KY', 'MD', 'NC', 'TN', 'WV', 'VA'], 
                      'VT': ['MA', 'NH', 'NY', 'VT'], 
                      'WA': ['AK', 'ID', 'OR', 'WA'], 
                      'WI': ['IA', 'IL', 'MI', 'MN', 'WI'], 
                      'WV': ['KY', 'MD', 'OH', 'PA', 'VA', 'WV'], 
                      'WY': ['CO', 'ID', 'MT', 'NE', 'SD', 'UT', 'WY']}





def get_state_neighbors(state):
    return neighboring_states

def get_rooms_by_state(state):
    
