#!/usr/bin/python3
from urllib.parse import urlsplit
from urllib.request import urlopen
from html.parser import HTMLParser
from enum import Enum
from gglsbl import SafeBrowsingList

class ThirdPartyChecker(object):

    def update(self, url, label):
        return self.google_update(url, label)
        # Waiting on url_void api key from their team, for now using google only
        # google_label = self.google_update(url, label)
        # urlvoid_label = self.urlvoid_update(url, label)
        # return (google_label + urlvoid_label) / 2.0


    def google_update(self, url, label):
        sbl = SafeBrowsingList('AIzaSyDN2-Fqgg5XKl6EHp2FTAwyAQU7FpTz8V0')
        threat_list = sbl.lookup_url(url)

        certainty = abs(label)

        if threat_list is not None and threat_list[0] == 'MALWARE':
            return min(1, label + label * (1 - certainty))
        else:
            return max(-1, label - label * (1 - certainty))

    def urlvoid_update(self, url, label):
        results = urlvoid.submit([url])
        malware_domains = results.get_detected_domains() 
        if malware_domains is not None or len(malware_domains) == 1:
            return min(1, label + label * (1 - certainty))
        else:
            return max(-1, label - label * (1 - certainty))
