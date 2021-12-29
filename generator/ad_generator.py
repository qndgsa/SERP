import json
import os
import urllib

import mysql.connector
from airium import Airium
from bs4 import BeautifulSoup



FILL_THE_EMPTY= False

LOCAL = False

if LOCAL:
    SERVER_URL = "http://localhost/SERP/"
else:
    SERVER_URL = "http://cs.virginia.edu/~zw3hk/SERP/"

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


def generate_image_ad_html(query, ads):
    template = Airium()
    template('<p > <b style="color:black; font-size: 80%">Ads · &nbsp; </b><span style="font-size: 150%" >' + query +' </span></p>')

    with template.card(style="padding:10px;"):
        with template.table():
            for i in range(0,len(ads)):
                A = ads[i]
                with template.tr():
                    with template.div(klass="img-ad",
                                      style="display: inline-block; height:235px;width:135px;z-index:2;border-radius: 25px;padding:15px; margin-top: 30px;margin-left: 10px;box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"):
                        with template.div(klass="container"):
                            with template.div(klass="img"):
                                with template.a(href=A['URL'], target="_blank", onclick="ad();"):
                                    with template.div(klass="img-container",
                                                      style="padding:4px;background-color:#F9F9F9"):
                                        with template.div(klass="img-container-sizer",
                                                          style="display:inline-block;text-align:center;height:114px;width:114px"):
                                            template(
                                                "<span class =\"space\"> </span> ")
                                            template(
                                                "<img style=\"border:none;margin:0;vertical-align:middle;border-radius:0%\" height=\"114\" src=\"" +
                                                A['img_link'] + "\" width=\"114\">")
                        with template.div(klass="ad-title", style="width:135px; height: 100px;"):
                            with template.div(klass="title-container"):
                                with template.div(klass="title", style="height:50px"):
                                    with template.a(href=SERVER_URL + "trackings.php?pos=1" + "&ad_index="+str(i+1)+"&entry=" + urllib.parse.quote(A['URL']), target="_blank",
                                                    style="text-decoration: none;"):
                                        with template.span(klass="title-text",
                                                           style="-webkit-line-clamp:1;overflow: hidden;text-overflow: ellipsis;display: -webkit-box;-webkit-line-clamp: 2;-webkit-box-orient: vertical;"):
                                            template(
                                                A['title'])
                                with template.div(klass="price"):
                                    template(
                                        A['price'])
                                with template.div(klass="brand"):
                                    with template.span(klass="brand-text", style="font-size:10px;"):
                                        template(
                                            A['brand'])
                            with template.div(klass="rating"):
                                rating = A['rating'] * 20
                                with template.div(klass="rating-upper",
                                                  style=("width:" + str(rating) + "%")):
                                    template(
                                        "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                                with template.div(klass="rating-lower"):
                                    template(
                                        "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                                with template.span(klass="rating-comment", style="color:black;"):
                                    template(
                                        "(" + A['rating comment'] + ")")
    html = str(template)
    print(html)

if __name__ == "__main__":

    ad = {
        "title": "GNC Herbal Plus Ginkgo Biloba 120Mg - Ginkgo Biloba - 100 Capsules",
        "img_ad": True,
        "URL": "https://www.gnc.com/ginkgo-biloba/183412.html?utm_medium=organic",
        "img_link": "data:image/png;base64,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",
        "description": "",
        "price": "$16.99",
        "brand": "GNC",
        "rating": 4.3,
        "rating comment": "43"
        }
    generate_image_ad_html(ads=[ad,ad,ad, ad], query = 'ginkgo biloba tinnitus')
    #append_ad_to_top('C:\MAMP\htdocs\SERP','Does Ginkgo Biloba treat tinnitus-NMYNMY1.html','ginko_tinnitus_data_verified.json')
    #append_add_to_all_files('C:\MAMP\htdocs\SERP')
    #update_config_table(local = False)