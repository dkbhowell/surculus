import urllib2
import json
import os

def get_json_results(count, offset):
    pass

keyBing = 'uuaYIIN9R+4rMDPaM8m1ZPvox33aJxhjV71fRUGeUrQ='        # get Bing key from: https://datamarket.azure.com/account/keys
credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:]
count = 15
offset = 0
sort = '%27Relevance%27'

queries = ['%27TeslaMotors%27', '%27Zynga%27', '%27SpaceX%27']
directory = 'News/'
output_files = ['TeslaMotors', 'Zynga', 'SpaceX']
file_counter = 0

for query in queries:
    print 'Printing results for ' + query

    url = 'https://api.datamarket.azure.com/Bing/Search/News?' + \
          'Query=%s&NewsSortBy=%s&$top=%d&$skip=%d&$format=json' % (query, sort, count, offset)

    request = urllib2.Request(url)
    request.add_header('Authorization', credentialBing)
    requestOpener = urllib2.build_opener()
    response = requestOpener.open(request)

    results = json.load(response)
    results = results["d"]
    results = results["results"]


    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = directory + output_files[file_counter]
    file = open(filename, 'w')
    file.write(json.dumps(results))

    print json.dumps(results, indent=3)
    file_counter += 1