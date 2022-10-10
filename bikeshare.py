import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

Cities = ['chicago', 'new york', 'washington']

Months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

Weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asking user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Getting user input for city (chicago, new york city, washington).
    city = str(input('Would you like to see data for Chicago, New York or Washington? \n')).lower()
    while city.lower() not in Cities:
          city = str(input('Please input valid city name from Chicago, New York or Washington. \n')).lower()
          if city.lower() in Cities:
             break           

    # Getting user input for month (all, january, february, ... , june)
    month = str(input('Which month? January, February, March, April, May, or June? If you don\'t want to apply month filter then type \"all\"\n')).lower()
    while month.lower() not in Months:
          month = str(input('Please input valid Month name from January, February, March, April, May, or June. \n')).lower()
          if month.lower() in Months:
             break

    # Getting user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? If you don\'t want to apply day filter then type \"all\"\n')).lower()
    while day.lower() not in Weekdays:
          day = str(input('Please input valid Weekday from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. \n')).lower()
          if day.lower() in Weekdays:
             break
         
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loading data into dataframe for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filtering by month if applicable
    if month.lower() != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filtering by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # extracting hour from Start Time to create new column
    df['hour'] = df['Start Time'].dt.hour
    
    # displaying the most common month
    frequent_month = df['month'].mode()[0]
    print('\nMost Frequent Travel Month:', frequent_month)
    
    # displaying the most common day of week
    frequent_day = df['day_of_week'].mode()[0]
    print('\nMost Frequent Travel Weekday:', frequent_day)
    
    # displaying the most common start hour
    frequent_start_hour = df['hour'].mode()[0]
    print('\nMost Frequent Start Hour:', frequent_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # displaying most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station:', popular_start_station)
    
    # displaying most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost Popular End Station:', popular_end_station)
    
    # displaying most frequent combination of start station and end station trip
    popular_start_end_station = (df['Start Station'] + df['End Station']).mode()[0]
    print('\nMost Popular Start and End Station:\n', popular_start_end_station)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#, popular_start_end_station)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displaying total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\n Total Travel Time in seconds:', total_travel_time)
    
    # displaying mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('\n Average Travel Time in seconds:', average_travel_time) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    user_types = df['User Type'].value_counts()
    print('\n Count of User Types:\n', user_types) 
    
    # Displaying counts of gender, washington city data does not have gender and birth year column
    if city != 'washington':
        gender_types = df['Gender'].value_counts()
        print('\n Count of Gender Types:\n', gender_types)
    
    # Displaying earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        print('\n Earliest Year of Birth:', int(earliest_yob))
    
        recent_yob = df['Birth Year'].max()
        print('\n Recent Year of Birth:', int(recent_yob))
    
        popular_yob = df['Birth Year'].mode()[0]
        print('\n Most Frequent Year of Birth:', int(popular_yob))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data_display(df):
    """Displays raw data for bikeshare users."""
    
    count = 0
    print(df.head(5))
    while True:
        user_input = input('\n Would you like to view next 5 individuals Trip data? Type \'yes\' or \'no\'.\n').lower()
        if user_input.lower() != 'yes':
            return
        count += 5
        print(df.iloc[count:count+5])
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data_display(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
