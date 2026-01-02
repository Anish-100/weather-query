
import query_handling as qh
import api as api
from collections import namedtuple
import answer_query as aq
import time 
'''
Main loop that runs the query commands while active.
'''

Coordinate = namedtuple('Coordinate',['latitude','longitude'])

def  query_loop() -> list:

    '''Runs the loop to take in all queries and the first and second lines. '''

    final_list = []
    query_list = []
    used_forward_geocoding_api = False
    used_reverse_geocoding_api = False
    used_nws_api = False

    method,location, weather_service = qh.read_input()

    while True:
        query = input()
        if(query == 'NO MORE QUERIES'):
            break
        weather_query = qh.get_weather_query(query)
        query_list.append(weather_query)
    final_line = input()
    final_line = final_line.split(' ',2)
    final_word = f'{final_line[0]} {final_line[1]}'


    original_coordinate = get_nominatim_address(location, method) # Gets address

    if(original_coordinate == False) : # Only when it is false. 
        return False
    if(method == 'NOMINATIM'):
        used_forward_geocoding_api = True

    updated_coordinate =convert_to_printable_coordinates(original_coordinate.latitude,original_coordinate.longitude) # Gets lat and longitude (edited)

    #first element 
    final_list.append( ('TARGET', updated_coordinate.latitude, updated_coordinate.longitude) )

    forecast_hourly = ''
    if(weather_service == 'NWS'):
        forecast_hourly = get_weather_service((original_coordinate.latitude, original_coordinate.longitude)) # Only called when the API is needed to be used
        if(forecast_hourly == False) : # Only when it is false. 
            return False
        used_nws_api = True
    else:
        forecast_hourly = weather_service # file
    

    # Gets the period hourly cast and sets avg_coordinate
    parsed_hourly_forecast = parse_forecast(forecast_hourly, weather_service)
    if(parsed_hourly_forecast == False) : # Only when it is false. 
        return False
    if(weather_service == 'NWS'): #kinda redudent but more as a backup if somehow hourly report is not called but parse forecast is (which cannot happen thats why redudent)
        used_nws_api = True 
    
    avg_coordinate =_average_coordinate(parsed_hourly_forecast) 
    avg_coordinate_printable = convert_to_printable_coordinates(avg_coordinate.latitude,avg_coordinate.longitude)

    #Always the second element 
    final_list.append( ('FORECAST', avg_coordinate_printable.latitude, avg_coordinate_printable.longitude)  )



    for query in query_list:
        final_list.append(answer_weather_query(query, parsed_hourly_forecast))


    if(used_forward_geocoding_api == True):
        final_list.append('**Forward geocoding data from OpenStreetMap')
    
    
    if(final_word == 'REVERSE NOMINATIM'):
        time.sleep(1)
        temp_object = api.ReverseGeoCodingAPI(avg_coordinate)
        reverse_file = temp_object.get_address()
        if(failed_function(reverse_file) == True) : # Only when it is false. 
            return False
        used_reverse_geocoding_api = True

        if(used_reverse_geocoding_api == True):
            final_list.append('**Reverse geocoding data from OpenStreetMap')
        if(used_nws_api == True):
            final_list.append('**Real-time weather data from National Weather Service, United States Department of Commerce')

        final_list.append(reverse_file) 
    elif(final_word == 'REVERSE FILE'):
        temp_object = api.ReverseGeoCodingFile(final_line[-1])
        reverse_file = temp_object.get_address()
        if(failed_function(reverse_file) == True) : # Only when it is false. 
            return False
        if(used_nws_api == True):
            final_list.append('**Real-time weather data from National Weather Service, United States Department of Commerce')

        final_list.append(reverse_file) 



    return final_list
    

def get_nominatim_address(location:str, method:str )->str:
    '''Gets the forward latitiude/longitude from nominatim'''

    if(method == 'NOMINATIM'):
        time.sleep(1)
        our_location = api.ForwardGeoCodingAPI(location)

    else:
        our_location = api.ForwardGeoCodingFile(method)

    coords = our_location.get_point()
    if(failed_function(coords) == True):
        return False

    return coords


def get_weather_service(location: tuple ) -> str:
    '''Gets the whole weather report'''
    our_location = api.WeatherReport(location)
    
    json_text = our_location.get_point()
    if(failed_function(json_text) == True):
        return False

    return json_text

def parse_forecast(weather_report:str, weather_service:str )->'list':
    ''' Pareses weather report and returns only hourly report'''
    if(weather_service == 'NWS'):
        hourly_report = api.HourlyReportAPI(weather_report)
    else:
        hourly_report = api.HourlyReportFile(weather_service) 
        
    report_hours = hourly_report.get_point()
    if(failed_function(report_hours) == True):
        return False
    return report_hours
       



def answer_weather_query (weather_query:str, hourly_forecast: dict ) -> str:
    '''Returns answers for any weather query'''

    type_of_query = weather_query[0]
    length = int( weather_query[1][-2])
    limit = weather_query[1][-1]

    period_list = _limit_period(hourly_forecast, length)

    if(type_of_query == 'TEMPERATURE AIR'):
        scale = weather_query[1][0]
        return aq.temperature_air(scale,limit,period_list)
    elif(type_of_query == 'TEMPERATURE FEELS'):
        scale = weather_query[1][0]
        return aq.temperature_feels(scale,limit, period_list)

    elif(type_of_query == 'HUMIDITY'):
        return aq.humidity(limit, period_list)
    
    elif(type_of_query == 'WIND'):
         return aq.wind_speed(limit, period_list)
    
    elif(type_of_query == 'PRECIPITATION'):
         return aq.precipitation(limit, period_list)
    

def _average_coordinate(hourly_forecast:str)-> Coordinate:
    '''Takes the average lat and long out of each coordinate'''
    list_of_coords = hourly_forecast.get('geometry',{}).get('coordinates')[0]
    final_list = []
    for i in list_of_coords:
        if i not in final_list:
            final_list.append(i)
    
    sum_lat = 0.0
    sum_long =0.0
    for x in final_list:
        sum_lat += x[1]
        sum_long += x[0]
        #reversed
    average_coordinates = Coordinate(latitude= (sum_lat/len(final_list)), longitude= (sum_long/len(final_list)) )
    return average_coordinates

def _limit_period(hourly_forecast:dict, length: int)->dict:
    '''Limits the hourly to x hours '''
    all_periods = hourly_forecast.get('properties', {}).get('periods')
    try:
        limited_periods = all_periods[:length] 
    except:
        limited_periods = all_periods
    return limited_periods

def convert_to_printable_coordinates(latitude:float,longitude:float)-> Coordinate:
    lat = float(latitude)
    lon = float(longitude)
    if lon < 0:
        lon = str(abs(lon)) + '/W'
    elif lon > 0:
        lon = str(abs(lon)) + '/E'
    if lat < 0:
        lat = str(abs(lat)) + '/S'
    elif lat > 0:
        lat = str(abs(lat)) + '/N'
    return Coordinate(lat, lon)


def failed_function(reason:str) -> True|False:
    ''' Only prints the final reason for failure and returns True if it is a failed function'''
    if(reason == 'NOT 200'):
        return True
    elif(reason == 'FORMAT'):
        return True
    elif(reason == 'NETWORK'):
        return True
    
    if(reason == 'MISSING'):
        return True
    elif(reason == 'FORMAT'):
        return True
    
    return False



if __name__ =='__main__':
    query_loop()