#!/usr/bin/python
import sys, os, re
from optparse import OptionParser

# parse the options
parser = OptionParser()
parser.add_option('-a', '--authorize', action='store_true', dest='authorize')
parser.add_option('-g', '--guid', type='string', dest='guid',
                  help="not actually a guid")
parser.add_option('-p', '--programs', action='store_true', dest='progs')
parser.add_option('-c', '--channels', action='store_true', dest='chans')
parser.add_option('-v', '--video', action='store_true', dest='video')
parser.add_option('-s', '--shows', action='store_true', dest='shows')
(options, args) = parser.parse_args()

from resources.lib.livechannels import *
from resources.lib.liveprograms import *
from resources.lib.shows import *
from resources.lib.cbc import *

def progress(x):
    print x

cbc = CBC()
chans = LiveChannels()
events = LivePrograms()
shows = Shows()
res = []

if options.authorize:
    reg_url = cbc.getRegistrationURL()
    print 'Registration URL: "{}"'.format(reg_url)
    if not cbc.registerDevice(reg_url):
        print 'Error: unable to authorize'
        sys.exit(1)
    sys.exit(0)

if options.chans:
    res = chans.getLiveChannels()
elif options.progs:
    res = events.getLivePrograms()
elif options.video:
    res = shows.getStream(args[0])
    print res
    sys.exit(0)
elif options.shows:
    res = shows.getShows(None if len(args) == 0 else args[0],
                         progress_callback = progress)
else:
    print '\nPlease specify something to do\n'
    parser.print_help()
    sys.exit(1)

for item in res:
    if options.guid == None:
        if options.chans:
            print '{}) {} {}: {}'.format(item['guid'], item['cbc$callSign'], item['title'], item['description'])
        elif options.progs:
            if item['availabilityState'] == 'available':
                print '{}) {}: {}'.format(item['guid'], item['title'], item['description'])
        elif options.shows:
            print '{}) {}: {}\n\t{}\n'.format(item['guid'],
                                              item['title'].encode('utf-8'),
                                              item['description'].encode('utf-8'),
                                              item['url'])
    elif item['guid'] == options.guid:
        smil = item['content'][0]['url']
        print cbc.parseSmil(smil)

