import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # a list of valid cities
    cities = ['chicago', 'new york city', 'washington']
    
    # a list of valid months
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    
    # a list of valid week days
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to fetch information about? ')
    while city.lower() not in cities :
        print("Invalid input!")
        city = input('Which city would you like to fetch information about? ')

    # get user input for month (all, january, february, ... , june)
    month = input('Select month from January to June or All to fetch data for all the months: ')
    while month.lower() not in months :
        print("Invalid input!")
        month = input('Select month from January to June or All to fetch data for all the months: ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Select day of week, type \'all\' to fetch data for all days: ')
    while day.lower() not in days :
        print("Invalid input!")
        day = input('Select day of week, type \'all\' to fetch data for all days: ')

    print("Please input an integer value")
    limit = input('How many lines of data would you like to see? (Default: 5): ')
    if len(limit) == 0:
        limit = 5
    else :
        limit = int(input('How many lines of data would you like to see? (Default: 5): '))
        
    print('-'*40)
    return city, month, day, limit


def load_data(city, month = "all", day = "all"):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # convert inputed city name to lowercase
    city = city.lower()
    # capitalize the first letter of month and day names
    month = month.capitalize()
    day = day.capitalize()

    df = pd.read_csv( "./" + CITY_DATA[ city ], parse_dates= ["Start Time", "End Time"] )


    df['Month of year'] = df['Start Time'].dt.month_name()
    df['Day of week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if (month == "All") & (day == "All") :
        df = df
    elif (month != "All") :
        df = df[df['Month of year'] == month]
    elif (day != "All") :
        df = df[df['Day of week'] == day]
    else :
        df = df[(df['Month of year'] == month) & (df['Day of week'] == day)]

    return df
    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['Month of year'].mode()[0]
    print("Most common month: ", month)

    # display the most common day of week
    day = df['Day of week'].mode()[0]
    print("Most common day of the week: ", day)

    # display the most common start hour
    hour = df['Hour'].mode()[0]
    print("Most common start hour", hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, limit = 5):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df['Start Station'].groupby([df['Start Station']]).max().head(limit)
    print("Most commonly used start station: ", start)

    # display most commonly used end station
    end = df['End Station'].groupby([df['End Station']]).max().head(limit)
    print("Most commonly used end station: ", end)

    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print("Total travel time: ", total)

    # display mean travel time
    average = df['Trip Duration'].mean()
    print("Mean travel time: ", average)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby('User Type').count();
    print("Total user type: ", user_type)

    # Display counts of gender if city is not washington
    if city != 'washington' :
        gender = df.groupby('Gender').count();
        print("Gender count: ", gender)

    # Display earliest, most recent, and most common year of birth
    if city != 'washington' :
        earliest = df['Birth Year'].min()
        print("Earliest year of birth: ", earliest)

        recent = df['Birth Year'].max()
        print("Most recent year of birth: ", recent)

        common = df[df['Birth Year'] == df['Birth Year'].count()].max()
        print("Most common year of birth: ", common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, limit = get_filters()
        df = load_data(city, month, day)

        print(time_stats(df))

        print(station_stats(df, limit))
        print(trip_duration_stats(df))
        print(user_stats(df, city))

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
