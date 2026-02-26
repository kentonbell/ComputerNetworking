# author: Kenton Bell

from flask import Flask
from json import loads
from requests import get
from socket import gethostbyname
from subprocess import getstatusoutput



app = Flask(__name__)

dictionaryAddresses = {}

def add_to_dict(key, value):
    dictionaryAddresses[key] = value

def doesexist(key):
    if key in dictionaryAddresses:
        return True
    else:
        return False

def get_value(key):
    return dictionaryAddresses[key]


dictionaryWeather = {}

def add_to_dict_weather(key, value):
    dictionaryWeather[key] = value

def doesexist_weather(key):
    if key in dictionaryWeather:
        return True
    else:
        return False

def get_value_weather(key):
    return dictionaryWeather[key]

dictionaryRange = {}

def add_to_dict_range(key, value):
    dictionaryRange[key] = value

def doesexist_range(key):
    if key in dictionaryRange:
        return True
    else:
        return False

def get_value_range(key):
    return dictionaryRange[key]


def get_address(domain):

    if doesexist(domain):
        return "Cached: " + get_value(domain)

    showTestCode = True
    showAddressInfo = False
    showAPIInfo = True

    #step 1



    # initialize variables
    address = " "
    cityStateZip = " "
    thirdAddressLine = " "


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

    add_to_dict(domain, addressPrint)

    return addressPrint


def get_forecast(domain):

    if doesexist_weather(domain):
        return "Cached: " + get_value_weather(domain)


    # these show helpful PRINT code for debugging purposes
    # # # # to have nothing run in command line, set all to false
    showTestCode = False
    showAddressInfo = False
    showAPIInfo = False

    finalResponse = ""

    # step 1



    # initialize variables
    address = " "
    cityStateZip = " "
    thirdAddressLine = " "



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

    # https://geocoding.geo.census.gov/geocoder/locations/address?street=4600+Silver+Hill+Rd&city=Washington&state=DC&zip=20233&benchmark=Public_AR_Current&format=json
    geocoding_s = "https://geocoding.geo.census.gov/geocoder/locations/address?street="
    # 4600+Silver+Hill+Rd&city=Washington&state=DC&zip=20233&benchmark=Public_AR_Current&format=json
    geocoding_s += street + "&city=" + city + "&state=" + state + "&zip=" + zipcode + "&benchmark=Public_AR_Current&format=json"

    addressPrint = street.replace('+', ' ') + " " + city.replace('+', ' ') + ", " + state.replace('+',
                                                                                                  ' ') + " " + zipcode
    if showAddressInfo:
        print("The address we are looking at weather for is: ")
        print(addressPrint)
    #
    # finalResponse += "\n<br><br>The address we are looking at weather for is: "
    # finalResponse += addressPrint + "\n<br><br>"


    if showTestCode:
        print("here is the geocoding string:")
        print(geocoding_s)

    # getting address response
    try:
        weatherResponse = get(geocoding_s)  # takes forever sometimes
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

    # step 4
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
    #
    # finalResponse += "\n<br><br>Here is the forecast URL: " + forecast_URL + "\n<br><br>"

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

    # finalResponse += "\n<br><br>Here is the forecast for the address you entered: <br><br>" + tempPeriod + "\n"
    # plot_temps(temperatureArray)
    # print(tempPeriod)
    finalResponse += tempPeriod

    add_to_dict_weather(domain, finalResponse)

    return finalResponse







def get_Range(domain):


    if doesexist_range(domain):
        return "Cached: " + get_value_range(domain)


    showTestCode = False



    # step 1

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

    netRange = ""

    for line in whois.split('\n'):
        if "netrange:" in line.lower():
            netRange = line.split(':', 1)[1].strip()
            break

    if not netRange:
        netRange = "Unknown"
        if showTestCode:
            print("Warning: NetRange not found.")

    add_to_dict_range(domain, netRange)
    # print("here is the net range: ")
    return netRange.strip()


@app.route("/address/<domain>")
def addressRoute(domain):
    # status, output = getstatusoutput(f"whois {domain}")
    return get_address(domain)




@app.route("/weather/<domain>")
def weatherRoute(domain):
    # status, output = getstatusoutput(f"whois {domain}")
    return get_forecast(domain)



@app.route("/range/<domain>")
def addressRange(domain):
    # status, output = getstatusoutput(f"whois {domain}")
    return get_Range(domain)





@app.route("/upper/<echo_string>")
def upper(echo_string):
    return echo_string.upper()


@app.route("/callwhois/<domain>")
def whois(domain):
    status, output = getstatusoutput(f"whois {domain}")
    return output.split("\n")




@app.route('/')
def hello():
    string = "Hello, World! I hope you're having a great day! Here's the main page"

    string += "<br><br>Here's the IP address of this server: " + gethostbyname(gethostbyname("localhost"))

    string += "<br><br><br><br>Here is what you can do on this page: "

    string += "<br><br>1. Enter a Website or IP address with keyword 'address' and I'll give you the address information"
    string += "<br>You can enter this into the URL bar: http://127.0.0.1:5000/address/anythingYOUwant"

    string += "<br><br>2. Enter a Website or IP address keyword 'weather' and I'll give you the weather forecast"
    string += "<br>You can enter this into the URL bar: http://127.0.0.1:5000/weather/anythingYOUwant"

    string += "<br><br>3. Enter a Website or IP address keyword 'range' and I'll give you IP range of the domain"
    string += "<br>You can enter this into the URL bar: http://127.0.0.1:5000/range/anythingYOUwant"

    string += "<br><br><br>4. Enter a Website or IP address keyword 'upper' and I'll give you the string you wanted in all caps"
    string += "<br>You can enter this into the URL bar: http://127.0.0.1:5000/upper/anythingYOUwant"

    string += "<br><br>5. Enter a Website or IP address keyword 'callwhois' and I'll give you the whois information"
    string += "<br>You can enter this into the URL bar: http://127.0.0.1:5000/callwhois/anythingYOUwant"

    string += "<br><br><br><br>That's all! Enjoy the website!!!"

    # string += "<br><br>Here's the whois information for 8.8.8.8: " + whois("8.8.8.8")

    # string += "<br><br>Here's the JSON response from the API: " + loads(get("https://ip-api.com/json").text)["country"]

    # string += "<br><br>Here's the HTML response from the API: " + get("https://ip-api.com/html").text
    #
    # string += "<br><br>Here's the raw HTML response from the API: " + get("https://ip-api.com/html").text
    #
    # string += "<br><br>Here's the raw JSON response from the API: " + get("https://ip-api.com/json").text
    #
    # string += "<br><br>Here's the raw text response from the API: " + get("https://ip-api.com/text").text



    return string


if __name__ == "__main__":
    app.run()
