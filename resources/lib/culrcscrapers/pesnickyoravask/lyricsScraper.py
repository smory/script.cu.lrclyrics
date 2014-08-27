#-*- coding: UTF-8 -*-
'''
Created on 25.8.2014

scraper for http://www.karaoketexty.cz, http://www.karaoketexty.sk, http://www.karaoketexty.net or http://www.karaoketeksty.pl
The search is not the best when not whole name of artist and song are provided or when diacritics are missing...
@author: psmorada
'''
import urllib2;
import re;

__title__ = 'karaoketexty'
__priority__ = '290'
__lrc__ = False

class Lyrics:
    def __init__( self ):
        self.song = Song()
        self.lyrics = ""
        self.source = ""
        self.list = None
        self.lrc = False

class Song:
    def __init__( self ):
        self.artist = ""
        self.title = ""
        self.filepath = ""

class LyricsFetcher:
    
    def __init__( self ):
        self.base_url = "http://pesnicky.orava.sk"
        self.searchUrl = "http://pesnicky.orava.sk/index.php?searchword=%term%&ordering=popular&searchphrase=any&limit=50&areas[0]=songs&option=com_search"
        
    def search(self, artist, title):
        term = urllib2.quote((artist if artist else "") + " " + (title if title else ""));
        
        try:
            request = urllib2.urlopen(self.searchUrl.replace("%term%", term))
            searchResponse = request.read();
            #print(searchResponse);
        except:
            return None
        #print(searchResponse);
        
        # Search performed in 2 steps for performance reasons
        songPartMatch =  re.search("<dl class=\"search-results\">(.*?)</dl>", searchResponse, re.DOTALL | re.MULTILINE | re.UNICODE);
        print(songPartMatch.group(1));
        
        if not songPartMatch:
            return None;                

        searchResult = re.findall("<a href=\"(.*?)\".*?>\s*(.*?)\s*</.*?(?!Scorch).*?</dd>", songPartMatch.group(1), re.MULTILINE | re.DOTALL);
        
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
        
        matches = re.findall("<p\sclass=\"text\">(.*?)</p>", res, re.DOTALL | re.MULTILINE);
        
        if(len(matches) == 0):
            return None;
        print(len(matches));
        
        lyrics = ""
        i = 0;             
        for match in matches:  # sometimes match contains translation of song
            s = match;
            s = s.strip();
            #s = s.replace("<br />", "");
            s = s.replace("<i>", "");
            s = s.replace("</i>", "");
            
            # lyrics returned are not always standart - once contain new lines other time not... 
            lines = s.split("<br />");
            temp = ""
            for line in lines:
                temp += line.strip() + "\n"; 
            lyrics += temp if i == 0 else "\n***************\n" + temp; 
            i += 1;   
        print(lyrics);
        return lyrics;


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
#l = LyricsFetcher().search("Lucie Bíla", "láska je láska"); 
#l = LyricsFetcher().search("elan", "bosorka"); 
#l = LyricsFetcher().search("desmod", "hemeroidy"); 
#l = LyricsFetcher().search("tublatanka", "lod");
#l = LyricsFetcher().search("metalinda", "jan amos");
#l = LyricsFetcher().search("kabat", "colorado");
#l = LyricsFetcher().search("tri setri", "setri se chlapce");
#l = LyricsFetcher().search("orlik", "pivecko");
#l = LyricsFetcher().search("landa", "pozdrav");
l = LyricsFetcher().search("", "helenko");

  
#LyricsFetcher().findLyrics(l[0][1]);
        
        