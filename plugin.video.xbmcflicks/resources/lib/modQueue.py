from Netflix import *
import getopt
import time 
import re
import xbmcplugin
import xbmcgui
import urllib
import xbmc
import webbrowser

MY_USER = {
        'request': {
             'key': '',
             'secret': ''
        },
        'access': {
            'key': '',
            'secret': ''
        }
}

class XInfo:
    def __init__(self):
        self.Mpaa = "n/a"
        self.Position = "0"
        self.Year = "1970"
        self.Title = "Item Full Title Name"
        self.TitleShort = "Short Item Title"
        self.TitleShortLink = "Short Item Title with no spaces"
        self.Rating = ""
        self.Runtime = "0"
        self.Genres = ""
        self.ID = ""
        self.FullId = ""
        self.Poster = ""
        self.Cast = ""
        self.Synop = ""

def __init__(self):
    self.data = []

def getAuth(netflix, verbose):
    print ".. getAuth called .."
    netflix.user = NetflixUser(MY_USER,netflix)
    print ".. user configured .."

    #handles all the initial auth with netflix
    if MY_USER['request']['key'] and not MY_USER['access']['key']:
        tok = netflix.user.getAccessToken( MY_USER['request'] )
        if(verboseUser):
            print "now put this key / secret in MY_USER.access so you don't have to re-authorize again:\n 'key': '%s',\n 'secret': '%s'\n" % (tok.key, tok.secret)
        MY_USER['access']['key'] = tok.key
        MY_USER['access']['secret'] = tok.secret
        saveUserInfo()
        dialog = xbmcgui.Dialog()
        dialog.ok("Settings completed", "You must restart the xbmcflicks plugin")
        print "Settings completed", "You must restart the xbmcflicks plugin"
        sys.exit(1)

    elif not MY_USER['access']['key']:
        (tok, url) = netflix.user.getRequestToken()
        if(verboseUser):
            print "Authorize user access here: %s" % url
            print "and then put this key / secret in MY_USER.request:\n 'key': '%s',\n 'secret': '%s'\n" % (tok.key, tok.secret)
            print "and run again."
        #open web page with urllib so customer can authorize the app
        webbrowser.open(url)
        #display click ok when finished adding xbmcflicks as authorized app for your netflix account
        dialog = xbmcgui.Dialog()
        ok = dialog.ok("After you have linked xbmcflick in netflix.", "Click OK after you finished the link in your browser window.")
        MY_USER['request']['key'] = tok.key
        MY_USER['request']['secret'] = tok.secret
        #now run the second part, getting the access token
        tok = netflix.user.getAccessToken( MY_USER['request'] )
        if(verboseUser):
            print "now put this key / secret in MY_USER.access so you don't have to re-authorize again:\n 'key': '%s',\n 'secret': '%s'\n" % (tok.key, tok.secret)
        MY_USER['access']['key'] = tok.key
        MY_USER['access']['secret'] = tok.secret
        #now save out the settings
        saveUserInfo()
        #exit script, user must restart
        dialog.ok("Settings completed", "You must restart the xbmcflicks plugin")
        print "Settings completed", "You must restart the xbmcflicks plugin"
        sys.exit(1)

    return netflix.user

def saveUserInfo():
    #create the file
    f = open('special://home/addons/plugin.video.xbmcflicks/resources/usersettings/userinfo.txt','r+')
    setting ='requestKey=' + MY_USER['request']['key'] + '\n' + 'requestSecret=' + MY_USER['request']['secret'] + '\n' +'accessKey=' + MY_USER['access']['key']+ '\n' + 'accessSecret=' + MY_USER['access']['secret']
    f.write(setting)
    f.close()

def initApp():
    global APP_NAME
    global API_KEY
    global API_SECRET
    global CALLBACK
    global user
    global counter
    global debug
    global verboseUser
    
    APP_NAME = 'xbmcflix'
    API_KEY = 'gnexy7jajjtmspegrux7c3dj'
    API_SECRET = '179530/200BkrsGGSgwP6446x4x22astmd5118'
    CALLBACK = ''
    counter = '0'
    debug = False
    verboseUser = False
    
    reobj = re.compile(r"200(.{10}).*?644(.*?)4x2(.).*?5118")
    match = reobj.search(API_SECRET)
    if match:
        result = match.group(1)
        API_SECRET = result
    #load the userinfo.properties file
    userstring = open('special://home/addons/plugin.video.xbmcflicks/resources/usersettings/userinfo.txt', 'r').read()
    reobj = re.compile(r"requestKey=(.*)\nrequestSecret=(.*)\naccessKey=(.*)\naccessSecret=(.*)")
    match = reobj.search(userstring)
    if match:
        print "matched file contents, it is in the correct format"
        MY_USER['request']['key'] = match.group(1).strip()
        MY_USER['request']['secret'] = match.group(2).strip()
        MY_USER['access']['key'] = match.group(3).strip()
	MY_USER['access']['secret'] = match.group(4).strip()
	print "finished loading up user information from file"
    else:
        #no match, need to fire off the user auth from the start
	print "couldn't load user information from userinfo.properties file"

if __name__ == '__main__':
    initApp()
    if ( len( sys.argv ) > 1 ):
        print str(len(sys.argv))
        print str(sys.argv[0])
        print str(sys.argv[1])

    strArgs = str(sys.argv[1])
    movieid = ""
    action = ""
    details = ""
    match = re.search(r"(.*?)(delete|post)", strArgs, re.IGNORECASE)
    if match:
	movieid = match.group(1)
	print movieid
	action = match.group(2)
	print action
    else:
        "print unable to parse action item, exiting"
        exit
    
    netflixClient = NetflixClient(APP_NAME, API_KEY, API_SECRET, CALLBACK, verboseUser)
    #auth the user
    user = getAuth(netflixClient,verboseUser)

    #if we have a user, do the action
    if user:
        print "got user from main init of modQueue script"
        result = user.modifyQueue(str(movieid), str(action))
        matchr = re.search(r"'message': u'(.*?)'", str(result), re.IGNORECASE)
        if matchr:
            details = matchr.group(1)
        else:
            details = str(result)
        dialog = xbmcgui.Dialog()
        ok = dialog.ok("Results of " + action + " for movie id " + movieid, details)

        #refresh UI on delete
        if(action == "delete"):
            xbmc.executebuiltin("Container.Refresh")
