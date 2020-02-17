import urllib.request
import json
import csv
import sys
import os.path

in_txt_name= sys.argv[1] if len(sys.argv) >= 2 else "hashtags_in.txt"
out_csv_name= sys.argv[2] if len(sys.argv) >= 3 else "hashtags_out.csv"
string_out = ""
hashtags_list = []

class Hashtag:
    name = ""
    posts_count = 0

    def __init__(self, name):
        self.name = name

    def update_posts_count(self):
        url = "https://www.instagram.com/explore/tags/"+self.name+"/?__a=1"
        with urllib.request.urlopen(url) as url:
            jsondata = json.loads(url.read())
            self.posts_count = jsondata["graphql"]["hashtag"]["edge_hashtag_to_media"]["count"]
    
    def get_csv_row_array(self):
        return ([self.name, self.posts_count])

def write_csv(list):
    print("Writing csv...")
    with open(out_csv_name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Hashtag", "Posts Count"])
        for hashtag in hashtags_list:
            csv_writer.writerow(hashtag.get_csv_row_array())

if not os.path.exists(in_txt_name):
    print("Input file not found!")
    quit()

print("Opening input file...")

with open(in_txt_name,"r") as txt_file:
    for row in txt_file:
        hashtag_str = str(row.rstrip())
        hashtag = Hashtag(hashtag_str)
        print("Working on #"+hashtag_str+"...", end=" ", flush=True)
        hashtag.update_posts_count()
        hashtags_list.append(hashtag)
        print("OK")

print("Sorting list...")
hashtags_list_sorted = sorted(hashtags_list, key = lambda h: h.posts_count, reverse=True)
write_csv(hashtags_list_sorted)