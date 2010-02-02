# -*- coding: utf-8 -*-
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

from util import fix_chars

BASE_URL_WEBTV = 'http://www1.nrk.no/nett-tv'
CACHE_HTML_INTERVAL = 3600 * 5


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
        page = XML.ElementFromURL(url, isHTML=True, cacheTime=CACHE_HTML_INTERVAL, encoding='utf-8')
        elements = page
    
    for element in elements:
        
        elem_a = element.xpath('./a')[0]
        
        # Link is a clip
        if elem_a.get('href').find('klipp') != -1:
            
            # Title
            title = fix_chars(elem_a.get('title'))
            
            # Split title and add as a description
            desc = None
            if title.find(' - ') != -1:
                title, desc = title.split(' - ')[:2]
                
        
            # Link and MMS URL
            html_link = elem_a.get('href')
            clip_mms_url = _get_wmv_link(html_link)
            
            # TODO Does not support URL's with unicode characters
            try:
                dir.Append(WindowsMediaVideoItem(clip_mms_url, title=title, summary=desc, thumb=programImage, width=768, height=432))
            except:
                Log('Could not add %s to menu, illegal characters in URL' % title)
        
        
        # Link is a category
        elif elem_a.get('href').find('kategori') != -1:
            # Title
            title = fix_chars(elem_a.get('title'))
            
            # Split title and add as a description
            desc = None
            if title.find(' - ') != -1:
                title, desc = title.split(' - ')[:2]
            
            title = '[%s]' % title
            Log(title)
            
            category_id = elem_a.get('href').split('/')[-1]
            
            # TODO Does not support URL's with unicode characters
            try:
                dir.Append(Function(DirectoryItem(WebTVProgramMenu, title=title, summary=desc, thumb=programImage), categoryId=category_id, programImage=programImage))
            except:
                Log('Could not add %s to menu, illegal characters in URL' % title)
            
        
    
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
    Show the live radio menu.
    """
    dir = MediaContainer(viewGroup='Details', title2=sender.itemTitle)
    
    # Fetch most viewed HTML (from NRK's Ajax response)
    url = '%s/ml/topp12.aspx?dager=%s' % (BASE_URL_WEBTV, days)
    
    page = XML.ElementFromURL(url, isHTML=True, cacheTime=CACHE_HTML_INTERVAL, encoding='utf-8')
    program_elements = page.xpath('//div[@class="views-element"]')
    
    for program_element in program_elements:
        
        # Program image
        img = program_element.xpath('./div/a/img')[0].get('src')
        
        # Program title
        title = fix_chars(program_element.xpath('./h2/a')[0].text)
        
        # HTML link and fetch MMS link
        html_link = program_element.xpath('./p/a')[0].get('href')
        
        # Program description
        desc = fix_chars(program_element.xpath('./p/a')[0].text)
        
        # Append the item to the list
        dir.Append(WindowsMediaVideoItem(_get_wmv_link(html_link), title=title, summary=desc, thumb=img, width=768, height=432))
    
    return dir

##########
# Genres #
##########

WEB_TV_GENRES = (
    # Title, ID
    ('Barn', '2'),
    ('Distrikt', '13'),
    ('Dokumentar', '20'),
    ('Drama', '3'),
    ('Fakta', '4'),
    ('Kultur', '5'),
    ('Livssyn', '9'),
    ('Mat', '17'),
    ('Musikk', '6'),
    ('Natur', '7'),
    ('Nyheter', '8'),
    (u'På samisk', '19'),
    (u'På tegnspråk', '22'),
    ('Sport', '10'),
    ('Underholdning', '11'),
    ('Ung', '21'),
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
    elements = page.xpath('//div[@class="intro-element intro-element-small"]')
    
    for element in elements:
        
        # Title
        title = fix_chars(element.xpath('./div/a')[0].get('title'))
        project_id = element.xpath('./div/a')[0].get('href').split('/')[-1]
        Log(title + ' ' + project_id)
        
        # Split title and add as a description
        if title.find(' - ') != -1:
            title, desc = title.split(' - ')[:2]
        
        # Image
        img = element.xpath('./div/a/img')[0].get('src')
        
        # Description
        try:
            desc = fix_chars(element.xpath('./p/a')[0].text)
        except AttributeError:
            desc = None
        
        
        dir.Append(Function(DirectoryItem(WebTVProgramMenu, title=title, summary=desc, thumb=img), projectId=project_id, programImage=img))
    
    return dir


#############
# By letter #
#############

def WebTVByLetterMenu(sender, query):
    if len(query) != 1:
        return (MessageContainer(header=sender.itemTitle, message=L('by_letter_length'), title1=L('title')))
    
    return WebTVContentMenu(sender, letter=query)


###########
# Helpers #
###########

def _get_wmv_link(clip_url):
    """
    Fetches the Windows Meda Video link from nonline.org. Thanks dude!
    
    Source:
    http://nonline.org/nrk/beta/
    """
    url = 'http://nonline.org/nrk/beta/%s' % clip_url
    page = XML.ElementFromURL(url, isHTML=True, cacheTime=CACHE_HTML_INTERVAL)
    
    elem_a = page.xpath('//p/a')
    mms_link = None
    
    if len(elem_a) > 0:
        mms_link = elem_a[0].get('href')
        
    Log('%s -> %s' % (clip_url, mms_link))
    return mms_link
    
