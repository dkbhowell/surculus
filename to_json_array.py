import os

base_directory = '/Users/dustin/Dev/social_networks_project/surculus/companies/'
test_file = '/Users/dustin/Dev/social_networks_project/surculus/companies/SpaceX/2015-04-08/top_tweets_copy'

def fix_file(filename, fixed_filename):
    out_file = open(fixed_filename, 'w')
    out_file.write('[\n')
    file = open(filename, 'r')
    for line in file:
        if line[0] == '{':
            out_file.write(line[:len(line)])
            out_file.write(',\n')
    out_file.seek(-2, 1)
    out_file.write(' ]')

for co_folder in os.listdir(base_directory):
    if co_folder[0] != '.':
        co_dir = base_directory + co_folder
        #print co_dir
        for date_folder in os.listdir(co_dir):
            if date_folder[0] != '.':
                tweet_filename = co_dir + "/" + date_folder + "/top_tweets"
                if os.path.isfile(tweet_filename):
                    print tweet_filename
                    fix_file(tweet_filename, tweet_filename + '_fixed')
                    #tweet_file = open(tweet_filename)

fix_file(test_file, '/Users/dustin/Dev/social_networks_project/surculus/companies/SpaceX/2015-04-08/top_tweets_copy_fixed')