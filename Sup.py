import re

import requests
import json
import pika

class Sup:

    def __init__(self):
        self.stateFile = "state.json"
        self.states = self.loadStates()


    def loadStates(self):
        try:
            with open(self.stateFile, 'r') as f:
                return json.load(f)
        except:
            return {}

    def saveState(self):
        with open(self.stateFile, 'w') as f:
            json.dump(self.states, f)

    def callback(self, channel, method, properties, body):

        message = json.loads(body.decode('utf-8'))
        fqdn = message['fqdn']
        for check in message['checks']:

            if check['status'] != self.getCheckStatus(check['name'], fqdn) and re.match(r'OK|CRITICAL', check['status']):
                self.states[fqdn][check['name']] = check
                self.saveState()
                self.sendMessage(fqdn, check)

            elif check['status'] != self.getCheckStatus(check['name'], fqdn) and check['status'] == 'WARNING':
                self.states[fqdn][check['name']] = check
                self.saveState()


    def getCheckStatus(self, check_name, fqdn):

        try:
            return self.states[fqdn][check_name]['status']
        except KeyError:
            return ''

    def sendMessage(self, fqdn, check):

        notificationRecipients = self.getNotificationRecipients(fqdn, check['name'], check['status'])

        if check['status'] == 'OK':
            self.sendRecoveryMessage(notificationRecipients, fqdn, check)
        elif check['status'] == 'CRITICAL':
            self.sendAlertingMessage(notificationRecipients, fqdn, check)

    def getNotificationRecipients(self, fqdn, check_name, check_status):

        # Check if line of a csv file and match on fqdn and check_name
        # If match, return the recipients
        # If not match, return empty list
        pass

    def sendRecoveryMessage(self, recipients, fqdn, check):

        # Send a recovery message to the recipients
        pass

    def sendAlertingMessage(self, recipients, fqdn, check):

        # Send an alerting message to the recipients
        pass



if __name__ == '__main__':
    sup = Sup()

    message = b'{"fqdn": "toto.rtg.hbgt.infra.net", "checks": [{"name" : "files_blocked", "status" : "OK", "timestamp" : "1518098983","message" : "All OK !"}]}'
    sup.callback('', '', '', message)
