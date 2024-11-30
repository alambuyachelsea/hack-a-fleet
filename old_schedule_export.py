import pandas as pd
import datetime

trips_df = pd.read_csv("ferry_tips_data.csv")

ids = [17, 16, 12, 21, 38]

for id in ids:
    route_df = trips_df[(trips_df["route_id"] == id) & (trips_df["trip_type"] == "ordinary           ")].copy()
    
    route_df.loc[:, "time_departure"] = route_df["time_departure"].apply(lambda x: datetime.datetime.fromisoformat(x))
    route_df["weekday"] = route_df["time_departure"].apply(lambda x: x.weekday())
    route_df["hour"] = route_df["time_departure"].apply(lambda x: x.hour)
    route_df["minute"] = route_df["time_departure"].apply(lambda x: x.minute)

    schedule = route_df.groupby(["weekday", "hour", "minute"], as_index=False).count()
    schedule = schedule[["weekday", "hour", "minute", "route_id"]]
    schedule = schedule.rename(columns={"route_id": "number of occurences (if low, it was probably some special schedule)"})
    schedule.to_csv("old_schedules/route"+str(id)+".csv", index=False)