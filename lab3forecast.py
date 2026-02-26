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




    #step 1

    whois = getstatusoutput(f"whois {argv[1]}")[1]


    if showTestCode:
        print("here is the whois response: ")
        print(whois)



    # initialize variables
    address = " "
    cityStateZip = " "
    thirdAddressLine = " "


    # gets address
    whois_lines = whois.split('\n')
    for line in whois_lines:
        if "address" in line:
            address = line.split(':')[1].strip()
            nextLineIndex = whois_lines.index(line) + 1
            nextLine = whois_lines[nextLineIndex]
            nextNextLineIndex = whois_lines.index(nextLine) + 1
            nextNextLine = whois_lines[nextNextLineIndex]
            cityStateZip = nextLine.split(':')[1].strip()
            thirdAddressLine = nextNextLine.split(':')[1].strip()
            break


    # debug code
    if showTestCode:
        print(address)
        print(cityStateZip)
        print("Here is the third address line: ")
        print(thirdAddressLine)


    if "Suite" in cityStateZip:
        if showTestCode:
            print("there is a suite in the citystatezip so using the alt line")
            # this is to make sure the address is formatted properly
        cityStateZip = thirdAddressLine



    # formatting address stuff correctly
    city = cityStateZip.split(' ')[0].replace(' ', '+')
    if showTestCode:
        print(city)
    state = cityStateZip.split(' ')[1].replace(' ', '+')
    if showTestCode:
        print(state)
    zipcode = cityStateZip.split(' ')[2]
    if showTestCode:
        print(zipcode)

    street = address.replace(' ', '+')
    if showTestCode:
        print(street)




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
    lat = js['result']['addressMatches'][0]['coordinates']['y']
    lon = js['result']['addressMatches'][0]['coordinates']['x']

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
    forecast_URL = js['properties']['forecast']


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
    tempPeriod = js['properties']['periods'][0]['detailedForecast']

    # temperatureArray = []

    # get array of numbers for graph
    # for period in tempPeriods:
    #     if showTestCode:
    #         print(period['temperature']) #shows temperature number
    #     temperatureArray.append(int(period['temperature']))



    if showTestCode:
        print("here is the temperatures array:")
        # print(temperatureArray)


    if showAPIInfo:
        print("Here is the forecast for the address you entered:")
    # plot_temps(temperatureArray)
    print(tempPeriod)

    # print("here is an example of plot tempatures: ")
    # plot_temps([70,72,75,78,70,65,60])

if __name__ == "__main__":
    main()

