import pandas as pd
import numpy as np

class FormatDataService:
    def __init__(self):
        pass
    
    def format_activity(self, activity):

        
        #check to see if the activy has all the required fields
        if 'average_speed' not in activity:
            activity['average_speed'] = None
        if 'max_speed' not in activity:
            activity['max_speed'] = None
        if 'average_cadence' not in activity:
            activity['average_cadence'] = None
        if 'suffer_score' not in activity:
            activity['suffer_score'] = None
        if 'average_heartrate' not in activity:
            activity['average_heartrate'] = None
        if 'max_heartrate' not in activity:
            activity['max_heartrate'] = None
        

        return {
            'id': activity['id'],
            'start_date': activity['start_date'],
            'name': activity['name'],
            'distance': activity['distance'],
            'moving_time': activity['moving_time'],
            'elapsed_time': activity['elapsed_time'],
            'total_elevation_gain': activity['total_elevation_gain'],
            'start_date_local': activity['start_date_local'],
            'average_speed': activity['average_speed'],
            'max_speed': activity['max_speed'],
            'average_cadence': activity['average_cadence'],
            'average_heartrate': activity['average_heartrate'],
            'max_heartrate': activity['max_heartrate'],
            'suffer_score': activity['suffer_score']
        }
    def format_data(self, data):
        activities = []
        for activity in data:
            if activity['type'] == 'Run':
                activities.append(self.format_activity(activity))
        df = pd.DataFrame(activities)
        return df
    
    def fix_data(self, file_name):
        #load the data
        df = pd.read_csv(file_name)
        #fix the data
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])
        
        #add year, month, day, day of week, and time columns
        df['year'] = df['start_date_local'].dt.year
        df['month'] = df['start_date_local'].dt.month
        df['day'] = df['start_date_local'].dt.day
        df['day_of_week'] = df['start_date_local'].dt.day_name()
        df['time'] = df['start_date_local'].dt.time
        
        #convert distance to miles
        df['distance'] = df['distance'] * 0.000621371
        #convert moving_time to minutes
        df['moving_time'] = df['moving_time'] / 60
        #convert elapsed_time to minutes
        df['elapsed_time'] = df['elapsed_time'] / 60
        
        #convert speed from m/s to minutes/mile
        # Formula: minutes/mile = 26.822 / speed_in_mps
        # Handle division by zero by replacing 0 speeds with NaN
        df['average_speed'] = df['average_speed'].replace(0, np.nan)
        df['max_speed'] = df['max_speed'].replace(0, np.nan)
        
        # Convert speeds, handling NaN values
        df['average_speed'] = 26.822 / df['average_speed']
        df['max_speed'] = 26.822 / df['max_speed']
        
        #fill remaining empty values with 0 (for non-speed columns)
        df = df.fillna(0)

        #save the data
        df.to_csv(f"fixed_formatted_run_data.csv", index=False)
    
    def load_data(self, file_name):
        pass

if __name__ == "__main__":
    # sample_data = [{'resource_state': 2, 'athlete': {'id': 31849701, 'resource_state': 1}, 'name': 'Afternoon Run', 'distance': 4839.1, 'moving_time': 1347, 'elapsed_time': 1347, 'total_elevation_gain': 40.1, 'type': 'Run', 'sport_type': 'Run', 'workout_type': None, 'id': 15225395752, 'start_date': '2025-07-24T20:57:09Z', 'start_date_local': '2025-07-24T16:57:09Z', 'timezone': '(GMT-05:00) America/New_York', 'utc_offset': -14400.0, 'location_city': None, 'location_state': None, 'location_country': None, 'achievement_count': 0, 'kudos_count': 9, 'comment_count': 0, 'athlete_count': 1, 'photo_count': 0, 'map': {'id': 'a15225395752', 'summary_polyline': '}qj_GdodrLDMGSYi@g@oAQW_@cA[c@SJg@PiAp@_A`AKF]ZmApAYNg@`AG`@Nf@Vd@X\\N`@Vh@PAZa@~@{@LGTB^b@r@jBJd@r@zA`A|BDVQZYb@e@d@[d@wAl@_@ZK@IEOQ[i@c@mAYm@EYf@g@VQ`@[rAwAv@g@D?THDD^b@HNRh@x@jB`@tAbArCt@zCDn@DrBE|@?fAN~A?XGj@IzB?r@DRB@d@Ap@Kd@YjAeAf@Sd@e@h@QHD^XNn@Zb@FAh@{@tAgA`DyBn@g@fCgBhBiAvC{B~AeAvEoDvMaJRWNe@Hs@LiBHq@LcCCk@yCe@y@Mq@EmAWeBm@iAk@mBiAsA}@}@a@WSk@]gB{@c@[o@aAy@uBY_BW_A[mBQm@CGSGm@x@a@n@k@h@_AhAu@h@Yh@a@ZOBuA|@sBx@SDe@XiBx@uAv@aA\\iClAcAh@KLH^', 'resource_state': 2}, 'trainer': False, 'commute': False, 'manual': False, 'private': False, 'visibility': 'everyone', 'flagged': False, 'gear_id': 'g19751693', 'start_latlng': [42.0, -71.3], 'end_latlng': [42.0, -71.3], 'average_speed': 3.593, 'max_speed': 4.825, 'average_cadence': 82.9, 'has_heartrate': True, 'average_heartrate': 150.1, 'max_heartrate': 172.0, 'heartrate_opt_out': False, 'display_hide_heartrate_option': True, 'elev_high': 93.7, 'elev_low': 53.0, 'upload_id': 16259326684, 'upload_id_str': '16259326684', 'external_id': 'garmin_ping_462453659188', 'from_accepted_tag': False, 'pr_count': 0, 'total_photo_count': 0, 'has_kudoed': False, 'suffer_score': 10.0}, 
    #                {'resource_state': 2, 'athlete': {'id': 31849701, 'resource_state': 1}, 'name': 'Afternoon Run', 'distance': 4839.1, 'moving_time': 1347, 'elapsed_time': 1347, 'total_elevation_gain': 40.1, 'type': 'Run', 'sport_type': 'Run', 'workout_type': None, 'id': 15225395752, 'start_date': '2025-07-24T20:57:09Z', 'start_date_local': '2025-07-24T16:57:09Z', 'timezone': '(GMT-05:00) America/New_York', 'utc_offset': -14400.0, 'location_city': None, 'location_state': None, 'location_country': None, 'achievement_count': 0, 'kudos_count': 9, 'comment_count': 0, 'athlete_count': 1, 'photo_count': 0, 'map': {'id': 'a15225395752', 'summary_polyline': '}qj_GdodrLDMGSYi@g@oAQW_@cA[c@SJg@PiAp@_A`AKF]ZmApAYNg@`AG`@Nf@Vd@X\\N`@Vh@PAZa@~@{@LGTB^b@r@jBJd@r@zA`A|BDVQZYb@e@d@[d@wAl@_@ZK@IEOQ[i@c@mAYm@EYf@g@VQ`@[rAwAv@g@D?THDD^b@HNRh@x@jB`@tAbArCt@zCDn@DrBE|@?fAN~A?XGj@IzB?r@DRB@d@Ap@Kd@YjAeAf@Sd@e@h@QHD^XNn@Zb@FAh@{@tAgA`DyBn@g@fCgBhBiAvC{B~AeAvEoDvMaJRWNe@Hs@LiBHq@LcCCk@yCe@y@Mq@EmAWeBm@iAk@mBiAsA}@}@a@WSk@]gB{@c@[o@aAy@uBY_BW_A[mBQm@CGSGm@x@a@n@k@h@_AhAu@h@Yh@a@ZOBuA|@sBx@SDe@XiBx@uAv@aA\\iClAcAh@KLH^', 'resource_state': 2}, 'trainer': False, 'commute': False, 'manual': False, 'private': False, 'visibility': 'everyone', 'flagged': False, 'gear_id': 'g19751693', 'start_latlng': [42.0, -71.3], 'end_latlng': [42.0, -71.3], 'average_speed': 3.593, 'max_speed': 4.825, 'average_cadence': 82.9, 'has_heartrate': True, 'average_heartrate': 150.1, 'max_heartrate': 172.0, 'heartrate_opt_out': False, 'display_hide_heartrate_option': True, 'elev_high': 93.7, 'elev_low': 53.0, 'upload_id': 16259326684, 'upload_id_str': '16259326684', 'external_id': 'garmin_ping_462453659188', 'from_accepted_tag': False, 'pr_count': 0, 'total_photo_count': 0, 'has_kudoed': False, 'suffer_score': 10.0}
    #             ]
    # format_data_service = FormatDataService()
    # formatted_data = format_data_service.format_data(sample_data)
    # formatted_data.to_csv('formatted_data.csv', index=False)
    # print(formatted_data)
    format_data_service = FormatDataService()
    # sample_data = pd.read_csv('C:/Users/sutul/OneDrive/Desktop/strava-stats/backend/data/formatted_data.csv')
    fortmatted_data = format_data_service.fix_data('C:/Users/sutul/OneDrive/Desktop/strava-stats/backend/data/formatted_data.csv')
    # fortmatted_data.to_csv('C:/Users/sutul/OneDrive/Desktop/strava-stats/backend/data/fixed_formatted_data.csv', index=False)
    # format_data_service.fix_data('C:/Users/sutul/OneDrive/Desktop/strava-stats/backend/data/formatted_data.csv')
    