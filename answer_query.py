from math import pow
import datetime
#Does all the math and other stuff needed for the functions to work. 

def temperature_feels(scale:str, limit: str, hourly_list:dict)->float:
    '''Returns the max/min feels temperature'''

    final_temperature = 0

    temperature_list = []

    for period in hourly_list:
            temperature_list.append( [
                period['startTime'],
                _calc_feels_temperature(
                period['temperatureUnit'],period['temperature'],
                period['relativeHumidity']['value'], period['windSpeed']
                )
            ])
    final_temperature = _max_min(temperature_list, limit)

    if(scale == 'C'):
       final_temperature[1] = _convert_to_celsius(final_temperature[1])
       
    final_temperature[0] = _convert_to_datetime(final_temperature[0])
    final_temperature[1] =round(final_temperature[1],4)
    final_temperature[1] = f'{final_temperature[1]:.4f}'

    return final_temperature


def temperature_air(scale:str, limit: str, hourly_list:dict)->float:
    '''Returns the max/min air temperature with time'''
    final_temperature = 0

    temperature_list = []
    temperature_unit = ''
    for period in hourly_list:
            temperature_list.append( [ period['startTime'], period['temperature'] ])
            temperature_unit = period['temperatureUnit']
    final_temperature = _max_min(temperature_list,limit)
    if(temperature_unit == 'C'):
       final_temperature[1]= _convert_to_farenheit(final_temperature[1])

    if(scale == 'C'):
       final_temperature[1] = _convert_to_celsius(final_temperature[1])
    final_temperature[0] = _convert_to_datetime(final_temperature[0])
    final_temperature[1] =round(final_temperature[1],4)
    final_temperature[1] = f'{final_temperature[1]:.4f}'
    return final_temperature


def humidity(limit: str, hourly_list:dict )->float:
    '''Returns the max/min humidity in a given time period'''
    humidity_list =[]
    final_humidity = 0

    for period in hourly_list:
            humidity_list.append( [ period['startTime'] ,period['relativeHumidity']['value'] ])

    final_humidity = _max_min(humidity_list, limit)
    final_humidity[0] = _convert_to_datetime(final_humidity[0])
    final_humidity[1] = f'{final_humidity[1]:.4f}'
    final_humidity[1] = str(final_humidity[1])+'%'

    return final_humidity


def wind_speed(limit: str, hourly_list:dict )->float:
    '''Returns the max/min wind_speed in a given time period'''
    wind_list =[]
    final_wind = 0

    for period in hourly_list:
            wind_list.append( [ period['startTime'] ,period['windSpeed'].split()[0]])

    final_wind = _max_min(wind_list, limit)

    final_wind[0] = _convert_to_datetime(final_wind[0])
    final_wind[1] = f'{float(final_wind[1]):.4f}'

    return final_wind


def precipitation(limit: str, hourly_list:dict )->float:
    '''Returns the max/min precipitation in a given time period'''
    precipitation_list =[]
    final_precipitation = 0

    for period in hourly_list:
            precipitation_list.append( [ period['startTime'] ,period['probabilityOfPrecipitation']['value'] ])

    final_precipitation =_max_min(precipitation_list, limit)

    final_precipitation[0] = _convert_to_datetime(final_precipitation[0])
    final_precipitation[1] = f'{final_precipitation[1]:.4f}'
    final_precipitation[1] = str(final_precipitation[1])+'%'

    return final_precipitation



def _max_min(query_list:list, limit:str)-> list:
    '''Returns the max/min of a list'''
    final_num = 0.0
    if(limit == 'MAX'):
        max_val = [-9999,-99999]
        for num in query_list:
            if(float(num [1]) > float(max_val[1])):
                max_val = num
        for num in query_list:
            if(float(num[1]) == float(max_val[1])):
                if(num[0] < max_val [0]):
                    max_val = num
        final_num = max_val


    if(limit == 'MIN'):
        min_val = [1000,1000]
        for num in query_list:
            if(float(num [1]) < float(min_val [1])):
                min_val = num

        for num in query_list:
            if(float(num[1]) == float(min_val[1])):
                if(num[0] < min_val [0]):
                    min_val = num
        final_num = min_val

    return final_num


def _calc_feels_temperature(scale: str,air_temp:float , humidity: int, wind_speed: str):
    '''Calculates the feels-like temperature'''
    index = ''

    if(air_temp >= 68):
        index = 'heat'
    elif air_temp <= 50 and int(wind_speed.split()[0]) > 3:
        index ='wind_chill'
    
    temp = air_temp
    heat = humidity
    wind = int(wind_speed.split()[0]) # Follows format of "10 mph"
    if(index == 'heat'):
        final_temp = (
            -42.379 +(2.04901523* temp) + (10.14333127 * heat) - (0.22475541*temp* heat) +
            (-0.00683783*pow(temp,2)) + (-0.05481717*pow(heat,2)) +
            ( 0.00122874 * pow(temp,2) * heat ) + (0.00085282 * temp * pow(heat,2)) +
            (-0.00000199 * pow(temp,2) * pow(heat,2))
        )

    elif(index == 'wind_chill'):
        final_temp = (
            35.74 + (0.6215 * temp) + (-35.75 * pow(wind, 0.16) ) + (0.4275* temp * pow(wind,0.16) )
        )
    else:
        final_temp = temp
    return final_temp


def _convert_to_farenheit(celsius_temperature: float) -> float:
    '''Converts to farenheit '''
    return  ( float(celsius_temperature) * (9/5) ) + 32

def _convert_to_celsius(farenheit_temperature: float) -> float:
    '''Converts to celsius, might not be used'''
    farenheit_temperature = ( (float(farenheit_temperature) -32) *(5/9))
    return farenheit_temperature

def _convert_to_datetime(date_time:str)->str:
    '''Converts to utc time with ISO'''
    date_time_obj = datetime.datetime.fromisoformat(date_time)
    utc_date = date_time_obj.astimezone(datetime.timezone.utc)
    utc_time =utc_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    return utc_time