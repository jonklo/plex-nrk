# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *


LIVE_RADIO_BASEURL = 'http://media.hiof.no/scripts/make_session.php'
#LIVE_RADIO_QUALITY = 'h' # h (high) or m (medium)

LIVE_RADIO_STATIONS = (
    # Channel/image filename, name, description
    ('nrk-p1', u'P1', u'Den brede kanalen for folk flest. Norges største radiokanal. Bredt distriktstilbud.'),
    ('nrk-p2', u'P2', u'Kulturkanalen med kunst, kultur, nyheter, debatt og samfunnsstoff.'),
    ('nrk-petre', u'P3', u'Ungdomskanal med mye pop og rock-musikk, humor og skreddersydde nyheter for de unge.'),
    ('nrk-mpetre', u'mPetre', u'Musikk for de yngre.'),
    ('nrk-alltid-klassisk', u'Klassisk', u'Klassisk musikk døgnet rundt'),
    ('nrk-alltid-nyheter', u'Alltid Nyheter', u'Hyppige nyhetsoppdateringer - BBC kveld/natt.'),
    ('nrk-sami-radio', u'Sámi Radio', u'Tilbud for samisktalende.'),
    ('nrk-stortinget', u'Stortinget', u'Fra debattene.'),
    ('nrk-alltid-folkemusikk', u'Folkemusikk', u'Fra NRKs unike folkemusikkarkiv.'),
    ('nrk-jazz', u'Jazz', u'Jazz døgnet rundt.'),
    ('nrk-sport', u'Sport', u'Levende og arkivsport, engelsk fotball.'),
    ('nrk-urort', u'Urørt', u'Musikk.'),
    ('nrk-gull', u'Gull', u'Godbiter fra arkivene.'),
    ('nrk-super', u'Super', u'Barnetilbud.'),
    ('nrk-p1-ostfold', u'P1 Østfold', u''),
    ('nrk-p1-buskerud', u'P1 Buskerud', u''),
    ('nrk-p1-sogn-og-fjordane', u'P1 Sogn og Fjordane', u''),
    ('nrk-p1-rogaland', u'P1 Rogaland', u''),
    ('nrk-p1-finnmark', u'P1 Finnmark', u''),
    ('nrk-p1-hedmark', u'P1 Hedmark', u''),
    ('nrk-p1-hordaland', u'P1 Hordaland', u''),
    ('nrk-p1-more-og-romsdal', u'P1 Møre og Romsdal', u''),
    ('nrk-p1-nordland', u'P1 Nordland', u''),
    ('nrk-p1-oppland', u'P1 Oppland', u''),
    ('nrk-p1-oslo', u'P1 Oslo', u''),
    ('nrk-p1-telemark', u'P1 Telemark', u''),
    ('nrk-p1-troms', u'P1 Troms', u''),
    ('nrk-p1-trondelag', u'P1 Trøndelag', u''),
    ('nrk-p1-vestfold', u'P1 Vestfold', u''),
    ('nrk-p1-sorlandet', u'P1 Sørlandet', u''),
)


def LiveRadioMenu(sender):
    """
    Show the live radio menu.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Adds all the station as track items
    for station in LIVE_RADIO_STATIONS:
        url = '%s?channel=%s&quality=%s&format=ogg&protocol=ipv4' % \
            (LIVE_RADIO_BASEURL, station[0], Prefs.Get("radio_quality"))
            
        Log('Added stream: %s' % url)
        
        # Thumb file
        if station[0].startswith('nrk-p1'):
            thumb_file = 'nrk-p1.png'
        else:
            thumb_file = station[0] + '.png'
        
        dir.Append(TrackItem(url, station[1], summary=station[2], thumb=R('nrk-nettradio.png'))) # TODO R(thumb_file)
    
    return dir
