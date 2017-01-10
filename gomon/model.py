from pprint import pprint
from datetime import datetime
import humanize
import json
import os

now = datetime.now()

def map_results(results):
    if len(results) == 1:
        return results[0].lower()
    return 'mixed'

class PipelineCollection:
    def __init__(self, pipelines, last_updated):
        self.last_updated = last_updated
        self.pipelines = pipelines
        self.unreleased = self._filter_unreleased()
        self.failed = self._filter_failed()
        self.paused = [ p for p in self.pipelines.values() if p['paused'] ]

    def _filter_unreleased(self):
        unreleased = [ p for p in self.pipelines.values() if p['successfull_incomplete_runs'] and not p['paused'] ]
        now = int(datetime.now().timestamp()) * 1000
        unreleased.sort(key=lambda p: (-p['successfull_incomplete_runs'], -(p['last_timestamp'] - (p['last_timestamp_completed'] or 0))))
        return unreleased

    def _filter_failed(self):
        failed = [ p for p in self.pipelines.values() if p['result'] == 'failed' and not p['paused'] ]
        return failed

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

def pipeline_result(stages):
    for stage in reversed(stages):
        if stage['results'] == ['notyet']:
            pass
        elif stage['results'] == ['Passed']:
            return 'Passed'
        else:
            return map_results(stage['results'])
    return 'notyet'

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

def deep_map_results(runs):
    for run in runs:
        for stage in run:
            stage['result'] = map_results(stage['results']) 



def enrich(pipeline):
    runs = pipeline['runs']
    deep_map_results(runs)
    pipeline.update({
        'last_timestamp': last_timestamp(runs),
        'last_timestamp_completed': last_timestamp_completed(runs),
        'successfull_incomplete_runs': successfull_incomplete_runs(runs),
        'result': pipeline_result(runs[0]),
    })
    if pipeline['last_timestamp_completed']:
        delta = now - datetime.fromtimestamp(int(pipeline['last_timestamp_completed'] / 1000))
        label = humanize.naturaltime(delta)
    else:
        label = 'never'
    pipeline['last_completed'] = label
        
    return pipeline


def read_data():
    with open('data/current.json') as fh:
        data = json.load(fh)
    original = os.readlink('data/current.json')
    last_updated = original[:-5]

    data = { name: enrich(p) for name, p in data.items() }
    return PipelineCollection(pipelines=data, last_updated=last_updated)
