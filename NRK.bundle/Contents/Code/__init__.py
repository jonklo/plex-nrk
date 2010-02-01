# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

from live_radio import LiveRadioMenu
from live_tv import LiveTVMenu
from podcasts import *
from web_tv import *

NRK_PREFIX = '/video/nrk'

NAME = L('Title')
ART = 'art-default.png'
ICON = 'icon-default.png'


def Start():
    """
    Initiates the plugin.
    """
    Plugin.AddPrefixHandler(NRK_PREFIX, MainMenu, L('title'), ICON, ART)
    
    Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
    
    MediaContainer.content = 'Items'
    
    # Set defaults
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)



def MainMenu():
    """
    Sets up the main menu. All the menu functions are in separate files.
    """
    dir = MediaContainer(viewGroup="Details")
    Log(Locale.Geolocation())
    Locale.SetDefaultLocale(loc =Locale.Geolocation().lower())
    dir.Append(Function(DirectoryItem(
                            WebTVMenu, 
                            title=L('webtv_title'), 
                            summary=L('webtv_description'), 
                            thumb=R('nrk-nett-tv.png'))))
    
    dir.Append(Function(DirectoryItem(
                            LiveTVMenu, 
                            title=L('livetv_title'), 
                            summary=L('livetv_description'), 
                            thumb=R('nrk-nett-tv.png'))))
    
    dir.Append(Function(DirectoryItem(
                            LiveRadioMenu, 
                            title=L('liveradio_title'), 
                            summary=L('liveradio_description'), 
                            thumb=R('liveradio.png'))))
    
    dir.Append(Function(DirectoryItem(
                            PodcastVideoMenu, 
                            title=L('podcast_video_title'), 
                            summary=L('podcast_video_description'), 
                            thumb=R('nrk-no.png'))))
    
    dir.Append(Function(DirectoryItem(
                            PodcastAudioMenu, 
                            title=L('podcast_audio_title'), 
                            summary=L('podcast_audio_description'), 
                            thumb=R('nrk-no.png'))))
    
    return dir

"""
# see:
#  http://dev.plexapp.com/docs/Functions.html#CreatePrefs
#  http://dev.plexapp.com/docs/mod_Prefs.html#Prefs.Add
def CreatePrefs():
    Prefs.Add(id='username', type='text', default='', label='Your Username')
    Prefs.Add(id='password', type='text', default='', label='Your Password', option='hidden')

# see:
#  http://dev.plexapp.com/docs/Functions.html#ValidatePrefs
def ValidatePrefs():
    u = Prefs.Get('username')
    p = Prefs.Get('password')
    ## do some checks and return a
    ## message container
    if( u and p ):
        return MessageContainer(
            "Success",
            "User and password provided ok"
        )
    else:
        return MessageContainer(
            "Error",
            "You need to provide both a user and password"
        )
"""
