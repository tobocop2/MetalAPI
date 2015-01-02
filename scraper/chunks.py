import os
import json

cmd = 'scrapy crawl ma -o ma.json'
os.system(cmd)

with open('ma.json') as infile:
    print 'loading file'
    o = json.load(infile)
    print 'file loaded'
    chunkSize = 500
    try:
        release_dir = 'chunks'
        os.makedirs(release_dir)
    except OSError:
        if not os.path.isdir(release_dir):
            raise
    os.chdir(release_dir)
    for i in xrange(0, len(o), chunkSize):
        with open('ma.json' + '_' + str(i//chunkSize) + '.json', 'w') as outfile:
            json.dump(o[i:i+chunkSize], outfile)
