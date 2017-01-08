from pprint import pprint
import json


class PipelineCollection:
    def __init__(self, pipelines):
        self.pipelines = pipelines
        self.unreleased = self._filter_unreleased()

    def _filter_unreleased(self):
        unreleased = [ p for p in self.pipelines.values() if p['successfull_incomplete_runs'] ]
        unreleased.sort(key=lambda p: - (p['last_timestamp_completed'] - p['last_timestamp']) * p['successfull_incomplete_runs'])
        return unreleased

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

def enrich(pipeline):
    runs = pipeline['runs']
    pipeline.update({
        'last_timestamp': last_timestamp(runs),
        'last_timestamp_completed': last_timestamp_completed(runs),
        'successfull_incomplete_runs': successfull_incomplete_runs(runs),
    })
    return pipeline


def read_data():
    with open('data/current.json') as fh:
        data = json.load(fh)

    data = { name: enrich(p) for name, p in data.items() }
    return PipelineCollection(pipelines=data)
