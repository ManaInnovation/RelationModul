import json
import numpy as np

def parse_property_data(property_json):
    try:
        # Decode JSON data
        return json.loads(property_json['option'])
    except json.JSONDecodeError:
        print("Error: Could not decode JSON.")
        return None

def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return None

def main():
    property1 = {
        "id": "17", "object_id": "1743", "field_id": "19", "field_relation_id": "172", "type": "text",
        "UID": "K0I2QDQJ1JW3A7748M84383282L8045V1",
        "option": "{\"se\":\"74106\",\"UID\":\"0\",\"va\":\"3456\",\"re\":\"12\",\"et\":\"6/2/2024 8:35:06 PM\",\"ut\":\"6/2/2024 8:51:58 PM\",\"op\":\"0\"}"
    }
    property2 = {
        "id": "18", "object_id": "1742", "field_id": "19", "field_relation_id": "172", "type": "text",
        "UID": "8B40B3K36V3M6OAA74H27C08627Q0IP41",
        "option": "{\"se\":\"44013\",\"UID\":\"0\",\"va\":\"A1012A\",\"re\":\"1\",\"et\":\"11/22/2023 12:13:33 PM\",\"ut\":\"11/22/2023 12:13:33 PM\",\"op\":\"0\"}"
    }

    option1 = parse_property_data(property1)
    option2 = parse_property_data(property2)

    if not option1 or not option2:
        print("Error: One of the properties could not be parsed.")
        return

    # Convert data to numeric format
    se1, re1 = convert_to_float(option1['se']), convert_to_float(option1['re'])
    se2, re2 = convert_to_float(option2['se']), convert_to_float(option2['re'])

    # Create a 2D array from the data
    data = np.array([
        [se1, re1],
        [se2, re2]
    ], dtype=float)

    # Calculate covariance
    if data.shape[0] > 1 and data.shape[1] > 1:
        cov_matrix = np.cov(data.T, rowvar=False)
        cov_value = cov_matrix[0, 1]

        # Determine relationship type
        if cov_value > 0:
            relation = "Convergent"
        elif cov_value < 0:
            relation = "Divergent"
        else:
            relation = "Neutral"

        # Print results
        print("2D array of data:")
        print(data)
        print(f"Covariance between the features: {cov_value}")
        print(f"Relationship type: {relation}")
    else:
        print("Error: Not enough data to calculate covariance.")

if __name__ == "__main__":
    main()
