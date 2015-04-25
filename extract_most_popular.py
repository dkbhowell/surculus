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
        if rt > rtw_stats.get('max', 0):
            rtw_stats['max'] = rt
        if fav > fav_stats.get('max', 0):
            fav_stats['max'] = fav
        if flw > flw_stats.get('max', 0):
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
        rtw_percent = float(rt) / rtw_stats['max']
        fav_percent = float(fav) / fav_stats['max']
        flw_percent = float(flw) / flw_stats['max']
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
    company_tweet_directory = cwd + "/" + 'company_tweet_logs'
    mention_tweet_directory = cwd + "/" + 'popular_tweet_logs'
    for company in os.listdir(company_tweet_directory):
        company_path = company_tweet_directory + "/" + company
        if os.path.isdir(company_path):
            company_top_tweets = {}
            for data_file in os.listdir(company_path):
                print company + " - " + data_file
                company_top_tweets[data_file] = None
                nfile = open(company_path + "/" + data_file)
                tweet_dicts = get_dicts_from_file(nfile)
                nfile.close()

    for directory in directories:
        path = cwd + "/" + directory
        #print path
        for company_dir in os.listdir(path):
            new_path = path + "/" + company_dir
            if os.path.isdir(new_path):
                #print new_path
                for data_file in os.listdir(new_path):
                    read_filename = new_path + "/" + data_file
                    #print read_filename

    file = open(test_file)

    write_dir = write_folder + "/TeslaMotors"
    if not os.path.exists(write_dir):
        os.makedirs(write_dir)

    write_filename = write_dir + "/" + "2015-04-19"
    write_file = open(write_filename, 'w')

    json_dicts = get_dicts_from_file(file)
    top_dicts = get_top_dicts(json_dicts, 3)
    for dict in top_dicts:
        print json.dumps(dict, indent=3)
