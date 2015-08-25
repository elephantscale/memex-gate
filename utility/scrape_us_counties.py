#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#ITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import sys
from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup


def parse_arguments():
    """ Process command line arguments """
    parser = ArgumentParser(description='Grabs tables from html')
    parser.add_argument('-u', '--url', required=False, default='http://en.wikipedia.org/wiki/List_of_counties_by_U.S._state', help='url to grab from')
    args = parser.parse_args()
    return args


def parse_lists(countiesLists):
    """ Get data from counties lists """
    results = []
    for list in countiesLists:
        elements = list.find_all('li')
        for list_element in elements:
            if list_element.find('a'):
                text = list_element.find('a').get_text()
                if (len(text) > 1):
                    results.append(text.split(',')[0])

    return results

def main():
    '''
    Purpose::
        ScrapeUSCounties.py merely fetches
        http://en.wikipedia.org/wiki/List_of_counties_by_U.S._state
        and uses XPATH to extract out County
        from every State in the U.S.
        The data is then written to a flat file one county per
        line.
    Input::

    Output::

    Assumptions::
    '''
    # Get arguments
    args = parse_arguments()
    if args.url:
        url = args.url

    # Make soup
    try:
        resp = urlopen(url)
    except URLError as e:
        print 'An error occured fetching %s \n %s' % (url, e.reason)
        return 1
    soup = BeautifulSoup(resp.read())


    # Get rows
    try:
        countiesLists = soup.find_all('ol')
    except AttributeError as e:
        print 'No counties lists found, exiting'
        return 1

    # Get data
    data = parse_lists(countiesLists)

    f = open('US_counties.txt', 'w')
    # Print data
    #f.write("\n".join(str(i).encode('utf8') for i in table_data))
    for i in data:
        f.write((i).encode('utf8') +'\n')

    f.close()

    #write data to flat file

if __name__ == '__main__':
    status = main()
    sys.exit(status)
