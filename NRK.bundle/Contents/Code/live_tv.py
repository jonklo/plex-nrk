# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *


LIVE_TV_STATIONS = (
    {
        'title': 'NRK 1', 
        'url': 'mms://straumv.nrk.no/nrk_tv_direkte_nrk1_%s',
        'desc': u'Bredt og variert programtilbud. Norges største tv-kanal.', 
        'img': 'nrk1.png',
    },
    {
        'title': 'NRK 2', 
        'url': 'mms://straumv.nrk.no/nrk_tv_direkte_nrk2_%s',
        'desc': u'Fordypningskanalen. Bakgrunns-, dokumentar og nyhetskanal.', 
        'img': 'nrk2.png',
    }, 
    {
        'title': 'NRK Super / NRK 3', 
        'url': 'mms://straumv.nrk.no/nrk_tv_direkte_nrk3_%s',
        'desc': u'Den tredje kanalen tilbyr vekselsvis et barnetilbud og et tilbud for unge voksne med serier, humor film.', 
        'img': 'nrk3.png',
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
        
        dir.Append(WindowsMediaVideoItem(url, title=station['title'], summary=station['desc'], thumb=R('nrk-nett-tv.png'), width=768, height=432)) # TODO thumb=R(station['img'])
    
    return dir
