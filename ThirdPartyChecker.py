#!/usr/bin/python3
from urllib.parse import urlsplit
from urllib.request import urlopen
from html.parser import HTMLParser
from enum import Enum
from gglsbl import SafeBrowsingList



class ThirdPartyChecker(object):

    def update(self, url, label):
        return google_update(url, label)

    def google_update(self, url, label):
        sbl = SafeBrowsingList('AIzaSyDN2-Fqgg5XKl6EHp2FTAwyAQU7FpTz8V0')
        threat_list = sbl.lookup_url(url)
        if len(threat_list) > 0 and threat_list[0] == 'MALWARE':
            return min(1, label + 0.25)
        else:
            return max(-1, label - 0.25)