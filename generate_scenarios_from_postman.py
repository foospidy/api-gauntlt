#!/usr/bin/env python

import sys
import json

class Senarios():
    API = None
    PROFILE = None
    EXAMPLES = None
    scenario = None
    source = None
    target = None
    hostnames = []
    http_methods = ['OPTIONS', 'HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'TRACE', 'TRACK', 'BOGUS', ]

    def __init__(self):
        input = sys.argv[1].split('.')

        with open('input/{}.{}.{}'.format(input[0], input[1], input[2]), 'r') as f:
            self.API = json.load(f)

        self.get_hostnames()

    def get_hostnames(self):
        from urlparse import urlparse

        for request in self.API['requests']:
            hostname = urlparse(request['url']).hostname

            if hostname not in self.hostnames:
                self.hostnames.append(hostname)

    def generate_sslyze_scenario(self):
        """
        SSLyze Scenarios
        """
        for hostname in self.hostnames:
            self.source = 'scenario_templates/sslyze.attack'
            self.target = 'scenarios/sslyze.{}.attack'.format(hostname)

            with open(self.source, 'r') as f:
                self.scenario = f.read()

            self.scenario = self.scenario.replace('[HOSTNAME]', hostname)

            with open(self.target, 'w') as f:
                f.write(self.scenario)

    def generate_verb_scenario(self):
        """
        Verb Scenarios
        """
        self.source = 'scenario_templates/verb.postman.attack'
        self.target = 'scenarios/verb.attack'

        with open(self.source, 'r') as f:
            self.scenario = f.read()

        self.EXAMPLES = '    | method | path | response |\n'
        verbs = ['DELETE', 'PATCH', 'TRACE', 'TRACK', 'BOGUS', 'GET', 'POST']

        for request in self.API['requests']:
            for verb in verbs:
                if verb != request['method']:
                    self.EXAMPLES += '    | {} | {} | 501 Not Implemented |\n'.format(verb, request['url'])

        self.scenario = self.scenario.replace('[EXAMPLES]', self.EXAMPLES)

        with open(self.target, 'w') as f:
            f.write(self.scenario)

    def generate_authn_scenario(self):
        """
        Authentication Scenarios
        """
        self.source = 'scenario_templates/authn.postman.attack'
        self.target = 'scenarios/authn.attack'

        with open('scenario_templates/authn.postman.attack', 'r') as f:
            self.scenario = f.read()

        self.EXAMPLES = '    | method | url |\n'
        verbs = ['OPTIONS', 'HEAD', 'PUT', 'DELETE', 'PATCH', 'TRACE', 'TRACK', 'BOGUS', 'GET', 'POST']

        for request in self.API['requests']:
            for verb in verbs:
                self.EXAMPLES += '    | {} | {} |\n'.format(verb, request['url'])

        self.scenario = self.scenario.replace('[EXAMPLES]', self.EXAMPLES)

        with open(self.target, 'w') as f:
            f.write(self.scenario)

scenario = Senarios()

scenario.generate_sslyze_scenario()
scenario.generate_authn_scenario()
scenario.generate_verb_scenario()
