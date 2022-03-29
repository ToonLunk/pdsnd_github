from cmath import nan
import time
import pandas as pd
import numpy as np # for quick maths!

# this is a dictionary mapping all of the city data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# create a list of months
months = ['january', 'february','march','april','may','june']

# create a list of days
days = ['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']

# create an error message here so I can change it in one place
invalid_user_input = "\nWARNING: That selection is not valid, please try again."

def list_to_str(a_list):
    """ I made this quick function to quickly return lists as strings, with a separator. Accepts
    a list and returns an easily-printable string, separated by commas."""
    # make an empty string
    a_string = ""
    
    # loop through each item. if it isn't the last, add a comma. if it is, add item, then return the string.
    for item in a_list:
        if item != a_list[-1]:
            a_string += item.title() + ", "
        else:
            a_string += item.title()
    return a_string

def view_data (df):
    """
    This will print the raw data 5 lines at a time as requested in the rubric.
    """
    df['Row Number'] = np.arange(len(df))
    
    line_count = 5 # to print out 5 lines at a time
    # lines_left holds how many lines are left in the raw data
    lines_left = 0
    #lines_left_message holds what response to print to the user
    lines_left_message = "Press enter to view more. Enter 'no' to stop viewing. There {} {} row{}left.\n"
    print('-'*40)
    print("Now loading raw data...\n")
    user_input = ""
    
    while user_input.lower() != 'no' and line_count < len(df):
        line_count += 5
        lines_left = len(df) - line_count
        print(df.head(line_count))
        print('-'*40)
        if(lines_left > 1):
            print(lines_left_message.format('are', lines_left, 's '))
        elif(lines_left == 1):
            print(lines_left_message.format('is', lines_left, ' '))
        else:
            print("There are no rows left to view. Enter 'no' to stop viewing.\n")
        user_input = input("Your Response: ")
    print('-'*40)
    print("Now exiting raw data viewer (no more data to show)...")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    # create a variable that holds city names (from the CITY_DATA dictionary. Cast it to a list, then
    # pass it to my new function.)
    valid_inputs = list(CITY_DATA.keys())
    
    # get what city the user wants to filter by
    while True:
        print("Please enter the name of the city you'd like to view information about. The options are:")
        print(list_to_str(valid_inputs), "\n")
        city = input("Your city: ").lower()
        if city.lower() not in valid_inputs or city.lower() == 'all':
            print(invalid_user_input, "\n")
        else:
            print("Loading data from " + city.title() + "...\n")
            break
    
    # get what month the user wants to filter by, if any
    while True:
        print("Enter a month to filter data by (January-June only), or enter 'all' to view all months:")
        month = input("Your month choice: ").lower()
        if (month.lower() not in ['january', 'february','march','april','may','june', 'all']):
            print(invalid_user_input, "\n")
        else:
            print("Loading data from " + month.title() + "...\n")
            break

    # get what day the user wants to filter by, if any
    while True:
        print("Enter a day to filter data by (Monday-Sunday), or enter 'all' to view all days:")
        day = input("Your day choice: ").lower()
        if (day.lower() not in ['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday','all']):
            print(invalid_user_input, "\n")
        else:
            print("Loading data from " + day.title() + "...\n")
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # this holds the message that verifies the user's selection, made here so I don't have to retype it

    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime (so i can analyze it)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # make a new column for month so I can filter by it
    df['Month'] = df['Start Time'].dt.month

    # make a new column for weekday so I can filter by it
    df['Weekday'] = df['Start Time'].dt.day_name()

    # make a new column for hour so I can filter by it
    df['Hour'] = df['Start Time'].dt.hour

    # convert the name of the month to the number that will be in the dataframe
    if month.lower() != 'all':
        months = ['january', 'february','march','april','may','june']
        month = months.index(month.lower()) + 1
        
        # filter by month
        df = df[df['Month'] == month]

    if day.lower() != 'all':
        df = df[df['Weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    """A lot is happening here. first, we get the mode of the Month column in the dataframe.
    then, we use it to index the month list we made at the very top of the program, then
    convert it to titlecase."""
    print("The most common month is:", months[df['Month'].mode()[0] - 1].title())

    # display the most common day of week
    print("The most common day of the week is:", df['Weekday'].mode()[0])

    # display the most common start hour
    # convert the returned hour to string so I can display it properly
    print("The most common hour is: " + str(df['Hour'].mode()[0])+ ":00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: " + most_common_start_station)


    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("\nThe most commonly used end station is: " + most_common_end_station)


    # display most frequent combination of start station and end station trip
    # the next line creates a new column with a string to represent each trip from start to end
    df['Start to End'] = df['Start Station'] + " to " + df['End Station']
    
    # then grab the mode of that new string and it should answer our question
    most_common_comb_station = df['Start to End'].mode()[0]
    print("\nMost frequent combination for start and stop station (start to end of trip):", most_common_comb_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print("\nTotal travel time: {:2d} hours and {:2d} seconds.".format(*divmod(total_travel_time, 60)))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print("\nMean travel time: {:2d} hours and {:2d} seconds.".format(*divmod(mean_travel_time, 60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_user_types = df['User Type'].value_counts().to_string()
    print("The user types are:\n")
    print(count_of_user_types)
    
    # Display counts of gender
    """ 
    NOTE: sometimes this caused an error because washington doesn't have gender data! So
    I put a try/catch block to prevent errors.
    """ 
    print("\nThe reported user gender data is:")
    try:
        count_of_user_genders = df['Gender'].value_counts().to_string()
        print("\n"+count_of_user_genders)

        # display the most common YOB for each gender
        # make new dataframes for male and female users
        male_df = df[df['Gender'] == 'Male']
        female_df = df[df['Gender'] == 'Female']
        common_birth_year_male = int(male_df['Birth Year'].mode())
        common_birth_year_female = int(female_df['Birth Year'].mode())

        print("\nThe most common male user's birth year is: {:2d}".format(common_birth_year_male))
        print("The most common female user's birth year is: {:2d}".format(common_birth_year_female))
    except:
        print("\nNo gender data found for " + city.title()+", continuing with report...")

    try:
        """
        This section was placed in a try block in case of a file like Washington, which
        does not include birth year data.
        """
        # Display earliest, most recent, and most common year of birth
        print("\nUser birth-year data:")
        
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].mode())
        print("\nThe eldest user was born in:",earliest_yob)
        print("The youngest user was born in:",most_recent_yob)
        print("The most common user's birth-year is:",most_common_yob)
    except:
        print("\nThere is no birth year data for the city "+city.title()+", continuing report...")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print('\nHello! Let\'s explore some US bikeshare data!')

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_data(df)

        print('\nWould you like to restart? Enter yes or no.\n')
        restart = input('Your Response: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

""" 
Credit to this Stack Overflow post to help me find the function divmod() to display hours and minutes!
https://stackoverflow.com/questions/20291883/converting-minutes-to-hhmm-format-in-python
"""