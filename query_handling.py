
# Only meant to take the queries, slice them up and present them in a nice way.

def read_input() -> str:
    '''Reads the first two lines and returns the method(Nominatim or file), location and weather-service(NWS or file)'''

    first_line =  input().split(' ',2)
    first_word = first_line[0] + ' '+first_line[1]
    location = ''

    if(first_word == 'TARGET NOMINATIM'):
        method = 'NOMINATIM'
        location = first_line[-1]

    elif (first_word == 'TARGET FILE'):
        method = first_line[-1]

    second_line = input().split(' ',2)

    second_word = second_line[0] + ' '+second_line[1]
    if second_word == 'WEATHER NWS':
        weather_service = 'NWS'
    elif second_word == 'WEATHER FILE':
        weather_service = second_line[-1]


    return method, location, weather_service
    #location returns (lat,lon) or ''
    #Method returns NOMINATIM OR path
    #weather_service returns NWS or path
    

def get_weather_query(line:str) -> list:
    ''' Returns a random weather query with what its specifics are + its parameters in a list form. 
    Follows['parameter_name',[x,y,z]] return style.
    ]'''
    length = len(line.split())

    weather_query = WeatherQuery()

    final_query = []
    if(length == 5):
        mode = line.rsplit(' ',3)[0]
        final_query.append(mode)
        if( mode == 'TEMPERATURE AIR'):

            final_query.append( weather_query.air_temperature(line))
        elif(mode == 'TEMPERATURE FEELS'):
            final_query.append( weather_query.feels_temperature(line) )
    else:
        mode = line.rsplit(' ',2)[0]
        final_query.append(mode)
        if(mode == 'HUMIDITY'):
            final_query.append( weather_query.humidity(line) )
        elif(mode == 'WIND'):
            final_query.append( weather_query.wind(line) )
        elif(mode == 'PRECIPITATION'):
            final_query.append ( weather_query.precipitaion(line) )
    return final_query


class WeatherQuery: 
     
    def air_temperature(self, line:str):
        weather_input  = line.rsplit(' ',3)
        air_scale = weather_input[1]
        air_length = weather_input[2]
        air_limit = weather_input[3]
        return [air_scale,air_length,air_limit]

    def feels_temperature(self, line):
        weather_input  = line.rsplit(' ',3)
        feels_scale = weather_input[1]
        feels_length = weather_input[2]
        feels_limit = weather_input[3]
        return [feels_scale,feels_length,feels_limit]

    def humidity(self, line: str):
        weather_input = line.rsplit(' ',2)
        humidity_length = weather_input[1]
        humidity_limit = weather_input[2]
        return  [humidity_length, humidity_limit]

    def wind(self, line: str):
        weather_input  = line.rsplit(' ', 2)
        wind_length = weather_input[1]
        wind_limit = weather_input[2]
        return  [wind_length, wind_limit]

    def precipitaion(self, line: str): 
        weather_input = line.rsplit(' ',2 )
        precipitation_length = weather_input[1] 
        precipitation_limit = weather_input[2] 
        return  [precipitation_length, precipitation_limit]

