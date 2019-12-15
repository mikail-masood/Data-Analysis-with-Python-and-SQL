""" CSC120 Assignment 2, Part 1 - Fall 2018"""
from typing import List
import sqlite3

##### CONSTANTS - do not change ######
# Database name
TTC_DB = 'ttc.db'

# Add more constants if you wish below


##### END OF CONSTANTS #######

##### Helper function for running queries #####
def run_query(db: str, db_query: str, args: tuple = None) -> List[tuple]:
    """Return the results of running query db_query on database with name db.

    Optional query argumnts for can be included in args.
    """
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    
    if args is None: 
        cur.execute(db_query)
    else:
        cur.execute(db_query, args)

    data = cur.fetchall()
    cur.close()
    con.close()
    return data
    
    
######## END OF HELPER FUNCTIONS ################


####### Data functions below ######
# These functions will require you to write SQL database queries.
# Be sure to use the run_query() helper function so that you don't need to
# set up the connections every time you want to make a query.
    
# You can assume that we will only test with valid arguments  and data 
# that appear in the TTC database.

def stop_name_for_stop_id(stop_id: int) -> str:
    """Return the stop name for the stop ID stop_id.
    
    >>> stop_name_for_stop_id(3693)
    'BLOOR ST WEST AT ST GEORGE ST'
    """
    
    query = 'SELECT stop_name FROM stops WHERE id = ?'
    return run_query(TTC_DB, query, (stop_id,))[0][0]

def get_stops_for_trip(trip_id: int) -> List[tuple]:
    """Return the stops for the trip with trip ID trip_id.
    
    >>> get_stops_for_trip(35903652)
    [(35903652, 1, '9:06:00', 15654), (35903652, 2, '9:06:17', 14619), 
    (35903652, 3, '9:06:54', 5024), (35903652, 4, '9:07:36', 4848), 
    (35903652, 5, '9:07:58', 765), (35903652, 6, '9:08:24', 8348), 
    (35903652, 7, '9:08:46', 5822), (35903652, 8, '9:09:20', 1349), 
    (35903652, 9, '9:09:42', 4270), (35903652, 10, '9:10:06', 9079), 
    (35903652, 11, '9:10:36', 7259), (35903652, 12, '9:11:07', 7080), 
    (35903652, 13, '9:11:52', 9661)]
    """
    all_trips = ' SELECT * FROM stop_times WHERE trip_id = ?'
    return run_query(TTC_DB, all_trips, (trip_id,))
    
def get_route_number_for_route(route_id: int) -> int:
    """Return the route number for the route ID route_id.
    
    >>> get_route_number_for_route(53564)
    509
    """
    query = 'SELECT number FROM routes WHERE id = ?'
    return run_query(TTC_DB, query, (route_id,))[0][0]
    
def get_route_name_for_route(route_id: int) -> str:
    """Return the route name for the route ID route_id.
    
    >>> get_route_name_for_route(53564)
    'HARBOURFRONT'
    """
    query = 'SELECT name FROM routes WHERE id = ?'
    return run_query(TTC_DB, query, (route_id,))[0][0]

def get_route_id_for_trip(trip_id: int) -> int:
    """Return the route id for the trip with trip ID trip_id.
    
    >>> get_route_id_for_trip(35902949)
    53425
    """
    query = 'SELECT route_ID FROM trips WHERE id = ?'
    return run_query(TTC_DB, query, (trip_id,))[0][0]

def get_vehicle_number_for_trip(trip_id: int) -> int:
    """Return the vehcile number for the trip with trip ID trip_id.
    
    >>> get_vehicle_number_for_trip(35903273)
    192
    """
    route = get_route_id_for_trip(trip_id)
    query = 'SELECT vehicle_number FROM vehicles where route_id = ?'
    return run_query(TTC_DB, query, (route,))[0][0]

        
def trip_details(trip_id: int, print_details: bool = False) -> None:
    '''Print the trip details for the trip with id trip_id.
    If print_details is True, also print detailed stop information.
    
    Precondition: trip_id is a valid trip ID in the database.'''
    
    # First we set variables that extract the information we want from the 
    # functions we defined above.
    route_number = get_route_number_for_route(get_route_id_for_trip(trip_id))
    route_name = get_route_name_for_route(get_route_id_for_trip(trip_id))
    vehicle_number = get_vehicle_number_for_trip(trip_id)
    
    # We use string formatting to easily print a correct statement depending 
    # on the variable given
    print("Trip details for trip {}".format(trip_id))
    print("Route: {} {}, on Vehicle #{}".format(route_number, route_name, \
                                                vehicle_number))
    print("Total Number of Stops: {}".format(len(get_stops_for_trip(trip_id))))
    
    # This is statement allows us to print the details if and only if you ask
    # the program to do so
    
    if print_details:
        print()
        i = 0
        while i < len(get_stops_for_trip(trip_id)):
            s = 'Stop {}: {} at {}'
            print(s.format(i+1, stop_name_for_stop_id(get_stops_for_trip \
            (trip_id)[i][3]), get_stops_for_trip(trip_id)[i][2]))
            i += 1
        print()
    
    print("Trip start time: {}".format(get_stops_for_trip(trip_id)[0][2]))
    print("Trip end time: {}".format(get_stops_for_trip(trip_id)\
    [len(get_stops_for_trip(trip_id)) - 1][2]))
          
    
    
    # One more newline at the end
    print() 

    
## MAIN PROGRAM
# This is where the program asks for input and prints output, and calls the
# trip_details() function you wrote above.
if __name__ == '__main__':
    
    # DO NOT change the code below    
    
    running_program = True
    
    while running_program:
        trip_id = input("Please enter a trip ID or q to quit: ")
        if trip_id == "q":
            running_program = False
        elif trip_id.isnumeric():
            show_details = input("Show stop details? y/n: ")
            if (show_details == "y"):
                trip_details(int(trip_id), True)
            else:
                trip_details(int(trip_id))
