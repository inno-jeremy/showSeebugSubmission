#!/usr/bin/env python
#coding: utf-8

import re
from pocsuite.net import req
from pocsuite.poc import Output, POCBase
from pocsuite.utils import register

class showSeebugSubmission(POCBase):
    vulID = 'showSeebugSubmission'
    version = 'showSeebugSubmission'
    vulDate = '2016-01-04'
    references = [' ']
    name = 'showSeebugSubmission'
    appPowerLink = 'showSeebugSubmission'
    appName = 'showSeebugSubmission'
    appVersion = 'showSeebugSubmission'
    vulType = 'showSeebugSubmission'
    desc = 'showSeebugSubmission'
    samples = [' ']


    def _attack(self):
        return self._verify()


    def _verify(self, verify=True):
        result = {}
        total = 0
        start_page = raw_input('start page:')
        stop_page = raw_input('stop page:')
        pages = int(stop_page) - int(start_page) + 1

        for page_range in range(pages):
            response = req.get(self.url + '/market/?page=%d' % (page_range + int(start_page))).content
            raw = re.findall('<tr>([\s\S]+?)</tr>', response)    #正则表达式非贪婪匹配
            for amount_of_raws in range(len(raw)):
                if '<span class="label label-brand">提交</span>' in raw[amount_of_raws]:
                    author = re.search('<img [\s\S]+?>([\s\S]+?)</a>' , raw[amount_of_raws]).group(1)
                    time = re.search('<td class="text-center datetime">[\s\S]+?(\d[\d :-]+)[\s\S]+?</td>' , raw[amount_of_raws]).group(1)
                    type = re.search('<td class="text-center">(.+)</td>' , raw[amount_of_raws]).group(1)
                    vid = re.search('<a class="vul-title" href="/vuldb/(ssvid-\d+)">([\s\S]+?)</a>' , raw[amount_of_raws]).group(1)
                    title = re.search('<a class="vul-title" href="/vuldb/ssvid-\d+">([\s\S]+?)</a>' , raw[amount_of_raws]).group(1)
                    award = re.search('</i>[\s\S]+?([\d\.]+kB)[\s\S]+?</td>' , raw[amount_of_raws]).group(1)

                    total = total + 1
                    print '\n'
                    print str(total) + '.'
                    print author
                    print time
                    print type
                    print vid
                    print title
                    print award
                    print '\n'

                    result['VerifyInfo'] = {}
                    result['VerifyInfo']['URL'] = self.url
        print 'total:' , total
        return self.parse_attack(result)


    def parse_attack(self, result):
        output = Output(self)

        if result:
            output.success(result)
        else:
            output.fail('failed')

        return output

register(showSeebugSubmission)
