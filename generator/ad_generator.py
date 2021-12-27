import json
import os
import urllib

import mysql.connector
import sys
from random import choice
from airium import Airium
from bs4 import BeautifulSoup

FILL_THE_EMPTY= False

LOCAL = False

if LOCAL:
    SERVER_URL = "http://localhost/SERP/"
else:
    SERVER_URL = "http://cs.virginia.edu/~zw3hk/SERP/"

combination_data=[('ginko_tinnitus_data_verified.json', 'ANNMMYY')]
COPIES = 3
fill = False



# data config
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="t00d00",
#     database="serp"
# )  # database connection

LOCAL = False





config_id = 0  # config id in the config sequence data table
query_id = 0  # query id in the config query data


COPIES = 3


def update_config_table(local):
    if local:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="anat",
            database="serp"
        )  # database connection
        SERVER_URL = "http://localhost/SERP/"
    else:
        db = mysql.connector.connect(
            host="hcdm3.cs.virginia.edu",
            user="zw3hk",
            passwd="Fall2021!!",
            database="serp"
        )  # database connection
        SERVER_URL = "http://cs.virginia.edu/~zw3hk/SERP/"

    cursor = db.cursor()
    cursor.execute(
        "SELECT config_query_data.entry_file, config_sequence_data.sequence FROM config_query_data  CROSS JOIN config_sequence_data where sequence LIKE 'A%'")
    combination_data = cursor.fetchall()
    for combination in combination_data:
        for i in range(COPIES):
            entry_file = combination[0]
            sequence = combination[1]

            print(entry_file)
            print(sequence)
            # load dataset
            with open(entry_file, 'rb') as f:
                data = json.load(f)
                query = data['query']
                effective = data['effective']
                ineffective = data['ineffective']
                unknown = data['inconclusive']
                topic = data['topic']

                if len(effective) < 3 or len(ineffective) < 3 or len(unknown) < 3:
                    if len(sequence) > 7 or len(sequence) == 0:
                        print("skip")
                        continue
                elif len(effective) > 3 or len(ineffective) > 3 or len(unknown) > 3:
                    if len(sequence) < 10 or len(sequence) == 0:
                        print("skip")
                        continue

                URL = SERVER_URL + query + "-" + sequence + str(i) + '.html'
                cursor.execute(
                    "INSERT INTO serp.config_data (query, entry_file, sequence, URL, used, answered, topic0, topic1) VALUES ((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s))",
                    (query, entry_file, sequence, URL, 0, 0, topic[0], topic[1]))
                db.commit()
    db.close()


def append_ad_to_top(dirpath, fname, entry_file):
    splitf = fname.split('-')
    config_suffix = splitf[1]
    if config_suffix.startswith('A'): #already an ad file
        return
    index = int(fname.split('-')[1].split('.')[0][-1])

    with open(entry_file, 'rb') as f:
        data = json.load(f)
        ads = data['ads']

    with open(dirpath + '\\' + fname, 'rb') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    anchors = soup.find_all("a")
    for a in anchors:
        href =a['href']
        pos_start_index = href.find('pos=') +4
        pos = int(href[pos_start_index])
        new_pos = pos +1
        new_ref = href[:pos_start_index]+str(new_pos)+href[(pos_start_index+1):]
        a['href'] = new_ref

    template = Airium()
    entry = ads[index%len(ads)]
    with template.div(klass="searchresult"):
        with template.p():
            template('<b style="color:black;display:inline-block;">Ad · &nbsp; </b> '+
                entry['short_url'])
        #                                        with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
        #                                                        onclick="url(" + str(position_counter) + ");"):
        with template.a(href=SERVER_URL + "trackings.php?pos=1" + "&entry=" + urllib.parse.quote(entry['URL']), target="_blank",
                        style="text-decoration: none;"):
            with template.h2():
                template(
                    entry['title'])
        with template.p(id="description"):
            template(
                entry['description'])
    html = str(template)
    new_div = BeautifulSoup(html, 'html.parser')
    tag = soup.find(id='searchresultsnumber')

    tag.insert(0,new_div)

    output_fname = dirpath + '\\'+splitf[0]+'-A'+config_suffix
    with open(output_fname, "w", encoding='utf8') as file:
        file.write(str(soup))




def append_add_to_all_files(dir):
    for file in os.listdir("."):
        if file.endswith(".html"):
            if 'EEE' in file:
                continue
            if file.startswith('Does Omega Fatty Acids treat Adhd'):
                append_ad_to_top(dir, file, 'pufa_adhd_data_verified.json')
            elif file.startswith('Does Melatonin  treat jetlag'):
                append_ad_to_top(dir, file, 'melatonin_data_verified.json')
            elif file.startswith('Does Ginkgo Biloba treat tinnitus'):
                append_ad_to_top(dir, file,  'ginko_tinnitus_data_verified.json')
            else:
                continue
            print(file)

#append_ad_to_top('C:\MAMP\htdocs\SERP','Does Ginkgo Biloba treat tinnitus-NMYNMY1.html','ginko_tinnitus_data_verified.json')
append_add_to_all_files('C:\MAMP\htdocs\SERP')
#update_config_table()