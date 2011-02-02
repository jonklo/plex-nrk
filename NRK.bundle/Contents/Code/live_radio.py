# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *


LIVE_RADIO_BASEURL = 'http://lyd.nrk.no/nrk_radio_'
LIVE_RADIO_QUALITY = 'h' # h (high) or m (medium)

LIVE_RADIO_STATIONS = (
    # Channel/image filename, name, description
    ('p1_ostlandssendingen', u'P1', u'Den brede kanalen for folk flest. Norges største radiokanal. Bredt distriktstilbud.'),
    ('p2', u'P2', u'Kulturkanalen med kunst, kultur, nyheter, debatt og samfunnsstoff.'),
    ('p3', u'P3', u'Ungdomskanal med mye pop og rock-musikk, humor og skreddersydde nyheter for de unge.'),
    ('mp3', u'mPetre', u'Musikk for de yngre.'),
    ('klassisk', u'Klassisk', u'Klassisk musikk døgnet rundt'),
    ('alltid_nyheter', u'Alltid Nyheter', u'Hyppige nyhetsoppdateringer - BBC kveld/natt.'),
    ('sami', u'Sámi Radio', u'Tilbud for samisktalende.'),
    ('folkemusikk', u'Folkemusikk', u'Fra NRKs unike folkemusikkarkiv.'),
    ('jazz', u'Jazz', u'Jazz døgnet rundt.'),
    ('sport', u'Sport', u'Levende og arkivsport, engelsk fotball.'),
    ('p3_urort', u'Urørt', u'Musikk.'),
    ('gull', u'Gull', u'Godbiter fra arkivene.'),
    ('super', u'Super', u'Barnetilbud.'),
    ('p1_ostfold', u'P1 Østfold', u''),
    ('p1_buskerud', u'P1 Buskerud', u''),
    ('p1_sogn_og_fjordane', u'P1 Sogn og Fjordane', u''),
    ('p1_rogaland', u'P1 Rogaland', u''),
    ('p1_finnmark', u'P1 Finnmark', u''),
    ('p1_hedmark_og_oppland', u'P1 Hedmark og Oppland', u''),
    ('p1_hordaland', u'P1 Hordaland', u''),
    ('p1_more_og_romsdal', u'P1 Møre og Romsdal', u''),
    ('p1_nordland', u'P1 Nordland', u''),
    ('p1_sorlandet', u'P1 Sørlandet', u''),
    ('p1_telemark', u'P1 Telemark', u''),
    ('p1_troms', u'P1 Troms', u''),
    ('p1_trondelag', u'P1 Trøndelag', u''),
    ('p1_vestfold', u'P1 Vestfold', u''),
    ('p1_sorlandet', u'P1 Sørlandet', u'')
)


def LiveRadioMenu(sender):
    """
    Show the live radio menu.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Adds all the station as track items
    for station in LIVE_RADIO_STATIONS:
        url = '%s%s_mp3_%s' % \
            (LIVE_RADIO_BASEURL, station[0], Prefs.Get("radio_quality"))
            
        Log('Added stream: %s' % url)
        
        # Thumb file
        if station[0].startswith('nrk-p1'):
            thumb_file = 'nrk-p1.png'
        else:
            thumb_file = station[0] + '.png'
        
        dir.Append(TrackItem(url, station[1], summary=station[2], thumb=R('nrk-nettradio.png'))) # TODO R(thumb_file)
    
    return dir
