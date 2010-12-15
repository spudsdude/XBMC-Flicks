import sys
import xbmc, xbmcgui, xbmcplugin
import urllib
from iqueue import *

# plugin modes
MODE1 = 10
MODE1a = 11
MODE1b = 12
MODE2 = 20
MODE3 = 30
MODE4 = 40
MODE5 = 50
MODE6 = 60
MODE6a = 61
MODE6b = 62
MODE6c = 63
MODE6d = 64
MODE6e = 65
MODE6f = 66
MODE6g = 67
MODE6h = 68
MODE6i = 69
MODE6j = 70
MODE6k = 71
MODE6l = 72

# parameter keys
PARAMETER_KEY_MODE = "mode"

# menu item names
SUBMENU1 = "My Instant Queue - ALL"
SUBMENU1a = "My Instant Queue - Movies"
SUBMENU1b = "My Instant Queue - TV Shows"
SUBMENU2 = "Recommended (Filtered for Instant Watch)"
SUBMENU3 = "All New Movies & Shows"
SUBMENU4 = "Search..."
SUBMENU5 = "Top 25 New Movies & Shows"
SUBMENU6 = "By Genre"
SUBMENU6a = "Action & Adventure"
SUBMENU6b = "Children & Family"
SUBMENU6c = "Classics"
SUBMENU6d = "Comedy"
SUBMENU6e = "Documentary"
SUBMENU6f = "Drama"
SUBMENU6g = "Foreign"
SUBMENU6h = "Horror"
SUBMENU6i = "Romance"
SUBMENU6j = "Sci-Fi & Fantasy"
SUBMENU6k = "Television"
SUBMENU6l = "Thrillers"


# plugin handle
handle = int(sys.argv[1])

# utility functions
def parameters_string_to_dict(parameters):
   ''' Convert parameters encoded in a URL to a dict. '''
   paramDict = {}
   if parameters:
       paramPairs = parameters[1:].split("&")
       for paramsPair in paramPairs:
           paramSplits = paramsPair.split('=')
           if (len(paramSplits)) == 2:
               paramDict[paramSplits[0]] = paramSplits[1]
   return paramDict

def addDirectoryItem(name, isFolder=True, parameters={}, thumbnail=None):
   ''' Add a list item to the XBMC UI.'''
   if thumbnail:
      li = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
   else:
      li = xbmcgui.ListItem(name)
   url = sys.argv[0] + '?' + urllib.urlencode(parameters)
   return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url, listitem=li, isFolder=isFolder)


# UI builder functions
def show_root_menu():
   ''' Show the plugin root menu. '''
   addDirectoryItem(name=SUBMENU1, parameters={ PARAMETER_KEY_MODE:MODE1 }, isFolder=True, thumbnail="special://home/addons/plugin.video.xbmcflicks/resources/images/iqueue_all.png")
   addDirectoryItem(name=SUBMENU1a, parameters={ PARAMETER_KEY_MODE:MODE1a }, isFolder=True, thumbnail="special://home/addons/plugin.video.xbmcflicks/resources/images/iqueue_movies.png")
   addDirectoryItem(name=SUBMENU1b, parameters={ PARAMETER_KEY_MODE:MODE1b }, isFolder=True, thumbnail="special://home/addons/plugin.video.xbmcflicks/resources/images/iqueue_tv.png")

   addDirectoryItem(name=SUBMENU2, parameters={ PARAMETER_KEY_MODE:MODE2 }, isFolder=True, thumbnail="special://home/addons/plugin.video.xbmcflicks/resources/images/recog.png")
   addDirectoryItem(name=SUBMENU5, parameters={ PARAMETER_KEY_MODE:MODE5 }, isFolder=True, thumbnail="special://home/addons/plugin.video.xbmcflicks/resources/images/new_top25.png")
   addDirectoryItem(name=SUBMENU3, parameters={ PARAMETER_KEY_MODE:MODE3 }, isFolder=True, thumbnail="special://home/addons/plugin.video.xbmcflicks/resources/images/new_all.png")
   addDirectoryItem(name=SUBMENU4, parameters={ PARAMETER_KEY_MODE:MODE4 }, isFolder=True, thumbnail="special://home/addons/plugin.video.xbmcflicks/resources/images/search.png")
   #addDirectoryItem(name=SUBMENU6, parameters={ PARAMETER_KEY_MODE:MODE6 }, isFolder=True)
   xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_SUBMENU1():
   ''' Show first submenu. '''
   for i in range(0, 5):
       name = "%s Item %d" % (SUBMENU1, i)
       addDirectoryItem(name, isFolder=False)
   xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_SUBMENU2():
   ''' Show second submenu. '''
   for i in range(0, 10):
       name = "%s Item %d" % (SUBMENU2, i)
       addDirectoryItem(name, isFolder=False)
   xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_SUBMENU6():
   #add in the genre folders
   addDirectoryItem(name=SUBMENU6a, parameters={ PARAMETER_KEY_MODE:
MODE6a }, isFolder=True)
   addDirectoryItem(name=SUBMENU6b, parameters={ PARAMETER_KEY_MODE:
MODE6b }, isFolder=True)
   addDirectoryItem(name=SUBMENU6c, parameters={ PARAMETER_KEY_MODE:
MODE6c }, isFolder=True)
   addDirectoryItem(name=SUBMENU6d, parameters={ PARAMETER_KEY_MODE:
MODE6d }, isFolder=True)
   addDirectoryItem(name=SUBMENU6e, parameters={ PARAMETER_KEY_MODE:
MODE6e }, isFolder=True)
   addDirectoryItem(name=SUBMENU6f, parameters={ PARAMETER_KEY_MODE:
MODE6f }, isFolder=True)
   addDirectoryItem(name=SUBMENU6g, parameters={ PARAMETER_KEY_MODE:
MODE6g }, isFolder=True)
   addDirectoryItem(name=SUBMENU6h, parameters={ PARAMETER_KEY_MODE:
MODE6h }, isFolder=True)
   addDirectoryItem(name=SUBMENU6i, parameters={ PARAMETER_KEY_MODE:
MODE6i }, isFolder=True)
   addDirectoryItem(name=SUBMENU6j, parameters={ PARAMETER_KEY_MODE:
MODE6j }, isFolder=True)
   addDirectoryItem(name=SUBMENU6k, parameters={ PARAMETER_KEY_MODE:
MODE6k }, isFolder=True)
   addDirectoryItem(name=SUBMENU6l, parameters={ PARAMETER_KEY_MODE:
MODE6l }, isFolder=True)
   xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

# parameter values
params = parameters_string_to_dict(sys.argv[2])
mode = int(params.get(PARAMETER_KEY_MODE, "0"))
print "##########################################################"
print("Mode: %s" % mode)
print("Arg1: %s" % sys.argv[1])
print("Arg2: %s" % sys.argv[2])
print "##########################################################"

# Depending on the mode, call the appropriate function to build the UI.
if not sys.argv[2]:
   # new start
   ok = show_root_menu()
elif mode == MODE1:
   getInstantQueue()
elif mode == MODE1a:
   getInstantQueue(1)
elif mode == MODE1b:
   getInstantQueue(2)
elif mode == MODE2:
    getRecommendedQueue()
elif mode == MODE3:
    getNewToWatchInstant()
elif mode == MODE4:
    keyboard = xbmc.Keyboard()
    keyboard.doModal()
    if (keyboard.isConfirmed()):
      arg = keyboard.getText()
      #print "keyboard returned: " + keyboard.getText()
      doSearch(arg)
    else:
      print "user canceled"
elif mode == MODE5:
   getNewToWatchInstantTopX()

elif mode == MODE6:
   ok = show_SUBMENU6()
elif mode == MODE6a:
   ok = show_SUBMENU6()
elif mode == MODE6b:
   ok = show_SUBMENU6()
elif mode == MODE6c:
   ok = show_SUBMENU6()
elif mode == MODE6d:
   ok = show_SUBMENU6()
elif mode == MODE6e:
   ok = show_SUBMENU6()
elif mode == MODE6f:
   ok = show_SUBMENU6()
elif mode == MODE6g:
   ok = show_SUBMENU6()
elif mode == MODE6h:
   ok = show_SUBMENU6()
elif mode == MODE6i:
   ok = show_SUBMENU6()
elif mode == MODE6j:
   ok = show_SUBMENU6()
elif mode == MODE6k:
   ok = show_SUBMENU6()
elif mode == MODE6l:
   ok = show_SUBMENU6()
