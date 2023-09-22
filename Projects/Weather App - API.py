import json
import requests

def main():

    # DSC510 - T304
    # Week 12
    # Final Project
    # 11/2/2022

    """
    This program will use an API connection to a weather service (openweathermap.org) to obtain weather information
    The user will be prompted to enter their city, state OR a zip code. The program determines what they typed in, calls to the weather service
    to obtain the Latitude and Longitude and then calls again to the weather service to obtain the weather information with the Lat and Long.
    There should be no point where this program fails as it can handle any input the user types.
    """

    def is_state(state):
        # This function has a dictionary that contains all the states (keys) and abbreviations (values).
        # I have this here to get the right weather the user is wanting. Since they are typing in an abbreviation when they type in city,state
        # and the API call requires the full state name, I needed to convert them.
        us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
        state = state.upper()
        for fullstate, abvstate, in us_state_to_abbrev.items():
            if state == abvstate:
                return(fullstate)
        return(print('Your state was not found.'))


    def latlong(geocodeurl, querrystring, headers, zipocity, state):
        # This function serves as calling the webservice to obtain the latitude and longitude information for the city, state OR zip code the user inputted
        # This function will call the next one, sending the longitude and latitude parameters
        # This try/except is error checking if the connection to the web service was successful or not as well as gathering the raw data from the web
        try:
            response = requests.request('GET', geocodeurl, headers=headers, params=querrystring)
        except:
            return(print('The connection to the web service failed, please try again'))
        # The following variable is cleaning up the raw web data into a dictionary using JSON
        parsed = json.loads(response.text)
        # The following series of if and elif statements are determining if the function was sent a zipcode or city, state
        # The if and elif statements then check if the city, state or zipcode exists or is valid
        if zipocity == 'zip':
            if 'message' in parsed.keys():
                if parsed['message'] == 'not found':
                    return(print('Sorry, you did not enter a valid Zip Code'))
            else:
                long = parsed['lon']
                lat = parsed['lat']
                weatherdata(lat, long, querrystring, headers)
        elif zipocity == 'city':
            fullstate = is_state(state)
            if len(parsed) == 0:
                return(print('Sorry, you did not enter a valid City,State'))
            else:
                for i in range(len(parsed)):
                    if parsed[i]['state'] == fullstate:
                        long = parsed[i]['lon']
                        lat = parsed[i]['lat']
                        weatherdata(lat, long, querrystring, headers)
                        break
                    else:
                        return(print('Your city was not found'))
    def weatherdata(lat, long, querrystring, headers):
        # This function will use the latitude and longitude from the latlong() function to gather the weather data from that lat and long
        # The function will then transport that raw data into a pretty print function that will display the weather in an easy-to-read format
        # This function also asks the user what units they would like to see on the temperatures
        while True:
            # To make sure the user types in correct units, I've made a while loop that will catch if they type in a valid unit
            units = input('What unit would you like the temperature to be in; Type F for Fahrenheit, C for Celsius, or K for Kelvin. ')
            units = units.strip()
            units = units.lower()
            if units == 'f':
                units = 'imperial'
                break
            elif units == 'c':
                units = 'metric'
                break
            elif units == 'k':
                units = 'standard'
                break
            else:
                print('You did not enter a valid unit, please try again.')
        weatherurl = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={querrystring["APIID"]}&units={units}'
        try:
            # similar to the latlong() function, I need to make sure the user gets connected to the web service. So, this try/except will make sure the user is successfully connected to the web service
            response = requests.request('GET', weatherurl, headers=headers, params=querrystring)
        except:
            return(print('Sorry the connection to the webservice failed, please check your network connection and try again. '))
        # If the connection was successful, the data will now get read somewhat cleanly into the parsed variable using JSON
        parsed = json.loads(response.text)
        # Now that I have the JSON data, I can send it to the pretty print function that will print out the data cleanly
        prettyprint(parsed)

    def prettyprint(parsed):
        # This function is the one uses the JSON data from the weatherdata() function. This will print the weather nice and pretty for the user
        #print(parsed)
        return print(
            'Sky:          ', parsed['weather'][0]['main'],'\n'
            'Current Temp: ', parsed['main']['temp'],'\n'
            'Feels Like:   ', parsed['main']['feels_like'],'\n'
            'Low:          ', parsed['main']['temp_min'],'\n'
            'High:         ', parsed['main']['temp_max'],'\n'
            'Humidity:     ', str(parsed['main']['humidity'])+'%','\n'
        )


    # Here, a few variables must be defined that will be used as parameters in the functions that call the web service
    # I'm defining them now so I will only have to define them once I must define the geocodeurl later since the user must input info fist
    querrystring = {'APIID':'ef20ab10991d02d0af0a7f81da5b4b77'}
    headers = {'cache-control':'no-cache'}

    # Here I define a few variables that will later help me determine if the user is entering a zip code or city,state
    zc = 0
    citystate = 0
    limit = 10
    zipocity = ''

    # Here is a welcome message to the user
    print('Welcome to the Corbin Weather App! Let\'s hope the weather is amazing today!')

    while True:
        # Now I am going to ask the user to input their location, either city state OR their zipcode
        location = input('Please enter a City,State OR a Zip Code: ')
        # Here I am getting rid of all the outer spaces that the user might have typed in to ensure that there is not spaces
        location = location.strip()
        # This try/except is checking whether or not the user inputted a city,state or a zipcode by checking if the input is an integer
        try:
            location = int(location)
            zipcode = location
            zc = 1
            zipocity = 'zip'
        except:
            citystate = 1
            zipocity = 'city'

        if citystate == 1:
            # This statement below splits the city and state into a list
            citystatelist = location.split(',')
            # Now that I have split the city, state into separate items in a list, I will use this for loop to remove any spaces the user might have put inbetween the city and state
            for i in range(len(citystatelist)):
                citystatelist[i] = citystatelist[i].strip()
            geocodeurl = f'http://api.openweathermap.org/geo/1.0/direct?q={citystatelist[0]}&limit={limit}&appid={querrystring["APIID"]}'
            try:
                # This try/except will put the abbreviation for the state into the 'state' variable that will be passed into the function
                state = citystatelist[1]
            except:
                # I have a pass statement here because they are already other statements that will print out if this fails.
                # Meaning I have multiple things to catch failures here
                pass
            citystate = 0
        elif zc == 1:
            geocodeurl = f'http://api.openweathermap.org/geo/1.0/zip?zip={zipcode}&appid={querrystring["APIID"]}'
            state = ''
            zc = 0

        # Now the program will call the first function (latlong) to obtain the latitude and longitude information and if the user didn't input a correct variable
        # it'll let them know
        try:
            latlong(geocodeurl, querrystring, headers, zipocity, state)
        except:
            print('Sorry, you did not enter a valid City,State or Zip Code')
            print('Here is an example: Indianapolis,IN or 46240')

        # The following code determines if the user wants to continue or not with getting more weather.
        # The 'again' variable will either be 'Y' to continue with more weather or 'N' to stop
        # If the user fails to enter either, it will prompt them with a fail message and send them back through the weather app again.
        again = input('Would you like to see weather for another location? Type "Y" for Yes or "N" for No: ')
        again = again.strip()
        again = again.lower()
        if again == 'n':
            break
        elif again == 'y':
            continue
        else:
            print('Sorry, you did not enter "Y" or "N", please try again.')


if __name__ == '__main__':
    main()
