#-*- coding: UTF-8 -*-
'''
Created on 25.8.2014

@author: psmorada
'''
import urllib2;
import re;
from utilities import *;

__title__ = 'hudba.sk'
__priority__ = '240'
__lrc__ = False

class LyricsFetcher:
    
    def __init__( self ):
        self.base_url = "http://hudba.zoznam.sk"
        self.searchUrl = "http://hudba.zoznam.sk/katalog/hladaj/?s=lyrics&q=%term%"
        
    def search(self, artist, title):
        term = urllib2.quote((artist if artist else "") + " " + (title if title else ""));
        
        try:
            request = urllib2.urlopen(self.searchUrl.replace("%term%", term))
            searchResponse = request.read();
            #print(searchResponse);
        except:
            return None
        
        # Search performed in 2 steps for performance reasons
        songPartMatch =  re.search("results-tab-songs.*?class=\"results\">(.*?)<span", searchResponse, re.DOTALL | re.MULTILINE);
        
        if not songPartMatch:
            return None;                

        searchResult = re.findall("<div\sclass=\"result\">.*?<a\shref=\"(.*?)\">(.*?)</a>", songPartMatch.group(1), re.MULTILINE | re.DOTALL);
        
        if len(searchResult) == 0:
            print("None");
            return None;
        
        links = [];
        
                
        i = 0;
        for result in searchResult:
            a = [];
            a.append(result[1]); # name from the server
            #print(result[1]);
            a.append(self.base_url + result[0]);  # url with lyrics
            a.append(artist);
            a.append(title);
            links.append(a);
            i += 1;
        print(links);
        print(str(len(links)));    
        return links;
    
    def findLyrics(self, url):
        print(url);
        try:
            request = urllib2.urlopen(url);
            res = request.read();
        except:
            print("None");
            return None
        
        match = re.search("<span\sitemprop=\"(?:transcript|description)\">(.*)", res);
        if match:  
            s = match.group(1);
            s = s.strip();
            #s = s.replace("<br />", "");
            s = s.replace("<i>", "");
            s = s.replace("</i>", "");
            
            # lyrics returned are not always standart - once contain new lines other time not... 
            lines = s.split("<br />");
            lyr = ""
            for line in lines:
                lyr += line.strip() + "\n"; 
            print(lyr);
            return lyr;
        else:
            print("not Found")
            return None;


    def get_lyrics(self, song):
        #log( "%s: searching lyrics for %s - %s" % (__title__, song.artist, song.title))
        lyrics = Lyrics();
        lyrics.song = song;
        lyrics.source = __title__;
        lyrics.lrc = __lrc__;
        
        links = self.search(song.artist , song.title);
        
        if(links == None or len(links) == 0):
            return None;
        elif len(links) > 1:
            lyrics.list = links
        
        lyr = self.get_lyrics_from_list(links[0])
        if not lyr:
            return None
        lyrics.lyrics = lyr
        return lyrics;

    def get_lyrics_from_list(self, link):
        title, url, artist, song = link;
        return self.findLyrics(url);        
#l = LyricsFetcher().search("Bila", "laska je laska"); 
#l = LyricsFetcher().search("elan", "bosorka"); 
#l = LyricsFetcher().search("desmod", "hemeroidy"); 
#l = LyricsFetcher().search("tublatanka", "lod");
#l = LyricsFetcher().search("metalinda", "jan amos");
#l = LyricsFetcher().search("kabat", "colorado");
#l = LyricsFetcher().search("tri setri", "setri se chlapce");
#l = LyricsFetcher().search("orlik", "pivecko");
#l = LyricsFetcher().search("lánda", "pozdrav");

  
#LyricsFetcher().findLyrics(l[0][1]);
        
        