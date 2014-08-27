#-*- coding: UTF-8 -*-
'''
Created on 25.8.2014
@author: psmorada
'''
import urllib2;
import re;

__title__ = 'pesnicky.orava.sk'
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
        #print(songPartMatch.group(1));
        
        if not songPartMatch:
            return None;                

        searchResult = re.finditer("<a href=\"(.*?)\".*?>\s*(.*?)\s*</.*?</dd>", songPartMatch.group(1), re.MULTILINE | re.DOTALL);
        
#         if len(searchResult) == 0:
#             print("None");
#             return None;
        
        links = [];
        
        #print("*******************")        
        i = 0;
        for result in searchResult:
            print(result.group(0));
            if(result.group(0).find("Scorch") > -1):
                continue;
            
            a = [];
            a.append(result.group(2)); # name from the server
            #print(result[1]);
            a.append(self.base_url + result.group(1));  # url with lyrics
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
        
        match = re.search("<div class=\"mj_song_body\">\s*<pre>(.*?)</pre>", res, re.DOTALL | re.MULTILINE);
        
        if(not match):
            print("No match")
            return None;
             
        s = match.group(1);
        s = s.strip();
        #s = s.replace("<br />", "");
        s = s.replace("<i>", "");
        s = s.replace("</i>", "");
        s = s.replace("<br />", "");
            
            
        print(s);
        return s;


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
#l = LyricsFetcher().search("", "helenko");
#l = LyricsFetcher().search("", "macejko");
#l = LyricsFetcher().search("", "ceresne");
#l = LyricsFetcher().search("", "v hlbokej doline");
#l = LyricsFetcher().search("", "ked ty zajdes i ja zajdu");
l = LyricsFetcher().search("", "70 sukien mala");
l = LyricsFetcher().search("", "Kopala studienku");


  
LyricsFetcher().findLyrics(l[0][1]);
        
        