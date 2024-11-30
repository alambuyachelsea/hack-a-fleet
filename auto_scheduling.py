import info_collection.ship_usage_data.average_load as load
import datetime as dt
import pandas as pd
import math

# Define variables according to different ferries 
PEAK_TIMES = 0.4  # Load above 40% of capacity is considered peak maybe hmm
OFF_PEAK_TIME = 0.2  # Load between 20% and 40% is off-peak
ROUTE_ID = 17


# Iterate through each hour to calculate demand and schedule the times accordingly 
# at first i didnt use unique but ig there will be different ferries that have the same time yk??
#idk if this makes sense 
def calculate_weekly_schedule(route_id, trips_df, round_trip_time: int, capacity: int):
    schedule = []
    for day_of_week in range(7):
        total_load_by_hour = load.total_load_by_hour(ROUTE_ID, day_of_week, trips_df)
        avg_load_per_trip_by_hour = load.average_load_by_hour(ROUTE_ID, day_of_week, trips_df)
        for hour in total_load_by_hour["hour"].unique():
            # Calculate total load for this hour
            outbound_load = total_load_by_hour[total_load_by_hour["hour"] == hour]["cars_outbound"].values[0]
            inbound_load = total_load_by_hour[total_load_by_hour["hour"] == hour]["cars_inbound"].values[0]
            # for a given hour we only need to care about the higher of inbound or outbound traffic
            total_load = max(inbound_load, outbound_load)

            avg_load_per_trip_outbound = avg_load_per_trip_by_hour[avg_load_per_trip_by_hour["hour"] == hour]["cars_outbound"].values[0]
            avg_load_per_trip_inbound = avg_load_per_trip_by_hour[avg_load_per_trip_by_hour["hour"] == hour]["cars_inbound"].values[0]
            avg_load_per_trip = max(avg_load_per_trip_outbound, avg_load_per_trip_inbound)

            # Determine trip frequency based on load
            # High demand: Schedule trips so that load equals target peak % or every RRT
            trips = total_load // (capacity * PEAK_TIMES)
            trips = min(trips, 60 // round_trip_time)

            # if wait is too long, let's go for off peak target number
            if trips <= 2:
                # Medium demand: Schedule fewer trips (min 1 every 40 minutes)
                trips = total_load // (capacity * OFF_PEAK_TIME)
                trips = min(trips, 60 // 40)
                trips = min(trips, 60 // round_trip_time)

            for trip in range(math.floor(trips)):
                departure_time = dt.time(hour=hour, minute= (60 // math.floor(trips)) * trip)
                schedule.append({"day": day_of_week, "hour": hour, "departure_time": departure_time})
    return schedule


FRANCIAGA_CAPACITY = 34
JUPITER_CAPACITY = 58
MERKURIUS_CAPACITY = 56
NINA_CAPACITY = 48
YXLAN_CAPACITY = 32

FRANCIAGA_CROSS_TIME = 3
JUPITER_CROSS_TIME = 7
MERKURIUS_CROSS_TIME = 4
NINA_CROSS_TIME = 6
YXLAN_CROSS_TIME = 25

LOADING_TIME = 6 #Approx time it takes to load up the ferries

routes = []
routes.append([17, FRANCIAGA_CAPACITY, FRANCIAGA_CROSS_TIME])
routes.append([16, JUPITER_CAPACITY, JUPITER_CROSS_TIME])
routes.append([12, MERKURIUS_CAPACITY, MERKURIUS_CROSS_TIME])
routes.append([21, NINA_CAPACITY, NINA_CROSS_TIME])
routes.append([38, YXLAN_CAPACITY, YXLAN_CROSS_TIME])

trips_df = pd.read_csv("ferry_tips_data.csv")

for route in routes:
    schedule = calculate_weekly_schedule(route[0],trips_df, route[2] + LOADING_TIME*2, route[1])
    schedule_df = pd.DataFrame(schedule)
    schedule_df.to_csv("new_schedules/route"+str(route[0])+".csv", index=False)