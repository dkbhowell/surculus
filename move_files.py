import shutil
import os

from_directory = 'popular_tweet_logs/TeslaMotors/'
to_directory_base = 'companies/TeslaMotors/'

for file in os.listdir(from_directory):
    if file[0] != '.':
        print file
        to_directory = to_directory_base + file + "/"
        if not os.path.exists(to_directory):
            os.makedirs(to_directory)
        from_path = from_directory + file
        to_path = to_directory + "company_mentions"
        shutil.copy(from_path, to_path)