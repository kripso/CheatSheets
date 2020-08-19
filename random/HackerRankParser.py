import json

with open('kripsoworld_data.json') as json_file:
    data = json.load(json_file)

    if 'submissions' in data:
        new_data = {}
        new_data['code'] = []

        for code in data['submissions'][1:]:
            new_data['code'].append(code['code'])

        print(new_data)
        with open('kripsoworld_data.json', 'w') as json_file:
            json.dump(new_data, json_file)

# indents Json data for printing

with open('kripsoworld_data.json') as json_file:
    data = json.load(json_file)
    printable_data = json.dumps(data, indent=4)
    print(printable_data)
