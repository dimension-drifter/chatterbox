from datetime import datetime
import re
import pandas as pd



def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)
    clean_data = data.replace('\u202f', ' ')
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    messages = re.split(pattern, data)
    message = [re.sub(r'\s+', ' ', data) for data in messages]
    messages1 = '\n'.join(message)
    dates = re.findall(pattern, data)
    date1 = [re.sub(r'\s+', ' ', data) for data in dates]
    date = '\n'.join(date1)

    def add_leading_zero(time_str):
        # Split the date and time
        date_part, time_part = time_str.split(', ')

        # Split the time into hour, minute, and period (am/pm)
        time, period = time_part.split('\u202f')
        hour, minute = time.split(':')

        # Add leading zero if hour is a single digit
        hour = hour.zfill(2)

        # Reconstruct the time string
        return f"{date_part}, {hour}:{minute} {period} -"

    # Apply the function to the list
    formatted_time_list = [add_leading_zero(time) for time in dates]  # Use time_list here
    date = [time.replace(' -', '', 1) for time in formatted_time_list]

    def convert_to_24_hour_format(time_str):
        # Remove the trailing dash and any extra spaces
        time_str = time_str.replace(' -', '').strip()

        # Split the string into date and time parts
        date_part, time_part = time_str.split(', ')

        # Convert to datetime object using 12-hour format
        dt = datetime.strptime(time_part, '%I:%M %p')

        # Format to 24-hour format
        formatted_time = dt.strftime('%H:%M')

        return f"{date_part}, {formatted_time} -"

    # Convert the list of time strings
    converted_times = [convert_to_24_hour_format(time) for time in date]
    # Split the text by newline character
    messages = messages1.strip().split('\n')

    # Remove empty strings from the list
    messages = [message.strip() for message in messages if message.strip()]
    df = pd.DataFrame({'user_message': messages, 'message_date': converted_times})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M -')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date

    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] =period

    return df











