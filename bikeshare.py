import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6}

WEEK_DATA = {'monday': 0,
             'tuesday': 1,
             'wednesday': 2,
             'thursday': 3,
             'friday': 4,
             'saturday': 5,
             'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Chicago, New York City, or Washington?\n').lower()
        print()
        if city not in CITY_DATA:
            print('Please enter a valid city name. Please watch the spelling.')
            continue
        city = CITY_DATA[city]
        break

    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        datafilter=input('You can filter by entering \'month\' or \'day\' or have the complete dataset analyzed by entering \'all\'.\n').lower()
        print()
        if datafilter == 'month':
            print('Which month to analyze?')
            month = input('January, February, March, April, May, June\n').lower()
            print()
            if month not in MONTH_DATA:
                print('I could not recognize your input. Please enter a valid input.')
                continue
            month = MONTH_DATA[month]
            day = 'all'
        elif datafilter == 'day':
            print('Which day to analyze?')
            day = input('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n').lower()
            print()
            if day not in WEEK_DATA:
                print('I could not recognize your input. Please enter a valid input.')
                continue
            day = WEEK_DATA[day]
            month = 'all'
        elif datafilter == 'all':
            day = 'all'
            month = 'all'
        else:
            print('I could not recognize your input. Please enter a valid input.')
            continue
        break
    #print('You chose {} for the month and {} for the day to analyze for the city {}.'.format(month, day, city))
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
    df = pd.read_csv(city)
    # Considering all days and months
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    if day != 'all':
        df = df[df['day_of_week'] == day] # boolean selection for the day of interest
    if month != 'all':
        df = df[df['month'] == month]    # boolean selection for the month of interest

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    for month in MONTH_DATA:
        if MONTH_DATA[month] == most_common_month:
            most_common_month = month.title()
    print('The most common month for travel is {}'.format(most_common_month))

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    for day in WEEK_DATA:
        if WEEK_DATA[day] == most_common_day:
            most_common_day = day.title()
    print('The most common day of week for travel is {}'.format(most_common_day))

    # TO DO: display the most common start hour
    df['hour']=pd.to_datetime(df['Start Time']).dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour for travel is {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print()
    print('Most commonly used start station as per the data was {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print()
    print('Most commonly used end station as per the data was {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print()
    station_combination = df['Start Station'] + ' to ' + df['End Station']
    most_common_station_combination = station_combination.mode()[0]
    print('The most common combination of start station and end station for a trip was {}'.format(most_common_station_combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    travel_durations = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    # TO DO: display total travel time
    print()
    td_sum = travel_durations.sum()
    print('Passengers travelled a total of {}.'.format(td_sum))

    # TO DO: display mean travel time
    print()
    td_mean = travel_durations.mean()
    print('Passengers travelled an average of {}.'.format(td_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # TO DO: Display counts of user types
    print()
    types_of_users = df.groupby('User Type', as_index = False).count()
    print('Number of types of users are {}'.format(len(types_of_users)))
    for i in range(len(types_of_users)):
        print('{}: {}'.format(types_of_users['User Type'][i], types_of_users['End Time'][i]))

    # TO DO: Display counts of gender
    print()
    if 'Gender' not in df:
        print('Sorry, but there is no gender data for this city to evaluate.')
    else:
        gender_of_users = df.groupby('Gender', as_index = False).count()
        print('Number of genders of users in the data are {}'.format(len(gender_of_users)))
        for i in range(len(gender_of_users)):
            print('{}: {}'.format(gender_of_users['Gender'][i], gender_of_users['End Time'][i]))
        print('Gender data for {} users is not available.'.format(len(df)-gender_of_users['End Time'][0]-gender_of_users['End Time'][1]))
        # This calculate the total number of users minus the ones where the explicit gender was mentioned to give the number of passengers that didn't provide gender data

    # TO DO: Display earliest, most recent, and most common year of birth
    print()
    if 'Birth Year' not in df:
        print('Sorry, but there is no data related to birth year of users for this city to evaluate.')
    else:
        birth = df.groupby('Birth Year', as_index = False).count()
        print('Earliest year of birth was {}.'.format(int(birth['Birth Year'].min())))
        print('Most recent year of birth was {}.'.format(int(birth['Birth Year'].max())))
        print('Most common year of birth year was {}.'.format(int(df['Birth Year'].value_counts().idxmax())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    while True:
        print()
        choice = input('Would you like to read some raw data? Please enter \'Yes\' or \'No\'\n').lower()
        print()
        if choice == 'no':
            return
        elif choice == 'yes':
            break
        else:
            print('You did not enter a valid input. Please try again.')
            continue

    if choice == 'yes':
        n = 5
        while True:
            for i in range(n-5,n):
                print(df.iloc[i])
                print()
            choice = input('Another five? Please enter \'Yes\' or \'No\'\n').lower()
            if choice == 'yes':
                n += 5
                continue
            elif choice == 'no':
                break
            else:
                print('You did not enter a valid choice. Exiting to main menu.')
                return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
