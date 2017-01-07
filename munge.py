from pprint import pprint
import json


def last_timestamp(runs):
    time = 0
    for run in runs:
        for stage in run:
            t = stage.get('time', None)
            if t and t > time:
                time = t
    if not time:
        time = None
    return time

def last_timestamp_completed(runs):
    time = 0
    for run in runs:
        if ','.join(run[-1]['results']) == 'Passed':
            return run[-1]['time']

def successfull_incomplete_runs(runs):
    count = 0
    for run in runs:
        if run[-1]['results'] == ['Passed']:
            return count
        
        for stage in reversed(run):
            if stage['results'] == ['notyet']:
                pass
            elif stage['results'] == ['Passed']:
                count += 1
                break
            else:
                break
    return count

def enrich(pipeline, name):
    return {
        'runs': pipeline,
        'name': name,
        'last_timestamp': last_timestamp(pipeline),
        'last_timestamp_completed': last_timestamp_completed(pipeline),
        'successfull_incomplete_runs': successfull_incomplete_runs(pipeline),
    }

with open('data/current.json') as fh:
    data = json.load(fh)
    pprint(data)

data = { name: enrich(p, name) for name, p in data.items() }
pprint(data)
