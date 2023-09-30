#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  nomorobo.py
#
#  Copyright 2018 Bruce Schubert <bruce@emxsys.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import urllib3
from bs4 import BeautifulSoup


class NomoroboService(object):

    def lookup_number(self, number):
        number = '{}-{}-{}'.format(number[0:3], number[3:6], number[6:])
        url = "https://www.nomorobo.com/lookup/%s" % number
#        url = "http://slurm.abaddon.arpa/"
        print(url)
        allowed_codes = [200,404]  # allow not found response
        htmp_doc = self.http_get(url, allowed_codes)
        soup = BeautifulSoup(htmp_doc, 'html.parser')
        hotsoup = str(soup.title.string).upper()
        
        score = 0  # = I'll have your spam!
        decision = "ANSWER"

        if "UNKNOWN CALLER" in hotsoup:
            print("Nuisance!")
            score = 1 # might be spam
            decision = "SCREEN"

        if "DO NOT ANSWER" in hotsoup:
            print("Spammer!")
            score = 2 # is spam
            decision = "VOICEMAIL"

        reason = ""
        for codemeta in soup.find_all('meta'):
            if "DESCRIPTION" in str(codemeta).upper():
                print(str(codemeta).upper())

        spam = False if score < self.spam_threshold else True

        result = {
            "spam": spam,
            "score": score,
            "reason": reason
        }
        return result

    def http_get(self, url, allowed_codes=[]):
        try:
            html_doc = urllib3.request(
                "GET",
                url
            )

            data = html_doc.data
        except:
            data = ""

        return data

    def __init__(self, spam_threshold=2):

        self.spam_threshold = spam_threshold
