import json
import ast
import math
import os

num_tweets = 3 # the number of most popular items to extract
directories = ['company_tweet_logs', 'popular_tweet_logs']
write_folder = 'top_tweets'
test_file = 'popular_tweet_logs/TeslaMotors/2015-04-19'

def find_min_dict(dict_list, key):
    min = {}
    for dict in dict_list:
        val = dict[key]
        if key not in min:
            min = dict
        else:
            if val < min[key]:
                min = dict
    return min

def get_dicts_from_file(file):
    dict_list = []
    for line in file:
        if line[0] == '{': #line is a json object
            py_dict_str = line.strip()
            py_dict = ast.literal_eval(py_dict_str)
            dict_list.append(py_dict)
    file.close()
    return dict_list

def get_top_dicts(dicts, num_to_return):
    count = len(dicts)
    if count < num_to_return:
        return dicts
    top_dicts = []
    rtw_stats, fav_stats, flw_stats = {},{},{}
    for json_dict in dicts:
        rt = json_dict['retweet_count']
        fav = json_dict['favorite_count']
        flw = json_dict['user']['followers_count']
        if rt >= rtw_stats.get('max', 0):
            rtw_stats['max'] = rt
        if fav >= fav_stats.get('max', 0):
            fav_stats['max'] = fav
        if flw >= flw_stats.get('max', 0):
            flw_stats['max'] = flw
        rtw_stats['total'] = rtw_stats.get('total', 0) + rt
        fav_stats['total'] = fav_stats.get('total', 0) + fav
        flw_stats['total'] = flw_stats.get('total', 0) + flw
    rtw_stats['average'] = float(rtw_stats['total']) / count
    fav_stats['average'] = float(fav_stats['total']) / count
    flw_stats['average'] = float(flw_stats['total']) / count

    for json_dict in dicts:
        rt = json_dict['retweet_count']
        fav = json_dict['favorite_count']
        flw = json_dict['user']['followers_count']

        rtw_stats['sum_sq_diff'] = rtw_stats.get('sum_sq_diff', 0) + math.pow((rt - rtw_stats['average']), 2)
        fav_stats['sum_sq_diff'] = fav_stats.get('sum_sq_diff', 0) + math.pow((rt - fav_stats['average']), 2)
        flw_stats['sum_sq_diff'] = flw_stats.get('sum_sq_diff', 0) + math.pow((rt - flw_stats['average']), 2)

    rtw_stats['avg_sq_diff'] = rtw_stats['sum_sq_diff'] / count
    fav_stats['avg_sq_diff'] = fav_stats['sum_sq_diff'] / count
    flw_stats['avg_sq_diff'] = flw_stats['sum_sq_diff'] / count

    rtw_stats['stdev'] = math.sqrt(rtw_stats['avg_sq_diff'])
    fav_stats['stdev'] = math.sqrt(fav_stats['avg_sq_diff'])
    flw_stats['stdev'] = math.sqrt(flw_stats['avg_sq_diff'])

    min_dict = {}
    for json_dict in dicts:
        rt = json_dict['retweet_count']
        fav = json_dict['favorite_count']
        flw = json_dict['user']['followers_count']
        if rtw_stats['max'] > 0:
            rtw_percent = float(rt) / rtw_stats['max']
        else:
            rtw_percent = 0
        if fav_stats['max'] > 0:
            fav_percent = float(fav) / fav_stats['max']
        else:
            fav_percent = 0
        if flw_stats['max'] > 0:
            flw_percent = float(flw) / flw_stats['max']
        else:
            flw_percent = 0
        rtw_score = rtw_percent * retweet_weight
        fav_score = fav_percent * favorite_weight
        flw_score = flw_percent * flw_percent
        score = rtw_score + fav_score + flw_score
        json_dict['popularity_score'] = score

        if len(top_dicts) == 0 and len(top_dicts) < num_to_return:
            top_dicts.append(json_dict)
            min_dict = json_dict
        elif len(top_dicts) < num_to_return:
            top_dicts.append(json_dict)
            if score < min_dict['popularity_score']:
                min_dict = json_dict
        else:
            if score > min_dict['popularity_score']:
                top_dicts.remove(min_dict)
                top_dicts.append(json_dict)
                min_dict = find_min_dict(top_dicts, 'popularity_score')

    return top_dicts


retweet_weight = 60
favorite_weight = 30
followers_weight = 10


if __name__ == '__main__':
    if (retweet_weight + favorite_weight + followers_weight) != 100:
        raise AssertionError("Weights not equal to 100")


    cwd = os.getcwd()
    base_directory = cwd + '/companies/'
    for company in os.listdir(base_directory):
        company_dir = base_directory + company + "/"
        if os.path.isdir(company_dir):
            company_top_tweets = {}
            for date in os.listdir(company_dir):
                if date[0] != '.':
                    date_dir = company_dir + date + "/"
                    company_tweets = date_dir + 'company_tweets'
                    company_mentions = date_dir + 'company_mentions'
                    top_tweets = []
                    if os.path.isfile(company_tweets):
                        print 'company tweets is file'
                        co_tweets_file = open(company_tweets)
                        co_tweet_dicts = get_dicts_from_file(co_tweets_file)
                        co_tweets_file.close()
                        top_tweets = get_top_dicts(co_tweet_dicts, 1)
                    if os.path.isfile(company_mentions):
                        print 'company mentions is a file'
                        co_mentions_file = open(company_mentions)
                        co_mention_dicts = get_dicts_from_file(co_mentions_file)
                        co_mentions_file.close()
                        top_mention_dicts = []
                        if len(top_tweets) == 1:
                            top_mention_dicts = get_top_dicts(co_mention_dicts, 2)
                        else:
                            top_mention_dicts = get_top_dicts(co_mention_dicts, 3)
                        top_tweets.extend(top_mention_dicts)
                    top_tweets_filename = date_dir + 'top_tweets'
                    top_tweet_file = open(top_tweets_filename, 'w')
                    for tweet_dict in top_tweets:
                        top_tweet_file.write(json.dumps(tweet_dict) + '\n\n')




                #company_top_tweets[data_file] = None
                #nfile = open(company_path + "/" + data_file)
                #tweet_dicts = get_dicts_from_file(nfile)
                #nfile.close()
                #top_dicts = []
                #if len(tweet_dicts) > 0:
                #    top_dicts = get_top_dicts(tweet_dicts, 1)
                #company_top_tweets[data_file] = top_dicts



    #file = open(test_file)

    #write_dir = write_folder + "/TeslaMotors"
    #if not os.path.exists(write_dir):
    #    os.makedirs(write_dir)

    #write_filename = write_dir + "/" + "2015-04-19"
    #write_file = open(write_filename, 'w')

    #json_dicts = get_dicts_from_file(file)
    #top_dicts = get_top_dicts(json_dicts, 2)
    #for dict in top_dicts:
    #    print json.dumps(dict, indent=3)
