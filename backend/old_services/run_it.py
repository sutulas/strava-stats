from services.strava_auth_service import StravaAuthService
from services.strava_data_service import StravaDataService
from services.format_data_service import FormatDataService
import json


if __name__ == "__main__":
    # auth_service = StravaAuthService()
    # data_service = StravaDataService()
    # format_data_service = FormatDataService()
    # access_token = auth_service.get_access()
    # activities = data_service.get_activities(access_token)
    # #save activies to json  
    # with open('activities.json', 'w') as f:
    #     json.dump(activities, f)
    # activities = json.load(open('activities.json'))
    format_data_service = FormatDataService()
    # formatted_data = format_data_service.format_data(activities)
    # print(formatted_data)
    # formatted_data.to_csv('formatted_run_data.csv', index=False)
    format_data_service.fix_data('formatted_run_data.csv')
