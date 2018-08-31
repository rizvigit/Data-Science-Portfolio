

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
    print('\n\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city= input("\n\nWhich city would you like to look at today?\n\nYou can choose Chicago, New York or Washington.\n\n").lower().strip()

    #check for variations of new york
    if city in ['nyc','new york']:
        city='new york city'



    # keep asking for input if input is invalid.
    cities=['chicago','new york city','washington']
    while city not in cities:
        city= input("\n\nThat was not a valid input!\n Which city would you like to look at today? \nYou can choose Chicago, New York or Washington.\n\n").lower().strip()
    print('\n\nYou chose '+city.title()+'!\nI hear it\'s beautiful this time of year.\nLet\'s go ahead and load the city.\n\n')

    #call function wihtout filters, to acquire available months.
    df = load_data(city, 'all', 'all')
    print('\nOK! Here is a list of available months:\n\n')

    #determine the months available in the data
    month_vals=np.unique(np.sort(df['Start Month'].values))

    #convert array into month names and add "all"
    months_master=["january","february","march","april","may","june","july","august","september","october","november","december", "all"]
    month_names=[months_master[i-1] for i in month_vals]
    month_names.append('all')
    print(month_names)


    # get user input for month (all, january, february, ... , june)
    month= input("\n\nWhich month would you like to look at? \nPlease type the full name of the month or \'all\' if you'd like to see data for all the months.\n\n").lower().strip()
    while month not in month_names:
        month= input("\n\nThat was not a valid input!\nWhich month would you like to look at today? \nPlease type the full name of one of the twelve months or \'all\'.\n\n").lower().strip()
        #print based on choice of month
    if month == 'all':
        print('\n\nGreat! We will look at all of the months!\n\n')
    else:
        print('\n\nYou chose '+month.title()+'!\n\n' )



    # get user input for day of week (all, monday, tuesday, ... sunday)
    day= input("Which day of the week would you like to look at? \nPlease type the name of the day or \'all\' if you'd like to see data for all the days.\n\n").lower().strip()
    days=["monday","tuesday","wednesday","thursday","friday","saturday","sunday", "all"]
    while day not in days:
        day= input("\n\nThat was not a valid input! \nWhich day would you like to look at today? \nPlease type the full name of one of the seven days or \'all\'.\n\n").lower().strip()
                #print based on choice of month
    if day == 'all':
        print('\n\nGreat! We will look at all of the days!\n\n' )
    else:
        print('\n\nYou chose '+day.title()+'!\n\n' )
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
    #read city data
    df=pd.read_csv(CITY_DATA[city])

    # convert to datetime and create columns for months and hours
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['Start Month']=df['Start Time'].dt.month
    df['Start Day']=df['Start Time'].dt.weekday_name
    df['Start Hour']=df['Start Time'].dt.hour
    df['Trip']=df['End Time']-df['Start Time']

    #convert month to number using index
    months=["january","february","march","april","may","june","july","august","september","october","november","december", "all"]
    month=months.index(month)+1

    #check filters for month and day, and filter dataframe appropriately.
    #if month not specified
    if month == 13:
        if day == 'all':
            df=df
        else:
            df=df.groupby('Start Day').get_group(day.title())
    #if month is specified
    else:
        if day == 'all':
            df=df.groupby('Start Month').get_group(month)
        else:
            df=df.groupby('Start Month').get_group(month).groupby('Start Day').get_group(day.title())
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if all months were selected
    if month=='all':
        print('The most common month was: {}!'.format(df['Start Month'].value_counts().idxmax()))

    # display the most common day of week

    if day=='all':
        print('The most common day of the week was: {}!'.format(df['Start Day'].value_counts().idxmax()))

    # display the most common start hour
    print('The most common start hour was: {}!'.format(df['Start Hour'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station was: {}!'.format(df['Start Station'].value_counts().idxmax()))

    # display most commonly used end station
    print('The most common end station was: {}!'.format(df['End Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip
    #find the combination by looking for max value
    ds=df.groupby(['Start Station','End Station']).size().idxmax()

    print('The most frequent combination of stations were starting at {} and ending at {}!'.format(ds[0],ds[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is:')
    print(df['Trip'].sum())

    # display mean travel time
    print('The mean travel time is:')
    print(df['Trip'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Here is a break down of the user types:\n')
    print(df['User Type'].fillna('Not Provided').value_counts())

    # Display counts of gender if appropriate
    if city in ['chicago','new york city']:
        print('\nHere is a break down of the user\'s genders:\n')
        print(df['Gender'].fillna('Not Provided').value_counts())


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
