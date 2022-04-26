# Written by Jeffrey LuoZheng
# April 25th 2022
# Please replace the token=demo with your own token when using
# You can get the air qulity token from here https://aqicn.org/data-platform/token/

import sys
import requests
import time


def airquality(latitude_1, longitude_1, latitude_2, longitude_2, minutes,rate):
    # Call the api with two set of lat and long to pull all the stations
    response = requests.get("https://api.waqi.info/v2/map/bounds?latlng=" +
                            latitude_1 + "," + longitude_1 + "," + latitude_2 + "," + longitude_2 + "&networks=all&token=demo")

    # get JSON object
    json_data = response.json() if response and response.status_code == 200 else None
    json_data = json_data["data"]
    
    # save the number of stations
    size = len(json_data)
    
    pm25sum = 0.0
    # Create 2-D matrix that saves all the pm25 samples
    matrix = [[0 for x in range((rate*minutes)-1)] for y in range(size)]
    i = 0
    
    # start timer while time is less than provided minutes
    starttime = time.time()
    while (time.time() - starttime) < (minutes * 60):
        counter = 0
        
        # Loop n number of time base on rate
        while(counter < rate):
            i = 0
            for station in json_data:
                station_response = requests.get("https://api.waqi.info/feed/geo:"+str(station["lat"])+";"+str(
                    station["lon"])+"/?token=demo")
                
                # We append the data to the 2-d matrix
                station_data = station_response.json() if station_response and station_response.status_code == 200 else None
                pm25data = station_data["data"]["iaqi"]["pm25"]["v"]
                matrix[i].append(pm25data)
                i = i + 1
            counter = counter + 1
            
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
        
    i = 0
    # loop over each station and print to the console
    for station in json_data:
        print("station name: " + station["station"]["name"])
        print("pm25: ")
        average = 0
        for j in range(len(matrix[i])):
            print(str(matrix[i][j]))
            average += matrix[i][j]
        average = average/len(matrix[i])
        i = i + 1
        pm25sum += average

    print("Average pm25 over all queried station: " + str(round(pm25sum/size, 2)))

# program check for number of parameters
if len(sys.argv) == 5:
    airquality(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 1, 1)
elif len(sys.argv) == 6:
    airquality(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5], 1)
elif len(sys.argv) == 7:
    airquality(sys.argv[1], sys.argv[2], sys.argv[3],
               sys.argv[4], sys.argv[5], sys.argv[6])
else:
    print("Invalid number of arguments")
