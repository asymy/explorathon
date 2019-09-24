
import json


def savedata(newdata):
    import json
    with open('data.json') as f:
        data = json.load(f)
    data['age'].append(newdata['age'])
    data['gender'].append(newdata['gender'])
    data['HPT'].append(newdata['HPT'])
    data['CDT'].append(newdata['CDT'])
    data['WDT'].append(newdata['WDT'])
    with open('data.json', 'w') as f:
        json.dump(data, f)


# data = {
#     'age': [25, 23],
#     'gender': ['female', 'male'],
#     'HPT': [43.0, 43.1],
#     'CDT': [31.1, 30.7],
#     'WDT': [33.2, 33.1]
# }

newdata = {
    'age': 25,
    'gender': 'female',
    'HPT': 43.0,
    'CDT': 31.1,
    'WDT': 33.1
}


savedata(newdata)
