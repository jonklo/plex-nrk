# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

# Moved to preferences
#LIVE_TV_QUALITY = 'l' # h (1000kb), m (600kb) or l (300kb)

LIVE_TV_STATIONS = (
    {
        'title': 'NRK 1', 
        'url': 'mms://straumV.nrk.no/nrk_tv_webvid03_%s',
        #'url': 'mms://mms-icanal-live.online.no/nrk_tv_direkte_nrk1_%s',
        
        'desc': u'Bredt og variert programtilbud. Norges største tv-kanal.', 
        'img': 'nrk1.png',
    },
    {
        'title': 'NRK 2', 
        'url': 'mms://straumV.nrk.no/nrk_tv_webvid04_%s',
        #'url': 'mms://mms-icanal-live.online.no/nrk_tv_direkte_nrk2_%s',
        'desc': u'Fordypningskanalen. Bakgrunns-, dokumentar og nyhetskanal.', 
        'img': 'nrk2.png',
    }, 
    {
        'title': 'NRK Super / NRK 3', 
        'url': 'mms://straumV.nrk.no/nrk_tv_webvid05_%s',
        #'url': 'mms://mms-icanal-live.online.no/nrk_tv_direkte_nrk3_%s',
        'desc': u'Den tredje kanalen tilbyr vekselsvis et barnetilbud og et tilbud for unge voksne med serier, humor film.', 
        'img': 'nrk3.png',
    },
    {
        'title': 'NRK Storting', 
        'url': 'mms://mms-icanal-live.online.no/nrk_tv_webvid05_%s',
        'desc': u'Fra debattene.', 
        'img': 'nrk-stortinget.png',
    },
    
)




def LiveTVMenu(sender):
    """
    Show the live TV menu.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    for station in LIVE_TV_STATIONS:
        url = station['url'] % Prefs.Get('livetv_quality')
        Log('Added %s' % url)
        
        dir.Append(WindowsMediaVideoItem(url, title=station['title'], summary=station['desc'], thumb=R(station['img'])))
    
    return dir
