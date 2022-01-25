import pandas as pd
import numpy as np
import re


def format_data(df):
    # Airline Code
    df['Airline Code'] = df['Airline Code'].apply(lambda x: re.sub(r'[^A-Za-z ]+', '', x))

    # Cleaning FlightCodes
    df[['FlightCodes', 'Decimal']] = df['FlightCodes'].str.split('.', 1, expand=True)
    df['FlightCodes'] = df['FlightCodes'].apply(lambda x: 0 if x == '' else int(x))
    df['FlightCodes'] = np.where(df['FlightCodes'].bfill() == 0,
                                 df['FlightCodes'].shift(+1) + 10,
                                 df['FlightCodes'])
    df['FlightCodes'] = df['FlightCodes'].astype(int)

    # Splitting To_From
    df[['To', 'From']] = df['To_From'].str.split('_', 1, expand=True)
    df['To'] = df['To'].str.upper()
    df['From'] = df['From'].str.upper()
    df = df.drop(['To_From', 'Decimal'], axis=1)
    return df


if __name__ == '__main__':
    ## make data structure
    # data = input()
    data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'
    rows = data.split('\n')
    new = []
    for s in rows:
        cols = s.split(';')
        new.append(cols)
    df = pd.DataFrame(new[1:-1], columns=new[0])
    cleaned_data = format_data(df)
    print(cleaned_data)