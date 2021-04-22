import include.secrets as secrets
import psycopg2
import pandas as pd
# from matplotlib.pyplot import polar
from matplotlib.figure import Figure
import base64
from io import StringIO


def query_db():
    # get data from last 24hrs
    SQL = 'SELECT dt, main_temp, main_feels_like, main_pressure, main_humidity, wind_speed, wind_deg FROM weather_station WHERE dt >= NOW() - \'1 day\'::INTERVAL;'
    # get config
    params = secrets.aws()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute(SQL)
    data = cur.fetchall()
    cur.close()
    return data


def plot_temp(data):
    # create dataframe from list of tuples
    df = pd.DataFrame(data)
    # label columns
    df.columns = ['dt', 'temp', 'feels like', 'pressure',
                  'humidity', 'wind speed', 'deg']
    # weather is only updated a few times per hour, the ETL loads a new value
    # every 5 minutes, so many entries will have the same dataset.
    df.drop_duplicates(subset='dt', keep='first', inplace=True)
    # converting tempreatures from Kelvin to Celsius
    df['temp'] -= 273.15
    df['feels like'] -= 273.15
    # print(df)
    # mean of all measurements within one full hour
    # TODO: caveat! mean of wind direction will be inacurate around 0 / 360
    hourly_mean = df.groupby(df['dt'].dt.hour).mean()
    # TODO: rearrange rows, so they don't go from 0..23 but instead start from
    # the current hour and go back 24hrs from there.
    # print(hourly_mean)
    # hourly_mean.plot.line(y=['temp', 'feels like'])
    fig = Figure()
    ax = fig.subplots()
    ax.plot(hourly_mean['temp'].tolist())
    # Save it to a temporary buffer.
    buf = StringIO()
    fig.savefig(buf, format="svg")
    svg = buf.getvalue()
    svg = '<svg' + svg.split('<svg')[1]
    return svg
