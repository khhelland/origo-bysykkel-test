import requests
import json



def bysykkel_status_request(client_name = "personlig-bysykkel_status"):
    return requests.get("https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"
                                       , headers={"client-name": client_name})
def bysykkel_info_request(client_name = "personlig-bysykkel_status"):
    return  requests.get("https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
                                     , headers={"client-name": client_name})

def get_table(client_name="personlig-bysykkel_status"):

    table = []
    data_received = False


    try:
        response_status = bysykkel_status_request(client_name)
        response_info = bysykkel_info_request(client_name)
    except requests.exceptions.ConnectionError:
        print("Could not connect to bysykkel-API")
        return table, data_received

    if response_status.status_code==200 and response_info.status_code==200:
        try:
            for station_info in response_info.json()['data']['stations']:
                for station_status in response_status.json()['data']['stations']:
                    if station_info['station_id'] == station_status['station_id']:
                        table.append((station_info['name'],
                                      station_status['num_bikes_available'],
                                      station_status['num_docks_available']
                        ))
                        break
            table.sort(key=lambda x: x[0])
            data_received = True
        except (KeyError, IndexError, TypeError):
            print("Received data not in expected form")
    else:
        print("Unexpected status codes:")
        print("Expected 200 for station status request, received " +str(response_status.status_code))
        print("Expected 200 for station information request, received " + str(response_info.status_code))

    return table, data_received
