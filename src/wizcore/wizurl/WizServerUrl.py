import httplib

serverurl = 'http://service.wiz.cn/wizkm/xmlrpc'

def WizUrlWithCommand(command):
    version = 1.0
    debug = 1
    plat = 'ios'
    url = "api.wiz.cn"
    dir = " /?p=wiz&v=%d&c=%s&plat=%s&debug=%d" % (version, command ,plat, bool(debug))
    connection = httplib.HTTPConnection(url, 80)
    connection.request('GET', dir)
    serverurl = connection.getresponse().read()
    connection.close()
 

def WizServerUrl():
    global serverurl
    if cmp(serverurl, "aaa") != 0:
        return serverurl

    serverurl = WizUrlWithCommand('sync_http')
    return serverurl

