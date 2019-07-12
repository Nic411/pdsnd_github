import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = ''
    while True:
        city = input('\nFor which city would you like to carry out the data analysis?\n Enter the name of the desired city: Chicago, New York City, Washington: ')
        if city.lower() in CITY_DATA:
            break
        else:
            print('This not the right input!')

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while True:
        month = input('\nFor which month should the analysis be carried out?\n Enter the month: January, February, ... , June) or "all" to apply no month filter: ')
        if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        elif month.lower() == 'all':
            break
        else:
            print('This not the right input!')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while True:
        day = input('\nFor which day of week should the analysis be carried out?\n Enter the day: Monday, Tuesday, ... Sunday) or "all" to apply no day filter: ')
        if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        elif day.lower() == 'all':
            break
        else:
            print('This not the right input!')
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        d_f - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nLoading the data... .. .. ..\n')
    d_f = pd.read_csv(CITY_DATA[city])

    # extract month and day of week from Start Time to create new columns
    d_f['Start Time'] = pd.to_datetime(d_f['Start Time'])
    d_f['month'] = d_f['Start Time'].dt.month
    d_f['day_of_week'] = d_f['Start Time'].dt.weekday_name
    d_f["day_of_month"] = d_f["Start Time"].dt.day

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        d_f = d_f[d_f['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        d_f = d_f[d_f['day_of_week'] == day.title()]

    print('\nLoading the data completed!\n')
    return d_f


def time_stats(d_f):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    d_f['month'] = d_f['Start Time'].dt.month
    popular_month = d_f['month'].mode()[0]
    print('\nMost Frequent Start Month:', popular_month)

    # TO DO: display the most common day of week
    d_f['day'] = d_f['Start Time'].dt.day
    popular_day = d_f['day'].mode()[0]
    print('\nMost Frequent Start Day:', popular_day)

    # TO DO: display the most common start hour
    d_f['hour'] = d_f['Start Time'].dt.hour
    popular_hour = d_f['hour'].mode()[0]
    print('\nMost Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(d_f):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    com_start_station = d_f['Start Station'].value_counts().idxmax()
    print('\nMost commonly used Start Station: ', com_start_station)

    # TO DO: display most commonly used end station
    com_end_station = d_f['End Station'].value_counts().idxmax()
    print('\nMost commonly used End Station: ', com_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    com_start_end_station = d_f[['Start Station', 'End Station']].dropna()
    com_start_end_station = com_start_end_station.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nMost frequent combination of start station and end station trip: ', com_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(d_f):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = d_f['Trip Duration'].dropna().sum()
    print('\nTotal Travel Time: ', total_time)

    # TO DO: display mean travel time
    mean_time = d_f['Trip Duration'].dropna().mean()
    print('\nMean Travel Time: ', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(d_f):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = d_f['User Type'].value_counts()
    print('\nCounts of user types: ' + str(user_types))

    #user_gender = d_f['Gender'].dropna()
    if 'Gender' not in d_f:
        print('\nUnfortunately, the data on gender and age are not available in the Washington database.')
    else:
        # TO DO: Display counts of gender
        gender = d_f['Gender'].value_counts()
        print('\nCounts of gender: ' + str(gender))

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest = np.min(d_f['Birth Year'])
        most_recent = np.max(d_f['Birth Year'])
        most_common = d_f['Birth Year'].mode()[0]
        print('\nThe earliest year of birth is: ' + str(earliest))
        print('\nThe most recent year of birth is: ' + str(most_recent))
        print('\nThe most common year of birth is: ' + str(most_common))

    print("\nDo you like to display 5 records of the raw data (yes or no)?")
    while True:
        answer = input('\nType yes or no: ')
        if answer.lower() == 'yes':
            print(d_f.iloc[0:5])
            break
        elif answer.lower() == 'no':
            print("\nOkay let's go further.")
            break
        else:
            print('This not the right input!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        d_f = load_data(city, month, day)

        time_stats(d_f)
        station_stats(d_f)
        trip_duration_stats(d_f)
        user_stats(d_f)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
