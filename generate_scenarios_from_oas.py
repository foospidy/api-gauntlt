#!/usr/bin/env python

import json

with open('input/input.json', 'r') as f:
    swagger = json.load(f)

api_schemes = swagger['schemes']
api_consumes = swagger['consumes']
api_produces = swagger['produces']
api_host = swagger['host']
api_version = swagger['info']['version']
api_base_path = swagger['x-basePath'].replace('{version}', api_version)
api_paths = swagger['paths']

"""
Verb Scenarios
"""
with open('scenario_templates/verb.attacks', 'r') as f:
    scenario = f.read()

verbs = ['delete', 'patch', 'trace', 'track', 'bogus', 'get', 'post']
verb_attack_scenario = ''
examples = ''

for path in api_paths:
    allowed_verbs = []

    for method in api_paths[path]:
        if method != 'parameters':
            allowed_verbs.append(method)

    for verb in verbs:
        if verb not in allowed_verbs:
            examples += '    | {} | {}{} | 501 Not Implemented |\n'.format(verb, api_base_path, path)

scenario = scenario.replace('[HOSTNAME', api_host)
scenario = scenario.replace('[EXAMPLES]', examples)

with open('scenarios/verb.attacks', 'w') as f:
    f.write(scenario)
