# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

from util import fix_chars

BASE_URL_WEBTV = 'http://www1.nrk.no/nett-tv'
CACHE_HTML_INTERVAL = 3600 * 5
RSS_MEDIA_NAMESPACE = {'media': 'http://search.yahoo.com/mrss/'}


def WebTVMenu(sender):
    """
    Show the web TV main menu.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Most viewed
    dir.Append(Function(DirectoryItem(WebTVMostViewedWeekMenu, title=L('most_viewed_week'), summary=L('most_viewed_week_description'), thumb=R('nrk-nett-tv.png'))))

    dir.Append(Function(DirectoryItem(WebTVMostViewedMonthMenu, title=L('most_viewed_month'), summary=L('most_viewed_month_description'), thumb=R('nrk-nett-tv.png'))))
    
    dir.Append(Function(DirectoryItem(WebTVMostViewedTotalMenu, title=L('most_viewed_total'), summary=L('most_viewed_total_description'), thumb=R('nrk-nett-tv.png'))))
    
    
    # By letter
    dir.Append(Function(InputDirectoryItem(WebTVByLetterMenu, title=L('by_letter'), prompt=L('by_letter_prompt'), summary=L('by_letter_description'), thumb=R('nrk-nett-tv.png'))))
    
    # Genre
    dir.Append(Function(DirectoryItem(WebTVGenreMainMenu, title=L('genres'), summary=L('genres_description'), thumb=R('nrk-nett-tv.png'))))
    
    
    # TODO: Recomended, Search
    
    return dir


##################################
# Generic program and clip menus #
##################################

def WebTVProgramMenu(sender, projectId=None, categoryId=None, programImage=None):
    """
    Shows the elements of a program project or category.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Fetch most viewed HTML (from NRK's Ajax response)
    if projectId:
        url = '%s/dynamisklaster.aspx?projectList$project:%s' % (BASE_URL_WEBTV, projectId)
        page = XML.ElementFromURL(url, isHTML=True, cacheTime=CACHE_HTML_INTERVAL, encoding='utf-8')
        elements = page.xpath('//div[@class="nettv-list"]/ul')[0]
        
    elif categoryId:
        url = '%s/menyfragment.aspx?type=category&id=%s' % (BASE_URL_WEBTV, categoryId)
        Log('Fetching %s' % url)
        elements = XML.ElementFromURL(url, isHTML=True, cacheTime=CACHE_HTML_INTERVAL) # , encoding='utf-8'
    
    # Display error message if there's no content
    if not elements:
        return (MessageContainer(header=L('title'), message=L('webtv_error_nocontent'), title1=L('title')))
    
    for element in elements:
        
        try:
            elem_a = element.xpath('./a')[0]
        except IndexError:
            elem_a = element
            if not elem_a.get('href'):
                break
        
        # Link is a clip
        if elem_a.get('href').find('klipp') != -1:
            
            # Title
            raw_title = fix_chars(elem_a.get('title'))
            Log('Raw title: %s' % raw_title)
            
            # Split title and add as a description
            title = raw_title
            desc = None
            
            if raw_title.find(' - ') != -1:
                split_title = raw_title.split(' - ')
                title = split_title[0]
                desc = ' - '.join(split_title[1:])
            
            # Link and MMS URL
            html_link = elem_a.get('href')
            clip_mms_url = _get_wmv_link(html_link)
            
            # TODO Does not support URLs with unicode characters
            try:
                dir.Append(WindowsMediaVideoItem(clip_mms_url, title=title, summary=desc, thumb=programImage, width=768, height=432))
            except:
                Log('Could not add %s to menu, illegal characters in URL' % title)
        
        
        # Link is a category
        elif elem_a.get('href').find('kategori') != -1:
            
            # Title
            raw_title = fix_chars(elem_a.get('title'))
            Log('Raw category title: %s' % raw_title)
            
            # Split title and add as a description
            title = raw_title
            desc = None
            
            if raw_title.find(' - ') != -1:
                split_title = raw_title.split(' - ')
                title = split_title[0]
                desc = ' - '.join(split_title[1:])
            
            title = '[%s]' % title
            category_id = elem_a.get('href').split('/')[-1]
            
            Log('Added category: %s' % title)
            
            dir.Append(Function(DirectoryItem(WebTVProgramMenu, title=title, summary=desc, thumb=programImage), categoryId=category_id, programImage=programImage))
    
    return dir


###############
# Most viewed #
###############

def WebTVMostViewedWeekMenu(sender):
    return WebTVMostViewedMenu(sender, days=7)

def WebTVMostViewedMonthMenu(sender):
    return WebTVMostViewedMenu(sender, days=31)

def WebTVMostViewedTotalMenu(sender):
    return WebTVMostViewedMenu(sender, days=3650)


def WebTVMostViewedMenu(sender, days=7):
    """
    Show a most viewed web tv menu.
    
    Source: http://pipes.yahoo.com/jonklo/nrkmostviewed
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Fetch most viewed clips (from a custom Yahoo Pipe)
    url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=aefa462421686c218bfa1f48df4b41b5&_render=rss&days=%s' % days
    Log('Fetching %s' % url)
    
    rss = XML.ElementFromURL(url, isHTML=False, cacheTime=CACHE_HTML_INTERVAL, encoding='utf-8')
    program_elements = rss.xpath('//channel/item')
    
    # Display error message if there's no content
    if not program_elements:
        return (MessageContainer(header=L('title'), message=L('webtv_error_nocontent'), title1=L('title')))
    
    for program_element in program_elements:
        
        # Program title and description
        title = program_element.xpath('./title/text()')[0]
        desc = program_element.xpath('./description/text()')[0]
        
        # Program image and clip URL
        img = program_element.xpath('./media:thumbnail', namespaces=RSS_MEDIA_NAMESPACE)[0].get('url')
        clip_url = program_element.xpath('./media:content', namespaces=RSS_MEDIA_NAMESPACE)[0].get('url')
        
        # Append the item to the list
        dir.Append(WindowsMediaVideoItem(clip_url, title=title, summary=desc, thumb=img, width=768, height=432))
    
    return dir

##########
# Genres #
##########

WEB_TV_GENRES = (
    # Title, ID
    (u'Barn', '2'),
    (u'Distrikt', '13'),
    (u'Dokumentar', '20'),
    (u'Drama', '3'),
    (u'Fakta', '4'),
    (u'Kultur', '5'),
    (u'Livssyn', '9'),
    (u'Mat', '17'),
    (u'Musikk', '6'),
    (u'Natur', '7'),
    (u'Nyheter', '8'),
    (u'På samisk', '19'),
    (u'På tegnspråk', '22'),
    (u'Sport', '10'),
    (u'Underholdning', '11'),
    (u'Ung', '21'),
)

def WebTVGenreMainMenu(sender):
    """
    Shows the genre overview menu.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    for genre in WEB_TV_GENRES:
        Log(genre[0])
        dir.Append(Function(DirectoryItem(WebTVContentMenu, title=genre[0]), genre_id=genre[1]))
    
    return dir
    

def WebTVContentMenu(sender, genre_id=None, letter=None):
    """
    Show the given genre's programs.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Fetch most viewed HTML (from NRK's Ajax response)
    if genre_id:
        url = '%s/DynamiskLaster.aspx?LiveContent$theme:%s' % (BASE_URL_WEBTV, genre_id)
    elif letter:
        url = '%s/DynamiskLaster.aspx?LiveContent$letter:%s' % (BASE_URL_WEBTV, letter)
    
    page = XML.ElementFromURL(url, isHTML=True, cacheTime=CACHE_HTML_INTERVAL, encoding='utf-8')
    elements = page.xpath('//ul/li/div')
    
    # Display error message if there's no content
    if not elements:
        return (MessageContainer(header=L('title'), message=L('webtv_error_nocontent'), title1=L('title')))
    
    for element in elements:
        
        # Title
        title = fix_chars(element.xpath('./a')[0].get('title'))
        project_id = element.xpath('./a')[0].get('href').split('/')[-1]
        Log(title + ' ' + project_id)
        
        # Split title and add as a description
        if title.find(' - ') != -1:
            title, desc = title.split(' - ')[:2]
        
        # Image
        img = element.xpath('./a/img')[0].get('src')
        
        # Description
        try:
            desc = fix_chars(element.xpath('./div/p/a')[0].text)
        except AttributeError:
            desc = None
        
        
        dir.Append(Function(DirectoryItem(WebTVProgramMenu, title=title, summary=desc, thumb=img), projectId=project_id, programImage=img))
    
    return dir


#############
# By letter #
#############

def WebTVByLetterMenu(sender, query):
    
    # If the string is longer than one character, just pass along the first one
    if len(query) > 1:
        query = query[0]
    
    return WebTVContentMenu(sender, letter=query)


###########
# Helpers #
###########

def _get_wmv_link(clip_url):
    """
    Fetches the Windows Meda Video link.
    """
    clip_id = clip_url.split('/')[-1]
    
    url = '%s/silverlight/getmediaxml.ashx?id=%s&hastighet=2000&vissuper=True' % (BASE_URL_WEBTV, clip_id)
    
    page = XML.ElementFromURL(url, isHTML=True, cacheTime=CACHE_HTML_INTERVAL)
    
    if not page:
        Log('Error fetching URL from %s' % url)
        return None
    
    # Find the video URL
    mms_link = page.xpath('//mediadefinition/mediaitems/mediaitem/mediaurl')[0].text
    
    Log('%s -> %s' % (clip_url, mms_link))
    return mms_link

