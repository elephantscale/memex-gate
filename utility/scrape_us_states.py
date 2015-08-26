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
    parser.add_argument('-u', '--url', required=False, default='http://simple.wikipedia.org/wiki/List_of_U.S._states', help='url to grab from')
    args = parser.parse_args()
    return args


def parse_states(rows):
    """ Get data from counties lists """
    results = []
    for row in rows:
        elements = row.find_all('td')
        row_data = {}
        row_data["code"] = elements[0].get_text()
        row_data["name"] = elements[1].get_text()
        row_data["capital"] = elements[2].get_text()
        results.append(row_data)

    return results

def main():
    '''
    Purpose::
        ScrapeUSStates.py merely fetches
        https://simple.wikipedia.org/wiki/List_of_U.S._states
        and uses XPATH to extract out State
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


    # Get table
    try:
        table = soup.find_all('table')[0]
    except AttributeError as e:
        print 'No tables found, exiting'
        return 1


    # Get rows
    try:
        rows = table.find_all('tr')
        rows.pop(0) # remove header
    except AttributeError as e:
        print 'No counties lists found, exiting'
        return 1

    # Get data
    data = parse_states(rows)

    f = open('us_states.txt', 'w')
    # Print data
    #f.write("\n".join(str(i).encode('utf8') for i in table_data))
    for r in data:
        f.write((r["name"]).encode('utf8') + ':code=' + r["code"] + ':capital=' + r["capital"] +'\n')

    f.close()

    #write data to flat file

if __name__ == '__main__':
    status = main()
    sys.exit(status)
