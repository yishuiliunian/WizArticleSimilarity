from xmlrpclib import Server

class WizXmlServer(Server):
    def addCommonParams(self, postParams):
        postParams['client_type'] = 'python_command'
        postParams['program_type'] = 'normal'
        postParams['api_version'] = 4
