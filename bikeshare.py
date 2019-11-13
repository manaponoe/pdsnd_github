import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


CITY_LIST = ['all','chicago','new york city','new_york_city', 'washington']
MONTH_LIST = ['all', 'january','february','march','april','may','june']
DAY_LIST = ['all','monday','tuesday','wednesday','thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while -1:
        city = input ("Enter :\n\t'all'====>All city \n\t'City title'===> Specific city \n\t'none'===> No city filter \nCity :").lower()
        if city in CITY_LIST or city =='':
            break
      
    # TO DO: get user input for month (all, january, february, ... , june)
    while -1:
        month = input ("Enter :\n\t'all'====>All month \n\t'month '===> Specific month \n\t'none'===> No month filter \nMonth :").lower()
        if month in MONTH_LIST or month =='':
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while -1:
        day = input ("Enter :\n\t'all'====>all day \n\t'day '===> specific day \n\t'none'===>no day filter \nDay :").lower()
        if day in DAY_LIST or day =='':
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
   
        #print (city)
   #Load all city file

    if city == 'all':
        city = ['chicago.csv','new_york_city.csv','washington.csv']
        tmp =[]
        for filename in city :
            frame = pd.read_csv(filename)
            tmp.append(frame)
        
        df = pd.concat(tmp)
        
    else:
        
        df = pd.read_csv(CITY_DATA[city])
  
   #convert in datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
   #extract month 

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    
    #filter by month 
    if month != 'all':
        month = MONTH_LIST.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        day = DAY_LIST.index(day) + 1
        df = df[df['day'] == day]
   
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].value_counts().idxmax()
    print (common_month)
    
    # TO DO: display the most common day of week
    common_day = df['day'].mode()[0]
    print (common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts().idxmax()
    print (common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    commun_st = df['Start Station'].value_counts().idxmax()
    print (commun_st)

    # TO DO: display most commonly used end station
    commun_es = df['End Station'].mode().loc[0]
    print (commun_es)

    # TO DO: display most frequent combination of start station and end station trip
    comb_sa_se = df[['Start Station','End Station']].mode().loc[0]
    print ("the most frequent combination of start satation and end station trip is :",comb_sa_se[0],comb_sa_se[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print ("Total travel time :",total_travel_time,'\n')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print ("Mean travel time :",mean_travel_time,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    nbr_user_types = df['User Type'].value_counts()
    #nbr_user_types = df['User Types'].value_counts()
    print ()
    
    for index, nbr_user in enumerate(nbr_user_types):
        print ("user {}, nbr{}".format(nbr_user_types.index[index],nbr_user))
        
    #print ("Total count user Types :", nbr_user_types,'\n')
    
    # TO DO: Display counts of gender
    
    if 'Gender' in df.columns:
        print("Gender counts *******:\n")
        gender_counts = df['Gender'].value_counts()
        for index, gender in enumerate(gender_counts):
            print ("{}:{}".format(gender_counts.index[index],gender))       
   
    if 'Birth Year' in df.columns:
        by = df['Birth Year']
        # TO DO: Display earliest, most recent, and most common year of birth
        print ("earliest year of birth :",by.min())
        print ("Most recent year of birth :",by.max())
        print ("Most common year of birth :",by.value_counts().idxmax())
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
  
    row_length = df.shape[0]
  
    for i in range(0, row_length, 5):

        answer = input('Would you like to view particular user trip data? Type \'yes\' or \'no\'\n> ')
        if answer.lower() != 'yes':
            break

       
        # convert to json format and spliting of each json row data 
        #row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')

        for row in row_data:
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2) 
            json_row = df.head(5).append(df.tail(5))
            print(json_row.tail(5))
        



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
