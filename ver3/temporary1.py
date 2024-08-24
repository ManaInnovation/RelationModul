import requests
import json
from datetime import datetime
from dateutil import parser

class Property:
    def __init__(self, id, object_id, field_id, field_relation_id, prop_type, UID, option):
        self.id = id
        self.object_id = object_id
        self.field_id = field_id
        self.field_relation_id = field_relation_id
        self.prop_type = prop_type
        self.UID = UID
        self.option = option

    def __str__(self):
        return (f"ID: {self.id}, Object ID: {self.object_id}, "
                f"Field ID: {self.field_id}, Field Relation ID: {self.field_relation_id}, "
                f"Type: {self.prop_type}, UID: {self.UID}, Option: {self.option}")
def fetch_property_list(cmd_url, headers):
    try:
        command = {"cmd": "get_all_property_list"}
        response = requests.post(cmd_url, headers=headers, data=json.dumps(command))
        #print("Response Text:", response.text)  # Debug print
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                #print("Parsed JSON Response:", response_data)  # Debug print
                #print("Response Data Type:", type(response_data))  # Check type
                #print("Response Data Keys:", response_data.keys())  # Print keys

                # Accessing the 'finalObj' key
                final_obj = response_data.get('finalObj', None)
                if final_obj is not None:
                    #print("FinalObj Data Type:", type(final_obj))  # Check type

                    if isinstance(final_obj, list):
                        property_list = []
                        for prop_data in final_obj:
                            #print("Property Data Type:", type(prop_data))  # Check each item's type
                            #print("Property Data:", prop_data)  # Debug print each item
                            if isinstance(prop_data, dict):
                                prop = Property(
                                    id=prop_data.get('id'),
                                    object_id=prop_data.get('object_id'),
                                    field_id=prop_data.get('field_id'),
                                    field_relation_id=prop_data.get('field_relation_id'),
                                    prop_type=prop_data.get('type'),
                                    UID=prop_data.get('UID'),
                                    option=prop_data.get('option')
                                )
                                property_list.append(prop)
                            else:
                                print("Warning: Skipping non-dict item in finalObj")
                        return property_list
                    else:
                        print("Error: Expected a list in the finalObj data")
                        return None
                else:
                    print("Error: Key 'finalObj' not found in the response data")
                    return None
            except json.JSONDecodeError:
                print("Error: JSON response could not be decoded")
                return None
        else:
            print(f"Error: Unable to fetch property list, Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Define the base URL and command endpoint
base_url = "http://www.asset23d.ir/api/"
cmd_url = base_url + "CMD"

# Define headers with Content-Type
headers = {
    "Content-Type": "application/json"
}

# Call fetch_property_list function to retrieve property list
property_list = fetch_property_list(cmd_url, headers)

# Process the retrieved property list if successful
array=[]
if property_list:
    now = datetime.now()
    array = []
    for prop in property_list:
        if isinstance(prop.option, str):
            if prop.option.strip().upper() == "NULL":
                continue

            try:
                prop.option = json.loads(prop.option)
            except json.JSONDecodeError:
                print(f"Warning: Failed to decode JSON from option string: {prop.option}")
                continue

        if isinstance(prop.option, dict):
            ut = prop.option.get('ut')
            if isinstance(ut, str):
                try:
                    ut = parser.parse(ut)
                except (ValueError, parser.ParserError):
                    print(f"Warning: 'ut' field could not be parsed: {ut}")
                    continue

            if isinstance(ut, datetime) and ut.date() == now.date():
                array.append(prop)

    for prop in array:
        print(prop)               # This will use the __str__ method of the Property class


print(datetime.now().replace(microsecond=0))