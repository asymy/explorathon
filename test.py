
import json


def savedata(newdata):
    import json
    with open('data.json') as f:
        data = json.load(f)
    data.update(newdata)
    with open('data.json', 'w') as f:
        json.dump(data, f)


d = {
    '1': 1,
    '2': 2
}

results = {
    '2': d
}

savedata(results)
