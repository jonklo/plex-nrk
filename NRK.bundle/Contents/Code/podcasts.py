# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

CACHE_HTML_INTERVAL = 3600 * 5
CACHE_RSS_FEED_INTERVAL = 3600

PODCAST_URL = 'http://www.nrk.no/podkast/'
PODCAST_ITUNES_NAMESPACE = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}


def PodcastAudioMenu(sender):
    return PodcastMenu(sender, kind='audio')

def PodcastVideoMenu(sender):
    return PodcastMenu(sender, kind='video')


def PodcastMenu(sender, kind):
    """
    Show all available feeds, either video or audio.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    page = XML.ElementFromURL(PODCAST_URL, isHTML=True, cacheTime=CACHE_HTML_INTERVAL)
    
    podcast_tables = page.xpath('//div[@class="pod"]/table')
    
    if kind == 'video':
        podcast_table = podcast_tables[0]
    
    else:
        podcast_table = podcast_tables[1]
    
    for tbody in podcast_table:
        tr_title = tbody.xpath('./tr[@class="pod-row"]')
        tr_desc = tbody.xpath('./tr[@class="pod-desc"]')
        tr_rss_url = tbody.xpath('./tr[@class="pod-rss-url"]')
        
        if len(tr_title):
            title = tr_title[0].xpath('./th')[0].text
        
        if len(tr_desc):
            description = tr_desc[0].xpath('./td/p')[0].text
        
        if len(tr_rss_url):
            rss_url = tr_rss_url[0].xpath('./td/a')[0].get('href')
            
            # Fetch the image from the RSS file
            feed = XML.ElementFromURL(rss_url, isHTML=False, cacheTime=CACHE_RSS_FEED_INTERVAL)
            
            try:
                image = feed.xpath('//itunes:image', namespaces=PODCAST_ITUNES_NAMESPACE)[0].get('href')
            except AttributeError:
                image = None
            
            # Add it to the list
            dir.Append(Function(DirectoryItem(PodcastShowMenu, title=title, summary=description, thumb=image), podcastName=title, podcastUrl=rss_url, podcastSubtitle=description, podcastImage=image))
        

    return dir

def PodcastShowMenu(sender, podcastName=None, podcastUrl=None, podcastSubtitle=None, podcastImage=None):
    """
    Show all available items for a given podcast.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    dir.title2 = podcastName
    
    rss = XML.ElementFromURL(podcastUrl, isHTML=False, cacheTime=CACHE_RSS_FEED_INTERVAL)
    
    episodes = rss.xpath('//channel/item')
    
    if len(episodes):
        
        for episode in episodes:
            episodeUrl = episode.xpath('./enclosure')[0].get('url')
            episodeTitle = episode.xpath('./title/text()')[0]
            episodeDate = str(episode.xpath('./pubDate/text()')[0])
            episodeDescription = episode.xpath('./description/text()')[0]
            episodeSubtitle = episodeDate

            episodeLength = 0
            
            dir.Append(TrackItem(episodeUrl, episodeTitle, album=L('title'), summary=episodeDescription, subtitle=episodeSubtitle, duration=episodeLength, thumb=podcastImage))
    
    else:
        # Display error message
        return (MessageContainer(header=L('title'), message=L('podcast_noepisodes'), title1=L('title')))
    
    return dir
