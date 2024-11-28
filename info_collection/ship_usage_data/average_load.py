from matplotlib import pyplot
import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime

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