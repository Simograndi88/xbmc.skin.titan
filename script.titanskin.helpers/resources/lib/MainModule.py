import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
import shutil
import xbmcaddon
import xbmcvfs
import os
import time
import urllib
import xml.etree.ElementTree as etree
import random

doDebugLog = False

def logMsg(msg, level = 1):
    if doDebugLog == True:
        xbmc.log(msg)

def sendClick(controlId):
    win = xbmcgui.Window( 10000 )
    time.sleep(0.5)
    xbmc.executebuiltin('SendClick('+ controlId +')')

def defaultSettings():
    # skins default settings for artist slideshow
    if xbmc.getCondVisibility("System.HasAddon(script.artistslideshow)"):
        __settings__ = xbmcaddon.Addon(id='script.artistslideshow')
        __settings__.setSetting('transparent', "true")
      
def musicSearch():
    xbmc.executebuiltin( "ActivateWindow(MusicLibrary)" )
    xbmc.executebuiltin( "SendClick(8)" )
        
def showWidget():
    win = xbmcgui.Window( 10000 )
    linkCount = 0
    xbmc.executebuiltin('Control.SetFocus(77777,0)')
    while linkCount !=10 and not xbmc.getCondVisibility("ControlGroup(77777).HasFocus"):
        time.sleep(0.1)
        if not xbmc.getCondVisibility("ControlGroup(77777).HasFocus"):
            xbmc.executebuiltin('Control.SetFocus(77777,0)')
        linkCount += 1
    
def setWidget(containerID):
    win = xbmcgui.Window( 10000 )
    win.clearProperty("activewidget")
    win.clearProperty("customwidgetcontent")
    skinStringContent = ""
    customWidget = False
    
    # workaround for numeric labels (get translated by xbmc)
    skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(submenuVisibility)")
    skinString = skinString.replace("num-","")
    if xbmc.getCondVisibility("Skin.String(widget-" + skinString + ')'):
        skinStringContent = xbmc.getInfoLabel("Skin.String(widget-" + skinString + ')')
    
    # normal method by getting the defaultID
    if skinStringContent == "":
        skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(defaultID)")
        if xbmc.getCondVisibility("Skin.String(widget-" + skinString + ')'):
            skinStringContent = xbmc.getInfoLabel("Skin.String(widget-" + skinString + ')')
       
    if skinStringContent != "":
 
        if "$INFO" in skinStringContent:
            skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
            skinStringContent = skinStringContent.replace(")]", "")
            skinStringContent = win.getProperty(skinStringContent)
            customWidget = True
        if "Activate" in skinStringContent:
            skinStringContent = skinStringContent.split(",",1)[1]
            skinStringContent = skinStringContent.replace(",return","")
            skinStringContent = skinStringContent.replace(")","")
            skinStringContent = skinStringContent.replace("\"","")
            customWidget = True
        if ":" in skinStringContent:
            customWidget = True
            
        if customWidget:
             win.setProperty("customwidgetcontent", skinStringContent)
             win.setProperty("activewidget","custom")
        else:
            win.clearProperty("customwidgetcontent")
            win.setProperty("activewidget",skinStringContent)

    else:
        win.clearProperty("activewidget")

def setCustomContent(skinString):
    #legacy
    win = xbmcgui.Window( 10000 )
    skinStringContent = xbmc.getInfoLabel("Skin.String(" + skinString + ')')

    if "$INFO" in skinStringContent:
        skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
        skinStringContent = skinStringContent.replace(")]", "")
        skinStringContent = win.getProperty(skinStringContent)    

    if "Activate" in skinStringContent:
        skinStringContent = skinStringContent.split(",",1)[1]
        skinStringContent = skinStringContent.replace(",return","")
        skinStringContent = skinStringContent.replace(")","")
        skinStringContent = skinStringContent.replace("\"","")
           
        xbmc.executebuiltin("Skin.SetString(" + skinString + ','+ skinStringContent + ')')         

    win.setProperty("customwidgetcontent", skinStringContent)
        
def updatePlexlinks():
    win = xbmcgui.Window( 10000 )
    logMsg("update plexlinks started...")
    xbmc.executebuiltin('RunScript(plugin.video.plexbmc,skin)')
    linkCount = 0
    logMsg("updateplexlinks started...")
    
    #update plex window properties
    xbmc.sleep(3000)
    while linkCount !=10:
        plexstring = "plexbmc." + str(linkCount)
        link = win.getProperty(plexstring + ".title")
        logMsg(plexstring + ".title --> " + link)
        plexType = win.getProperty(plexstring + ".type")
        logMsg(plexstring + ".type --> " + plexType)            

        link = win.getProperty(plexstring + ".recent")
        logMsg(plexstring + ".recent --> " + link)
        link = link.replace("ActivateWindow(VideoLibrary, ", "")
        link = link.replace("ActivateWindow(VideoLibrary,", "")
        link = link.replace("ActivateWindow(MusicFiles,", "")
        link = link.replace("ActivateWindow(Pictures,", "")
        link = link.replace(",return)", "")
        win.setProperty(plexstring + ".recent.content", link)
        logMsg(plexstring + ".recent --> " + link)

        link = win.getProperty(plexstring + ".viewed")
        logMsg(plexstring + ".viewed --> " + link)
        link = link.replace("ActivateWindow(VideoLibrary, ", "")
        link = link.replace("ActivateWindow(VideoLibrary,", "")
        link = link.replace("ActivateWindow(MusicFiles,", "")
        link = link.replace("ActivateWindow(Pictures,", "")
        link = link.replace(",return)", "")
        win.setProperty(plexstring + ".viewed.content", link)
        logMsg(plexstring + ".viewed --> " + link)

        linkCount += 1
    
    xbmc.sleep(5000)
    updatePlexBackgrounds()   
        
def updatePlexBackgrounds():
    win = xbmcgui.Window( 10000 )
    logMsg("update plex backgrounds started...")        
    
    #update plex backgrounds
    linkCount = 0
    xbmc.sleep(5000)
    while linkCount !=10:
        plexstring = "plexbmc." + str(linkCount)
        randomNr = random.randrange(1,10+1)       
        plexType = win.getProperty(plexstring + ".type")
        randomimage = ""
        if plexType == "movie":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").Art(fanart)")
            win.setProperty("plexfanartbg", randomimage)
        elif plexType == "artist":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").Art(fanart)")
            if randomimage == "":
                randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(1).Art(fanart)")
            if randomimage == "":
                randomimage = "special://skin/extras/backgrounds/hover_my music.png"                
        elif plexType == "show":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").Property(Fanart_Image)")
        elif plexType == "photo":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").PicturePath")                

        if randomimage != "":
            win.setProperty(plexstring + ".background", randomimage)
            logMsg(plexstring + ".background --> " + randomimage)            

        linkCount += 1
               
def showInfoPanel():
    win = xbmcgui.Window( 10000 )
    tryCount = 0
    secondsToDisplay = "4"
    secondsToDisplay = xbmc.getInfoLabel("Skin.String(ShowInfoAtPlaybackStart)")
    while tryCount !=50 and not xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)"):
        time.sleep(0.1)
        if not xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)") and xbmc.getCondVisibility("Player.HasVideo"):
            xbmc.executebuiltin('Action(info)')
        tryCount += 1
    
    # close info again
    time.sleep(int(secondsToDisplay))
    if xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)"):
        xbmc.executebuiltin('Action(info)')

def addShortcutWorkAround():
    win = xbmcgui.Window( 10000 )
    xbmc.executebuiltin('SendClick(301)')
    if xbmc.getCondVisibility("System.Platform.Windows"):
        time.sleep(1)
    else:
        time.sleep(2)
    xbmc.executebuiltin('SendClick(401)')


def setView(containerType,viewId):

    if viewId=="00":
        win = xbmcgui.Window( 10000 )

        curView = xbmc.getInfoLabel("Container.Viewmode")
        
        # get all views from views-file
        skin_view_file = os.path.join(xbmc.translatePath('special://skin'), "views.xml")
        skin_view_file_alt = os.path.join(xbmc.translatePath('special://skin/extras'), "views.xml")
        if xbmcvfs.exists(skin_view_file_alt):
            skin_view_file = skin_view_file_alt
        try:
            tree = etree.parse(skin_view_file)
        except:           
            sys.exit()
        
        root = tree.getroot()
        
        for view in root.findall('view'):
            if curView == view.attrib['id']:
                viewId=view.attrib['value']
    else:
        viewId=viewId    

    if xbmc.getCondVisibility("System.HasAddon(plugin.video.netflixbmc)"):
        __settings__ = xbmcaddon.Addon(id='plugin.video.netflixbmc')

        if containerType=="MOVIES":
            __settings__.setSetting('viewIdVideos', viewId)
        elif containerType=="SERIES":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        elif containerType=="SEASONS":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        elif containerType=="EPISODES":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        else:
            __settings__.setSetting('viewIdActivity', viewId) 


def showSubmenu(showOrHide,doFocus):

    win = xbmcgui.Window( 10000 )
    submenuTitle = xbmc.getInfoLabel("Container(300).ListItem.Label")
    submenu = win.getProperty("submenutype")
    submenuloading = ""
    if xbmc.getCondVisibility("Skin.HasSetting(AutoShowSubmenu)"):
        submenuloading = win.getProperty("submenuloading")

    # SHOW SUBMENU    
    if showOrHide == "SHOW":
        if submenuloading != "loading":
            if submenu != "":
                win.setProperty("submenu", "show")
                if doFocus != None:
                    win.setProperty("submenuTitle", submenuTitle)
                    xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
                    time.sleep(0.2)
                    xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            else:
                win.setProperty("submenu", "hide")
        else:
            win.setProperty("submenuloading", "")

    #HIDE SUBMENU
    elif showOrHide == "HIDE":
        win.setProperty("submenuloading", "loading")
        win.setProperty("submenu", "hide")
        if doFocus != None:
            win.setProperty("submenu", "show")
            xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            time.sleep(0.5)
            xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            win.setProperty("submenuloading", "loading")
            win.setProperty("submenu", "hide")
            
