""" CSC120 Assignment 2, Part 2 - 2018 Fall"""
from typing import List, Dict, Tuple
import sqlite3
import numpy as np
from matplotlib import pyplot as plt

##### CONSTANTS - do not change ######
# Database name
DELAYS_DB = 'delays.db'
# Months
MONTHS = ['sept2017', 'oct2017', 'nov2017', 'dec2017', 'jan2018', 'feb2018']

# Add more constants as needed below.



######## END OF CONSTANTS ################

##### Helper functions #####

# Helper function to run queries
def run_query(db: str, db_query: str, args: tuple = None) -> List[tuple]:
    '''Return the results of running query db_query on database with name db.

    Optional query arguments for can be included in args.
    '''
    
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

# Write your own helper functions below.


def total_delays(db: str, month: int) -> List[tuple]:
    '''Returns the total minutes delayed in each day of month '''
    
    query = """SELECT day, sum(minutes) 
              FROM delays WHERE month = ? 
              GROUP BY day
              ORDER BY CASE
                  WHEN day = 'Monday' THEN 1
                  WHEN day = 'Tuesday' THEN 2
                  WHEN day = 'Wednesday' THEN 3
                  WHEN day = 'Thursday' THEN 4
                  WHEN day = 'Friday' THEN 5
                  WHEN day = 'Saturday' THEN 6
                  WHEN day = 'Sunday' THEN 7
                END ASC
                  """
    total_delay_per_month = run_query(db, query, (MONTHS[month],))
    x = []
    y = []
    for sublist in total_delay_per_month:
        x.append(sublist[0])
        y.append(sublist[1])
    x_ordered = []
    for strings in x:
        x_ordered.append(strings[0:3])
    return x_ordered, y
        
def max_delays(db: str, month: int) -> List[tuple]:
    ''' Return the maximum 5 stations with the most delays in minutes in a given
    month'''
    
    query = '''SELECT DISTINCT station, SUM(minutes) as total_delays 
               FROM delays WHERE month = ?
               GROUP BY station
               ORDER BY total_delays DESC'''
    top_5_delays = run_query(db, query, (MONTHS[month],))[0:5]
    x = []
    y = []
    for tuples in top_5_delays:
        x.append(tuples[0])
        y.append(tuples[1])
    return x, y

def avg_mins_by_month(db: str)-> List[tuple]:
    """ Return the average minutes of delays in each month"""
    query = """SELECT month, AVG(minutes)
               FROM delays
               GROUP BY month
                ORDER BY CASE
                  WHEN month = 'sept2017' THEN 1
                  WHEN month = 'oct2017' THEN 2
                  WHEN month = 'nov2017' THEN 3
                  WHEN month = 'dec2017' THEN 4
                  WHEN month = 'jan2018' THEN 5
                  WHEN month = 'feb2018' THEN 6
                END ASC"""
    return run_query(db, query)

def num_delays(db: str) -> List[tuple]:
    """ Returns the total number of delays for each month"""
    query = """SELECT month, COUNT(month)
                FROM delays
                GROUP BY month
                ORDER BY CASE
                  WHEN month = 'sept2017' THEN 1
                  WHEN month = 'oct2017' THEN 2
                  WHEN month = 'nov2017' THEN 3
                  WHEN month = 'dec2017' THEN 4
                  WHEN month = 'jan2018' THEN 5
                  WHEN month = 'feb2018' THEN 6
                END ASC"""
    return run_query(db, query)

def longest_overall_delays(db: str) -> List[tuple]:
    """Return the longest total delays for each stations in all months"""
    query = """SELECT station, SUM(minutes) AS total_delays
               FROM delays
               GROUP BY station
               ORDER BY total_delays DESC"""
    return run_query(db, query)[0:5]

def delays_per_hour(db: str, month: int) -> None:
    """Returns a list of tuples with the times of the delay for every month """
    # This helper function allows to have a variable that contains a list of
    # tuples with the hours of each delays for that month
    query = '''SELECT time
               FROM delays
               Where month = ?'''
    return run_query(db, query, (MONTHS[month],))
    
def tuples_to_int(monthly_delays: List[tuple]) -> List[int]:
    """This helper function allows me to turn the list of tuples that I have 
    extraced from the helper funciton above into a list of integers that can 
    consider as the x values for my hist graph using a while loop"""
    
    # We use a while loop to convert the strings into ints by removing the 
    # columns from the strings, converting it to an int so it values can easily 
    # be represented in an histogram.
    
    i = 0
    x_month = []
    monthly_delays.sort()
    while i < len(monthly_delays):
        x_month.append(int(monthly_delays[i][0].replace(':', '')) / 100)
        i += 1
    return x_month



######## END OF HELPER FUNCTIONS ################

######## PLOTTING FUNCTIONS ################
# Write your plotting functions below (only these functions should directly 
# graph and save plots).

def day_delays(db: str) -> None:
    """Creates bar plots for the total minutes delayed on each day in each of 
    the 6months from database db
    """
    # Creating x and y variables for each month using the helper function
    # total_delays to get the cumalative minutes of delays on each day. 
    month_1 = [total_delays(db, 0)]
    month_2 = [total_delays(db, 1)]
    month_3 = [total_delays(db, 2)]
    month_4 = [total_delays(db, 3)]
    month_5 = [total_delays(db, 4)]
    month_6 = [total_delays(db, 5)]
    
    # using the variables to plot bar graphs of each month.
    plt.figure(figsize=(14, 17))
    plt.xticks(fontsize=30)
    
    plt.subplot(2, 3, 1)
    plt.xlabel('Day')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Sept 2017') 
    plt.bar(month_1[0][0], month_1[0][1])
    
    plt.subplot(2, 3, 2)
    plt.xlabel('Day')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Oct 2017')
    plt.bar(month_2[0][0], month_2[0][1])  
    
    plt.subplot(2, 3, 3)
    plt.xlabel('Day')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Nov 2017')
    plt.bar(month_3[0][0], month_3[0][1]) 
    
    plt.subplot(2, 3, 4)
    plt.xlabel('Day')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Dec 2017')
    plt.bar(month_4[0][0], month_4[0][1])    
    
    plt.subplot(2, 3, 5)
    plt.xlabel('Day')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Jan 2018')
    plt.bar(month_5[0][0], month_5[0][1])
    
    plt.subplot(2, 3, 6)
    plt.xlabel('Day')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Feb 2018')
    plt.bar(month_6[0][0], month_6[0][1])
    
    plt.tight_layout()
    plt.savefig('day_delays.png')
    plt.close()
def week_top_five(db: str) -> None:
    """Creates bar plots of the five stations with the longest overall delays
    ineach of the 6 months.
    """
    # Creating x and y variables for each month using the helper function
    # max_delays to get the five stations with the longest overall delays
    month_1 = [max_delays(db, 0)]
    month_2 = [max_delays(db, 1)]
    month_3 = [max_delays(db, 2)]
    month_4 = [max_delays(db, 3)]
    month_5 = [max_delays(db, 4)]
    month_6 = [max_delays(db, 5)]
    
    # using the variables to plot bar graphs of each month.
    plt.figure(figsize=(35, 20)) 
    plt.xticks(fontsize=20)    
    
    plt.subplot(2, 3, 1)
    plt.xlabel('Station')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Sept 2017')    
    plt.bar(month_1[0][0], month_1[0][1])
    
    plt.subplot(2, 3, 2)
    plt.xlabel('Station')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Oct 2017')    
    plt.bar(month_2[0][0], month_2[0][1])  
    
    plt.subplot(2, 3, 3)
    plt.xlabel('Station')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Nov 2017')     
    plt.bar(month_3[0][0], month_3[0][1]) 
    
    plt.subplot(2, 3, 4)
    plt.xlabel('Station')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Dec 2017')     
    plt.bar(month_4[0][0], month_4[0][1])    
   
    plt.subplot(2, 3, 5)
    plt.xlabel('Station')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Jan 2018')     
    plt.bar(month_5[0][0], month_5[0][1])
    
    plt.subplot(2, 3, 6)
    plt.xlabel('Station')
    plt.ylabel('Total Time of Delays (minutes)')    
    plt.title('Feb 2018')     
    plt.bar(month_6[0][0], month_6[0][1])     
    
    plt.tight_layout()
    plt.savefig('week_top_five.png')
    plt.close()

def delays_per_hour_histogram(db: str) -> None: 
    """ Return an historgram of the number of delays that occur during during
    each hour of each day, for all days combined for that month"""
    
    # We start by setting the general dimensions of the function
    plt.figure(figsize=(35, 20)) 
    plt.xticks(fontsize=25)       
    
    # We then use the built in plt subplot functions to plot 6 graphs for each 
    # month. We get the x values for this histogram using the helper functions
    # tuples_to int
    
    plt.subplot(2, 3, 1)
    plt.xlabel('Hour of the day')
    plt.ylabel('Number of delays')
    plt.title('Sep 2017')
    plt.hist(tuples_to_int(delays_per_hour(db, 0)), bins=np.arange(0, 25, 1))
    plt.xticks(np.arange(0, 24, 1.0))
    
    plt.subplot(2, 3, 2)
    plt.xlabel('Hour of the day')
    plt.ylabel('Number of delays')
    plt.title('Oct 2017')
    plt.hist(tuples_to_int(delays_per_hour(db, 1)), bins=np.arange(0, 25, 1))
    plt.xticks(np.arange(0, 24, 1.0))
    
    plt.subplot(2, 3, 3)
    plt.xlabel('Hour of the day')
    plt.ylabel('Number of delays')
    plt.title('Nov 2017')
    plt.hist(tuples_to_int(delays_per_hour(db, 2)), bins=np.arange(0, 25, 1))
    plt.xticks(np.arange(0, 24, 1.0))
    
    plt.subplot(2, 3, 4)
    plt.xlabel('Hour of the day')
    plt.ylabel('Number of delays')
    plt.title('Dec 2017')
    plt.hist(tuples_to_int(delays_per_hour(db, 3)), bins=np.arange(0, 25, 1))
    plt.xticks(np.arange(0, 24, 1.0))
    
    plt.subplot(2, 3, 5)
    plt.xlabel('Hour of the day')
    plt.ylabel('Number of delays')
    plt.title('Jan 2018')
    plt.hist(tuples_to_int(delays_per_hour(db, 4)), bins=np.arange(0, 25, 1))
    plt.xticks(np.arange(0, 24, 1.0))    
    
    plt.subplot(2, 3, 6)
    plt.xlabel('Hour of the day')
    plt.ylabel('Number of delays')
    plt.title('Feb 2018')
    plt.hist(tuples_to_int(delays_per_hour(db, 5)), bins=np.arange(0, 25, 1))
    plt.xticks(np.arange(0, 24, 1.0))        

    plt.tight_layout()    
    plt.savefig('hour_delays.png')
    plt.close()
        

def month_avg_minutes(db: str) -> None:
    '''Creates a bar plot of the average length of delays during each month'''
    # using the helper function abg_minutes_by_month we create the x and y 
    # variables
    x = []
    y = []
    for tuples in avg_mins_by_month(db):
        x.append(tuples[0])
        y.append(tuples[1])
    # plot the bar graph of month vs Delays
    plt.bar(x, y)
    plt.title('Average Length of Delays During Each Month', fontsize=15)
    plt.xlabel('Month')
    plt.ylabel('Time of Delays (Minutes)') 
    plt.tight_layout()
    plt.savefig('month_avg_minutes.png')
    plt.close()
    
def month_delays(db: str) -> None:
    """Creates a bar plot of the total number of delays during each month"""
    # Using the helper function num_delays we get the x and y variables of 
    # month and the corresponding number of delays in each month 
    x = []
    y = []
    for tuples in num_delays(db):
        x.append(tuples[0])
        y.append(tuples[1])
    # plotting the graph
    plt.bar(x, y)
    plt.title('Total number of Delays During Each Month', fontsize=15)
    plt.xlabel('Month')
    plt.ylabel('Total Number of Delays')
    plt.tight_layout()
    plt.savefig('month_delays.png')
    plt.close()
    
def month_top_five(db: str) -> None:
    """Creates a bar plot for the five station with longest overall delays over
    the 6 months.
    """
    # using the helper function longest_oveerall_delays, we create the x and y 
    # variables the 5 stations with the longest overall delays
    x = []
    y = []
    for tuples in longest_overall_delays(db):
        x.append(tuples[0])
        y.append(tuples[1])
    # Plotting the graph
    plt.figure(figsize=(20, 16))
    plt.xticks(fontsize=15)
    plt.title('Top Five Stations with The Longest \
    Cumalative Delays Over 6 Months'
              , fontsize=20)
    plt.xlabel('Station')
    plt.ylabel('Total Time of Delays (minutes)')
    plt.bar(x, y)
    plt.tight_layout()
    plt.savefig('month_top_five.png')
    
######## END OF PLOTTING FUNCTIONS ################

######## MAIN BLOCK BELOW ###########
# When we run your code, the main block below should plot your graphs and save
# your plots.

if __name__ == '__main__':
    # Write your main block below
    day_delays(DELAYS_DB)
    week_top_five(DELAYS_DB)
    delays_per_hour_histogram(DELAYS_DB)
    month_avg_minutes(DELAYS_DB)
    month_delays(DELAYS_DB)
    month_top_five(DELAYS_DB)