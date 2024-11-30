from matplotlib import pyplot
import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime
pd.options.mode.chained_assignment = None 

def average_load_by_hour(route_id:int, day_of_week:int, trips_df):
    #filter for chosen route and make sure to only count ordinary trips
    route_df = trips_df[(trips_df["route_id"] == route_id) & (trips_df["trip_type"] == "ordinary           ")] #The type ordinary has a bunch of spaces in the csv.
    route_name = route_df["route_name"].iloc[0]


    #make time departure a datetime
    route_df.loc[:, "time_departure"] = route_df["time_departure"].apply(lambda x: datetime.datetime.fromisoformat(x))
    route_df["weekday"] = route_df["time_departure"].apply(lambda x: x.weekday())
    route_df = route_df[route_df["weekday"] == day_of_week]
    route_df["hour"] = route_df["time_departure"].apply(lambda x: x.hour)

    # calculate mean of all loads in the same hour.
    hourly_df = route_df.groupby("hour", as_index=False).mean(numeric_only=True)
    return hourly_df

def total_load_by_hour(route_id:int, day_of_week:int, trips_df):
    #filter for chosen route and make sure to only count ordinary trips
    route_df = trips_df[(trips_df["route_id"] == route_id) & (trips_df["trip_type"] == "ordinary           ")] #The type ordinary has a bunch of spaces in the csv.
    route_name = route_df["route_name"].iloc[0]


    #make time departure a datetime
    route_df.loc[:, "time_departure"] = route_df["time_departure"].apply(lambda x: datetime.datetime.fromisoformat(x))
    route_df["weekday"] = route_df["time_departure"].apply(lambda x: x.weekday())
    route_df = route_df[route_df["weekday"] == day_of_week]
    route_df["date"] = route_df["time_departure"].apply(lambda x: x.date())
    route_df["hour"] = route_df["time_departure"].apply(lambda x: x.hour)
    route_df["minute"] = route_df["time_departure"].apply(lambda x: x.minute)

    # calculate the sum of traffic in an hour for every single day individually
    hourly_df_by_date = route_df.groupby(["date", "hour"], as_index=False).sum(numeric_only=True)

    # aggregate separate days into a mean.
    hourly_df = hourly_df_by_date.groupby("hour", as_index=False).mean(numeric_only=True)
    return hourly_df