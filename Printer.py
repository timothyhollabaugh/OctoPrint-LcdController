import socket
import urllib
import urllib2
import json
import thread
import logging

host = "http://localhost:5000"
apiKey = "08723BF9C8EE487CB4B7E3F2D989EA8F"

state = ""
cfile = ""
printTime = 0
printTimeTotal = 0
printTimeLeft = 0
printPer = 0
sdState = False

temperatures = {}
tmpTool = ""

files = {}
tmpFile = 0

def update():
    
    global state
    global cfile
    global printTime
    global printTimeTotal
    global printTimeLeft
    global printPer
    global sdState
    global files
    global temperatures

    # State
    try:
        url = host+"/api/printer"
        req = urllib2.Request(url)
        req.add_header('User-agent', 'LCD Controller')
        req.add_header('X-Api-Key', apiKey)
        resp = json.loads(urllib2.urlopen(req).read())
        
        state = resp["state"]["text"]
        sdState = resp["state"]["flags"]["sdReady"]
        temperatures = resp["temperature"]
    except urllib2.HTTPError as ex:
        if ex.code == 409:
            state = "Disconnected"
        else:
            state = "Octoprint Down! {d}".format(ex.code) 
            logging.warning("Unknown Network Error! HTTP Code %d", ex.code)
    except urllib2.URLError as ex:
        logging.warning("URLError!")
    # Job
    try:
        url = host+"/api/job"
        req = urllib2.Request(url)
        req.add_header('User-agent', 'LCD Controller')
        req.add_header('X-Api-Key', apiKey)
        resp = json.loads(urllib2.urlopen(req).read())
        
        cfile = resp["job"]["file"]["name"]
        printTimeTotal = resp["job"]["estimatedPrintTime"]
        printTimeLeft = resp["progress"]["printTimeLeft"] 
        printTime = resp["progress"]["printTime"]
        printPer = resp["progress"]["completion"]
        
        # Files
        url = host+"/api/files"
        req = urllib2.Request(url)
        req.add_header('User-agent', 'LCD Controller')
        req.add_header('X-Api-Key', apiKey)
        resp = json.loads(urllib2.urlopen(req).read())

        files = resp

    except urllib2.HTTPError as ex:
        state = "Octoprint Down! {d}".format(ex.code) 
        logging.warning("Unknown Network Error! HTTP Code %d", ex.code)
    except urllib2.URLError as ex:
        logging.warning("URLError!")

def setTemp(tool, temp):
    try:
        thread.start_new_thread(isetTemp, (tool, temp, ))
    except thread.error:
        pass

def isetTemp(tool, temp):

    url = host + "/api/printer/"

    body = ""

    if tool == "bed":
        url = url + "bed"
        body = '{"command": "target", "target": %d}' % temp
    else:
        url = url + "tool"
        body = '{"command": "target", "targets": {"%s": %d}}' % (tool, temp)
    
    #try:
    print url
    print body
    
    req = urllib2.Request(url)
    
    req.add_header('User-agent', 'LCD Controller')
    req.add_header('Content-type', "application/json")
    req.add_header('Content-length', len(body))
    req.add_header('X-Api-Key', apiKey)
    req.add_data(body)
    
    print urllib2.urlopen(req).read()

def pprint():
    try:
        thread.start_new_thread(ijob, ("start", ))
    except thread.error:
        pass

def cancel():
    try:
        thread.start_new_thread(ijob, ("cancel", ))
    except thread.error:
        pass

def pause():
    try:
        thread.start_new_thread(ijob, ("pause", ))
    except thread.error:
        pass

def restart():
    try:
        thread.start_new_thread(ijob, ("restart", ))
    except thread.error:
        pass

def ijob(p):
    try:
        print(p)
        url = host + "/api/job"
        
        body = '{"command": "' + p + '"}'
        
        req = urllib2.Request(url)
        
        req.add_header('User-agent', 'LCD Controller')
        req.add_header('Content-type', "application/json")
        req.add_header('Content-length', len(body))
        req.add_header('X-Api-Key', apiKey)
        req.add_data(body)
        
        print urllib2.urlopen(req).read()
    except urllib2.HTTPError:
        pass

def selectFile(f, l, p):
    try:
        thread.start_new_thread(iselectFile, (f, l, p))
    except thread.error:
        pass

def iselectFile(f, l, p):
    url = host + "/api/files/" + l + "/" + f
    
    if p:
        body = '{"command": "select", "print": true}'
    else:
        body = '{"command":"select"}'
    
    req = urllib2.Request(url)
    
    req.add_header('User-agent', 'LCD Controller')
    req.add_header('Content-type', "application/json")
    req.add_header('Content-length', len(body))
    req.add_header('X-Api-Key', apiKey)
    req.add_data(body)
    
    print urllib2.urlopen(req).read()
    
def deleteFile(f, l):
    try:
        thread.start_new_thread(ideleteFile, (f, l))
    except thread.error:
        pass

def ideleteFile(f, l):
    url = host + "/api/files/" + l + "/" + f

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    req = urllib2.Request(url)
    req.get_method = lambda: 'DELETE' # creates the delete method
    req.add_header('User-agent', 'LCD Controller')
    req.add_header('X-Api-Key', apiKey)
        
    print urllib2.urlopen(req).read()

    print url
    
