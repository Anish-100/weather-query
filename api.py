
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
import json
from collections import  namedtuple

Coordinate = namedtuple('Coordinate',['latitude','longitude'])

class ForwardGeoCodingAPI():
    def __init__(self, location: str):
        self.location  = location

    
    def get_point(self) -> dict | str:
        params = urllib.parse.urlencode({
            'q': self.location,
            'format': 'jsonv2'
        })

        api_url = f'https://nominatim.openstreetmap.org/search?{params}'
        try:
            request = urllib.request.Request(
                api_url,
                headers = {'Referer': 'https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/anishpb'},
            )
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding= 'utf-8')
            json_dict = json.loads(json_text)

            lat = json_dict[0].get('lat')
            lon =  json_dict[0].get('lon')
            
            if response.status != 200:  
                print('FAILED')
                print(response.status, api_url)
                print('NOT 200')
                return 'NOT 200'
    
        except urllib.error.HTTPError as e:
            print('FAILED')
            print(e.code, e.url)
            print('NOT 200')
            return 'NOT 200'
        except urllib.error.URLError as e:
            print('FAILED')
            print(api_url)
            print('NETWORK')
            return 'NETWORK'
        except (json.JSONDecodeError, KeyError) as e:
            print('FAILED')
            print(api_url)
            print('FORMAT')
            return 'FORMAT'
#          
        except Exception as e:
            print('FAILED')
            print(api_url)
            print('NOT 200')
            return 'NOT 200'

        else:
            response.close()
            return Coordinate(lat,lon)


class ForwardGeoCodingFile():
    def __init__(self,  path:str):
        self.path = path
    
    def get_point(self) -> dict:
        try:
            file = Path(self.path)
            with open(file, mode ='r') as temp_file:
                data = json.load(temp_file)

            lat = data[0].get('lat')
            lon =  data[0].get('lon')

            return Coordinate(lat, lon)
        
        except FileNotFoundError:
                print('FAILED')
                print(file)
                print('MISSING') 
                return 'MISSING'
        except (json.JSONDecodeError, KeyError) as e:
            print('FAILED')
            print(self.path)
            print('FORMAT')
            return 'FORMAT'
        except:
            print('FAILED')
            print(file)
            print('MISSING')
            return 'MISSING'



class WeatherReport:
    def __init__(self, location:tuple):
        self.location = location #tuple
    
    def get_point(self):
        lat = self.location[0]
        long = self.location[1]

        api_url = f'https://api.weather.gov/points/{lat},{long}'
        try:
            request = urllib.request.Request(
                api_url,
                headers = {'User-Agent':'https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/, anishpb@uci.edu',
                          'Accept': 'application/geo+json'}
            )
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding= 'utf-8')
            json_dict = json.loads(json_text)
            response.close()
            if response.status != 200:  
                print('FAILED')
                print(response.status, api_url)
                print('NOT 200')
                return 'NOT 200'
    
        except urllib.error.HTTPError as e:
            print('FAILED')
            if(e.code != '' ):
                print(e.code, e.url)
            elif(e.code == ''):
                print(e.url)
            if(e.code != 200):
                print('NOT 200')
                return 'NOT 200'
        except urllib.error.URLError as e:
            print('FAILED')
            print(api_url)
            print('NETWORK')
            return 'NETWORK'
        except json.JSONDecodeError as e:
            print('FAILED')
            print(api_url)
            print('FORMAT')
            return 'FORMAT'
         
        except:
            print('FAILED')
            print(api_url)
            print('NOT 200')
            return 'NOT 200'

        else:
            response.close()
            return json_dict
            

class HourlyReportAPI:
    def __init__(self, url:str):
        self.url = url #string

    def get_point(self):
        api_url = self.url.get('properties', {}).get('forecastHourly')
        try:
            request = urllib.request.Request(
                api_url,
                headers = {'User-Agent':'https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/, anishpb@uci.edu'},
            )
            response = urllib.request.urlopen(request)

            json_text = response.read().decode(encoding= 'utf-8')
            json_dict = json.loads(json_text)
            response.close()

            for period in json_dict['properties']['periods']:
                period['startTime'],
                period['temperatureUnit'], period['temperature'],
                period['relativeHumidity']['value'], period['windSpeed'],
                period['probabilityOfPrecipitation']['value']
            
            if response.status != 200:  

                print('FAILED')
                print(response.status, api_url)
                print('NOT 200')
                return 'NOT 200'
            
            return json_dict 
                
    
        except urllib.error.HTTPError as e:
            print('FAILED')
            if(e.code != '' ):
                print(e.code, e.url)
            elif(e.code == ''):
                print(e.url)
            if(e.code != 200):
                print('NOT 200')
                return 'NOT 200'
        except urllib.error.URLError as e:
            print('FAILED')
            print(api_url)
            print('NETWORK')
            return 'NETWORK'
        except (json.JSONDecodeError, KeyError) as e:
            print('FAILED')
            print(api_url)
            print('FORMAT')
            return 'FORMAT'
        except:
            print('FAILED')
            print(api_url)
            print('NOT 200')
            return 'NOT 200'


class HourlyReportFile:
    def __init__(self, path:str):
        self.path = path 
        

    def get_point(self) -> dict:
        '''Opens a file, and returns the contents as a json dict'''
        file = Path(self.path)
        try:
            with open(file, mode ='r') as temp_file:
                data = json.load(temp_file)
            
            # THis is there to make sure no missing fields. Will fail if it cant parse
            for period in data['properties']['periods']:
                period['startTime'],
                period['temperatureUnit'], period['temperature'],
                period['relativeHumidity']['value'], period['windSpeed'],
                period['probabilityOfPrecipitation']['value']

            return data
        except FileNotFoundError:
            print('FAILED')
            print(file)
            print('MISSING') 
            return 'MISSING'
        except(json.JSONDecodeError, KeyError):
            print('FAILED')
            print(file)
            print('FORMAT')
            return 'FORMAT'
        except:
            print('FAILED')
            print(file)
            print('MISSING')
            return 'MISSING'



class ReverseGeoCodingAPI: 
    def __init__(self, location:tuple):
        self.location  = location
    
    def get_address(self) -> str:
        lat = self.location[0]
        long = self.location[1]
        lat = round(self.location[0], 4)
        long = round(self.location[1], 4)
        params = urllib.parse.urlencode({
        'lat': lat,
        'lon': long, 
        'format': 'json'
        })
        
        api_url = f'https://nominatim.openstreetmap.org/reverse?{params}'
        try:
            request = urllib.request.Request(
                api_url,
                headers = {'Referer': 'https://www.ics.uci.edu/~thornton/icsh32/ProjectGuide/Project3/anishpb'},
            )
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding= 'utf-8')
            json_dict = json.loads(json_text)
            if response.status != 200:  
                print('FAILED')
                print(response.status, api_url)
                print('NOT 200')
                return 'NOT 200'
    
        except urllib.error.HTTPError as e:
            print('FAILED')
            if(e.code != '' ):
                print(e.code, e.url)
            elif(e.code == ''):
                print(e.url)
            if(e.code != 200):
                print('NOT 200')
                return 'NOT 200'
        except urllib.error.URLError as e:
            print('FAILED')
            print(api_url)
            print('NETWORK')
            return 'NETWORK'
        except json.JSONDecodeError as e:
            print('FAILED')
            print(api_url)
            print('FORMAT')
            return 'FORMAT'
        
        except:
            print('FAILED')
            print(api_url)
            print('NOT 200')
            return 'NOT 200'

        else:
            response.close()
            return json_dict.get('display_name')

class ReverseGeoCodingFile: 
        def __init__(self, path: str):
            self.path = path 

        def get_address(self): 
            '''Opens a file, and returns the contents as a json dict'''
            file = Path(self.path)
            try:
                with open(file, mode ='r') as temp_file:
                    data = json.load(temp_file)
                return data.get('display_name')
            except FileNotFoundError:
                print('FAILED')
                print(file)
                print('MISSING') 
                return 'MISSING'
            except json.JSONDecodeError:
                print('FAILED')
                print(file)
                print('FORMAT')
                return 'FORMAT'
            except:
                print('FAILED')
                print(file)
                print('MISSING')
                return 'MISSING'

