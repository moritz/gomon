import os
import json
from gocd import Server
from pprint import pprint
from datetime import datetime


def fetch_data(url='http://localhost:8153', **kwargs):
    server = Server(url, **kwargs)
    groups = server.pipeline_groups()
    groups.get_pipeline_groups()

    r_pipeline = {}

    for name in groups.pipelines:
        runs = []

        pipeline = server.pipeline(name)
        
        offset = 0
        keep_going = True
        while keep_going:
            histories = pipeline.history(offset).payload.get('pipelines', [])
            if not histories:
                break

            for p in histories:
                stages = []
                for stage in p['stages']:
                    results = ['notyet'] 
                    jobs = stage.get('jobs', [])
                    time = None
                    if jobs:
                        results = list({ j['result'] for j in jobs })
                        time = max([j['scheduled_date'] for j in jobs])

                    stages.append(dict(results=results, time=time, name=stage['name']))
                runs.append(stages)

                last_results = stages[-1]['results']
                if len(last_results) == 1 and last_results[0] == 'Passed':
                    keep_going = False
                    break
            offset += 10

        r_pipeline[name] = runs
        
    return r_pipeline

destination = 'data/current.json'
filename = '%s.json' % datetime.now().isoformat()
data = fetch_data()
pprint(data)
print(filename)
with open('data/' + filename, 'w') as fh:
    json.dump(data, fh)
try:
    os.remove(destination)
except FileNotFoundError:
    pass

os.symlink(filename, destination)