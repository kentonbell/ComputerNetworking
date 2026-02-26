#! /usr/bin/env python3
# author: TODO: Kenton Bell

from json import loads  # steps 3, 4
from requests import get  # steps 3, 4
from socket import gethostbyname  # step 1
from subprocess import getstatusoutput  # step 2
from sys import argv  # command line arguments
import matplotlib.pyplot as plt #for temp plotting function
import numpy as np #for temp plotting function

# Takes an array of temps
# and plots them.
def plot_temps(temps):
    xs = [x for x in range(len(temps))]
    plt.plot(xs, temps, label="Hourly temperatures")

    #Label the x and y
    plt.xlabel("Hour")
    plt.ylabel("Temperature F.")
    #Make sure we show the legend.
    plt.legend()
    #Show the plot
    plt.show()


def main():
    # TODO: Look at the code below for an example of how to do
    # API calls. I would recommend first uncommenting and
    # understanding the code, and then commenting the code back
    # out. The code is, largely, step 4.
    # base API string for weather.gov




    # these show helpful PRINT code for debugging purposes
    # # # # to have nothing run in command line, set all to false
    showTestCode = False
    showAddressInfo = True
    showAPIInfo = True



    #this is the input
    domain = argv[1]

    #step 1
    if all(c.isdigit() or c == '.' for c in domain):
        whois = getstatusoutput(f"whois {domain}")[1]
    else:
        temp2 = gethostbyname(domain)
        if not temp2:
            if showTestCode:
                print("No IP address found in nslookup output.")


        whois = getstatusoutput(f"whois {temp2}")[1]


    if showTestCode:
        print("here is the whois response: ")
        print(whois)



    # initialize variables
    address = " "
    cityStateZip = " "
    thirdAddressLine = " "

    address = ""
    city = ""
    state = ""
    zipcode = ""

    foundAdress = False

    for line in whois.split('\n'):
        line = line.strip()
        if line.lower().startswith("address:"):
            if not foundAdress:
                address = line.split(":", 1)[1].strip()
                foundAdress = True
        elif line.lower().startswith("city:"):
            city = line.split(":", 1)[1].strip()
        elif line.lower().startswith("stateprov:"):
            state = line.split(":", 1)[1].strip()
        elif line.lower().startswith("postalcode:"):
            zipcode = line.split(":", 1)[1].strip()


    if not all([address, city, state, zipcode]):
        print("FAIL: Could not extract full address info from whois.")
        return

    street = address.replace(' ', '+').replace(',', '').replace('.', '').strip()
    city = city.replace(',', '').replace('.', '').strip()
    state = state.strip()
    zipcode = zipcode.strip()

    if showTestCode:
        print("Street:", street)
        print("City:", city)
        print("State:", state)
        print("Zip:", zipcode)



    # getting address lookup script to send in

    #https://geocoding.geo.census.gov/geocoder/locations/address?street=4600+Silver+Hill+Rd&city=Washington&state=DC&zip=20233&benchmark=Public_AR_Current&format=json
    geocoding_s = "https://geocoding.geo.census.gov/geocoder/locations/address?street="
    #4600+Silver+Hill+Rd&city=Washington&state=DC&zip=20233&benchmark=Public_AR_Current&format=json
    geocoding_s += street + "&city=" + city + "&state=" + state + "&zip=" + zipcode + "&benchmark=Public_AR_Current&format=json"

    addressPrint = street.replace('+',' ') + " " + city.replace('+',' ') + ", " + state.replace('+',' ') + " " + zipcode
    if showAddressInfo:
        print("The address we are looking at weather for is: ")
        print(addressPrint)

    if showTestCode:
        print("here is the geocoding string:")
        print(geocoding_s)



    # getting address response
    try:
        weatherResponse = get(geocoding_s) #takes forever sometimes
    except:
        print("there was an error with the geocoding address lookup")
        print("try with a different address")
        return




    if showTestCode:
        print("here is the weather script response:")
        print(weatherResponse.text)

    # get java script
    try:
        js = loads(weatherResponse.text)
    except:
        print("there was an error with the json parse for the geocoding address lookup")
        print("try with a different address")
        return

    if showTestCode:
        print("here is the json:")
        print(js)

    # getting coordinates from dictionary
    # check if any address matches were found
    matches = js.get("result", {}).get("addressMatches", [])
    if not matches:
        print("No address matches found for:", addressPrint)
        print(geocoding_s)
        return  # or return a default message like "Address not found"

    # getting coordinates from dictionary
    lat = matches[0]['coordinates']['y']
    lon = matches[0]['coordinates']['x']

    # getting coordinates string from dictionary for the next api call
    latString = str(lat)
    lonString = str(lon)

    if showTestCode:
        print("here is the lat as a string: ")
        print(latString)
        print("here is the lon as a string: ")
        print(lonString)




    #step 4
    # base address for last api call
    weather_s = "https://api.weather.gov/points/"

    # use the commandline input and the weather_s to make API call

    # getting api call
    try:
        response = get(weather_s + latString + "," + lonString)
    except:
        print("there was an error with the weather.gov coordinates api call")
        print("try with a different address")
        return



    # convert it to json
    if showTestCode:
        print("here is the json:")
        # print(js)
    try:
        js = loads(response.text)
    except:
        print("there was an error with the json parse for the weather.gov coordinates api call")
        print("try with a different address")
        return


    # find the forecast URL based on the API page
    forecast_URL = js['properties']['forecastHourly']


    # print link that we use for next API call
    if showAPIInfo:
        print("Here is the forecast URL:")
        print(forecast_URL)


    # call the API again to get theforecast
    if showTestCode:
        print("here is the final response:")
        # print(final_response.text)
    try:
        final_response = get(forecast_URL)
    except:
        print("there was an error with the forecast hourly final api call")
        print("try with a different address")
        return


    # parse json
    if showTestCode:
        print("here is the final json:")
        # print(js)
    try:
        js = loads(final_response.text)
    except:
        print("there was an error with the json parse for the forecast hourly final api call")
        print("try with a different address")
        return

    # print the forecast
    if showTestCode:
        print("here is the temps!:")
    tempPeriods = js['properties']['periods']

    temperatureArray = []

    # get array of numbers for graph
    for period in tempPeriods:
        if showTestCode:
            print(period['temperature']) #shows temperature number
        temperatureArray.append(int(period['temperature']))



    if showTestCode:
        print("here is the temperatures array:")
        print(temperatureArray)


    if showAPIInfo:
        print("Here are the hourly temperatures plotted over the past 7 days:")
    plot_temps(temperatureArray)


    # print("here is an example of plot tempatures: ")
    # plot_temps([70,72,75,78,70,65,60])

if __name__ == "__main__":
    main()




