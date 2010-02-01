# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *


LIVE_RADIO_BASEURL = 'http://media.hiof.no/scripts/make_session.php'
LIVE_RADIO_QUALITY = 'h' # h (high) or m (medium)

LIVE_RADIO_STATIONS = (
    # Channel/image filename, name, description
    ('nrk-p1', 'P1', u'Den brede kanalen for folk flest. Norges største radiokanal. Bredt distriktstilbud.'),
    ('nrk-p2', 'P2', u'Kulturkanalen med kunst, kultur, nyheter, debatt og samfunnsstoff.'),
    ('nrk-petre', 'P3', u'Ungdomskanal med mye pop og rock-musikk, humor og skreddersydde nyheter for de unge.'),
    ('nrk-mpetre', 'mPetre', u'Musikk for de yngre.'),
    ('nrk-alltid-klassisk', 'Klassisk', u'Klassisk musikk døgnet rundt'),
    ('nrk-alltid-nyheter', 'Alltid Nyheter', u'Hyppige nyhetsoppdateringer - BBC kveld/natt.'),
    ('nrk-sami-radio', u'Sámi Radio', u'Tilbud for samisktalende.'),
    ('nrk-stortinget', 'Stortinget', u'Fra debattene.'),
    ('nrk-alltid-folkemusikk', 'Folkemusikk', u'Fra NRKs unike folkemusikkarkiv.'),
    ('nrk-jazz', 'Jazz', u'Jazz døgnet rundt.'),
    ('nrk-sport', 'Sport', u'Levende og arkivsport, engelsk fotball.'),
    ('nrk-urort', u'Urørt', u'Musikk.'),
    ('nrk-gull', 'Gull', u'Godbiter fra arkivene.'),
    ('nrk-super', 'Super', u'Barnetilbud.'),
    ('nrk-p1-ostfold', u'P1 Østfold', ''),
    ('nrk-p1-buskerud', 'P1 Buskerud', ''),
    ('nrk-p1-sogn-og-fjordane', 'P1 Sogn og Fjordane', ''),
    ('nrk-p1-rogaland', 'P1 Rogaland', ''),
    ('nrk-p1-finnmark', 'P1 Finnmark', ''),
    ('nrk-p1-hedmark', 'P1 Hedmark', ''),
    ('nrk-p1-hordaland', 'P1 Hordaland', ''),
    ('nrk-p1-more-og-romsdal', u'P1 Møre og Romsdal', ''),
    ('nrk-p1-nordland', 'P1 Nordland', ''),
    ('nrk-p1-oppland', 'P1 Oppland', ''),
    ('nrk-p1-oslo', 'P1 Oslo', ''),
    ('nrk-p1-telemark', 'P1 Telemark', ''),
    ('nrk-p1-troms', 'P1 Troms', ''),
    ('nrk-p1-trondelag', u'P1 Trøndelag', ''),
    ('nrk-p1-vestfold', 'P1 Vestfold', ''),
    ('nrk-p1-sorlandet', u'P1 Sørlandet', ''),
)


def LiveRadioMenu(sender):
    """
    Show the live radio menu.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Adds all the station as track items
    for station in LIVE_RADIO_STATIONS:
        url = '%s?channel=%s&quality=%s&format=ogg&protocol=ipv4' % \
            (LIVE_RADIO_BASEURL, station[0], LIVE_RADIO_QUALITY)
        
        if station[0].startswith('nrk-p1'):
            res_art = R('nrk-p1.png')
        else:
            res_art = R(station[0] + '.png')
        
        dir.Append(TrackItem(url, station[1], summary=station[2], thumb=res_art))
    
    return dir
