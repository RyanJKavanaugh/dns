# /Users/ryankavanaugh/Desktop/DNSTest
import socket
import xlrd
import requests
import urllib2
import json
import unittest
import time

workbook = xlrd.open_workbook('dns.xlsx')
worksheet = workbook.sheet_by_index(0)


class Verify_DNS_Data_From_Spreadsheet(unittest.TestCase):
    def test_dns_data(self):
        testCounter = 0
        print
        # Runs through the Domain Names & Verifies the IP addresses
        print 'Domain Name vs. NS Look Up Address:'
        print
        for x in range(1, 55):
            ipAllNumbers = None
            try:
                domainName = worksheet.cell(x, 0).value
                while ipAllNumbers == None:
                    ipAllNumbers = socket.gethostbyname(domainName)
                ipEnd = ipAllNumbers[-3:]
                ipEnd = int(ipEnd)
                nsLookUpAddress = int(worksheet.cell(x, 3).value)
                if (ipEnd != nsLookUpAddress):
                    print ipAllNumbers
                    print domainName + ' is providing an incorrect nslookup address'
                    print 'Row number: ' + str(x + 1)
                    print
                    testCounter += 1

            except:
                print ipAllNumbers
                print 'Check the ip for an error'
                print 'Row number: ' + str(x + 1)
                print domainName + ' did not connect properly'
                testCounter += 1
                print


        print

        # Run through the CARGTM Names and ensure they respond correctly from a curl-style request
        print 'CARGTM Name vs. Expected Response:'
        print

        # print requests.get('http://511-idaho-gov.cragtm.org').content

        for x in range(1, 55):
            try:
                item = str(worksheet.cell(x, 1).value)
                url = 'http://' + item
                result = None

                while result == None:
                    req = requests.get(url)
                    result = req.content
                    if req.status_code != 200:
                        result = None

                expectedResponse = str(worksheet.cell(x, 2).value)

                if expectedResponse not in result:
                    print url
                    print expectedResponse
                    print 'Row number: ' + str(x + 1)
                    print result
                    print
                    testCounter += 1
            except:
                print str(worksheet.cell(x, 1).value)
                print 'Did no connect properly'
                print 'Row number: ' + str(x + 1)
                print result
                testCounter += 1


        if testCounter > 0:
            assert False, 'DNS test failed'


if __name__ == '__main__':
    unittest.main()
