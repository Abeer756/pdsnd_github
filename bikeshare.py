# import the required libraries
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
    print('Hello! Let\'s explore some US bikeshare data!')

    # Valid options
    valid_cities = ["chicago", "new york city", "washington"]
    valid_months = ["all", "january", "february", "march", "april", "may", "june"]
    valid_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please choose a city (chicago, new york city, washington): ").strip().lower()
        if city in valid_cities:
            break
        else:
            print("Invalid city name. Please try again.")
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please choose a month (all, january, february, ... , june): ").strip().lower()
        if month in valid_months:
            break
        else:
            print("Invalid month. Please try again.")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please choose a day of the week (all, monday, tuesday, ... sunday): ").strip().lower()
        if day in valid_days:
            break
        else:
            print("Invalid day. Please try again.")
    
    print("-" * 40)
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
    # Map city strings to CSV filenames
    CITY_DATA = {
        'chicago': 'chicago.csv',
        'new york city': 'new_york_city.csv',
        'washington': 'washington.csv'
    }
    
    # 1. Read the specified city's CSV file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # 2. Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # 3. Extract the month (1-12) and day of week (Monday, Tuesday, etc.)
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()  # e.g. "Monday"

    # 4. Filter by month if applicable
    if month != 'all':
        # Create a list of valid months for mapping to numeric values
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1  # e.g. 'january' -> 1
        df = df[df['month'] == month_index]

    # 5. Filter by day of week if applicable
    if day != 'all':
        # Make sure case sensitivity doesn't matter by converting both sides to lowercase
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Assumes 'month', 'day_of_week', and 'Start Time' columns already exist in the DataFrame.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # 1) Most common month
    #    df['month'] is an integer (1–12), but if you want the name,
    #    you could map it back to ['January', 'February', ...] if needed.
    common_month = df['month'].mode()[0]
    print(f"The most common month (as a number 1–12) is: {common_month}")

    # 2) Most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print(f"The most common day of week is: {common_day_of_week}")

    # 3) Most common start hour
    #    First extract the hour if it isn’t already in the DataFrame
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # 1) Most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {common_start_station}")

    # 2) Most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {common_end_station}")

    # 3) Most frequent combination of start station and end station
    # Create a temporary column or just do it inline
    df['trip_route'] = df['Start Station'] + " -> " + df['End Station']
    common_route = df['trip_route'].mode()[0]
    print(f"Most frequent trip route: {common_route}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # 1) Total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time (seconds): {total_travel_time}")

    # Convert total travel time to hours, minutes, and seconds for readability
    total_hours = total_travel_time // 3600
    total_minutes = (total_travel_time % 3600) // 60
    total_seconds = total_travel_time % 60
    print(f"Total travel time: {total_hours} hours, {total_minutes} minutes, {total_seconds} seconds")

    # 2) Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time (seconds): {mean_travel_time:.2f}")

    # Convert mean travel time to minutes and seconds for readability
    mean_minutes = mean_travel_time // 60
    mean_seconds = mean_travel_time % 60
    print(f"Mean travel time: {int(mean_minutes)} minutes, {int(mean_seconds)} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # 1) Display counts of user types
    if 'User Type' in df.columns:
        user_type_counts = df['User Type'].value_counts()
        print("Counts of user types:")
        print(user_type_counts)
    else:
        print("No 'User Type' column in this dataset.")

    # 2) Display counts of gender (only if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nNo 'Gender' column in this dataset.")

    # 3) Display earliest, most recent, and most common year of birth (only if available)
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])

        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {most_recent_year}")
        print(f"Most common year of birth: {most_common_year}")
    else:
        print("\nNo 'Birth Year' column in this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # 1) Total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time (seconds): {total_travel_time}")

    # 2) Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time (seconds): {mean_travel_time}")

    # Alternatively, you might convert these values to minutes or hours:
    # total_minutes = total_travel_time / 60
    # mean_minutes = mean_travel_time / 60
    # print(f"Total travel time (minutes): {total_minutes}")
    # print(f"Mean travel time (minutes): {mean_minutes}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Displays raw data from the DataFrame in increments of 5 rows upon user request.
    Continues until the user says 'no' or we run out of data rows.
    """
    start_loc = 0
    df_length = len(df)

    while True:
        view_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no:\n").strip().lower()
        if view_data != 'yes':
            break

        # Print 5 rows
        print(df.iloc[start_loc : start_loc + 5])
        start_loc += 5

        # If no more rows, stop
        if start_loc >= df_length:
            print("\nNo more rows left to display.")
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        # Add input validation for restart prompt
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
            if restart in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if restart != 'yes':
            break
                



if __name__ == "__main__":
	main()
