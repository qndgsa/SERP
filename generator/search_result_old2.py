import json
import mysql.connector
import sys
from random import choice
from airium import Airium

# data config
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="t00d00",
#     database="serp"
# )  # database connection

db = mysql.connector.connect(
    host="hcdm3.cs.virginia.edu",
    user="zw3hk",
    passwd="Fall2021!!",
    database="serp"
)  # database connection

config_id = 0  # config id in the config sequence data table
query_id = 0  # query id in the config query data

GENERATE_ALL = True
# if this variable set to true, the generator will loop over two database to generate all
# possible configure combination

LOAD_CONFIG = True

COPIES = 3

FILL_THE_EMPTY = False

if LOAD_CONFIG:
    try:
        with open("configurations.txt") as f:
            cursor = db.cursor()
            cursor.execute(
                "truncate config_sequence_data")
            db.commit()

            line = f.readline()
            while line:
                line = line.strip()
                cursor.execute(
                    "INSERT INTO serp.config_sequence_data (sequence) VALUE (\"" + line + "\")")
                db.commit()
                line = f.readline()
            f.close()

    # entry file exception
    except IOError:
        print("Could not load configurations file.")

# read configuration data
if GENERATE_ALL:
    cursor = db.cursor()
    cursor.execute(
        "SELECT config_query_data.entry_file, config_sequence_data.sequence FROM config_query_data CROSS JOIN config_sequence_data")
    combination_data = cursor.fetchall()
else:
    cursor = db.cursor()
    cursor.execute("SELECT sequence FROM config_sequence_data WHERE config_id = (%s)", (config_id,))
    sequence_data = cursor.fetchall()

    cursor.execute("SELECT entry_file FROM config_query_data WHERE query_id = (%s)", (query_id,))
    query_data = cursor.fetchall()
    combination_data = [[query_data[0][0], sequence_data[0][0]]]

cursor.execute("truncate config_data")
# the sequence determine the display order of entries by category
# "Y" = effective, "N" = ineffective, "M" = unknown, "A" = Ad
# if gave number of the assigned category is more than entry_file's, program will replace
# them with other category in E,I,U order until run out all entries.
print(combination_data)
fill = False
# when set it as True, if the length of sequence is lower than total number of the entries, program will fill up
# the rest of entries in the html file

# Handle exceptions
def entry_exception(E_counter, I_counter, U_counter, exception_pos, position_counter):
    if exception_pos != "Y" and E_counter != len(effective):
        entry = effective[E_counter]
        with template.div(klass="searchresult"):
            with template.a():
                template(
                    entry['URL'])
            with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                            onclick="url(" + str(position_counter) + ");"):
                with template.h2():
                    template(
                        entry['title'])
            with template.p(id="description"):
                template(
                    entry['description'])
        E_counter += 1
        print("replace with effective")

    elif exception_pos != "N" and I_counter != len(ineffective):
        entry = ineffective[I_counter]
        with template.div(klass="searchresult"):
            with template.a():
                template(
                    entry['URL'])
            with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                            onclick="url(" + str(position_counter) + ");"):
                with template.h2():
                    template(
                        entry['title'])
            with template.p(id="description"):
                template(
                    entry['description'])
        I_counter += 1
        print("replace with ineffective")

    elif exception_pos != "M" and U_counter != len(unknown):
        entry = unknown[U_counter]
        with template.div(klass="searchresult"):
            with template.a():
                template(
                    entry['URL'])
            with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                            onclick="url(" + str(position_counter) + ");"):
                with template.h2():
                    template(
                        entry['title'])
            with template.p(id="description"):
                template(
                    entry['description'])
        U_counter += 1
        print("replace with unknown")

    else:
        print("No more entry for replacement")
    return E_counter, I_counter, U_counter

for combination in combination_data:
    for i in range(COPIES):

        template = Airium()
        entry_file = combination[0]
        sequence = combination[1]

        print(entry_file)
        print(sequence)
        # load dataset
        try:
            with open(entry_file, 'rb') as f:
                data = json.load(f)
            effective = data['effective']
            ineffective = data['ineffective']
            unknown = data['inconclusive']
            topic = data['topic']

            if len(effective) < 3 or len(ineffective) < 3 or len(unknown) < 3:
                if len(sequence) > 6 or len(sequence) == 0:
                    print("skip")
                    continue
            elif len(effective) > 3 or len(ineffective) > 3 or len(unknown) > 3:
                if len(sequence) < 9 or len(sequence) == 0:
                    print("skip")
                    continue

            if "A" in sequence:
                ad = data['ad']
            query = data['query']
            URL = "http://cs.virginia.edu/~zw3hk/SERP/" + query + "-" + sequence + str(i) + '.html'
            print(query, entry_file, sequence, URL)

        # entry file exception
        except IOError:
            print("Could not load entry file:", entry_file)
            sys.exit(1)

        cursor.execute(
            "INSERT INTO serp.config_data (query, entry_file, sequence, URL, used, answered, topic0, topic1) VALUES ((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s))",
            (query, entry_file, sequence, URL, 0, 0, topic[0], topic[1]))
        db.commit()

        template('<!DOCTYPE html>')
        with template.html(lang="pl"):
            # create header and load css
            with template.head():
                template.meta(charset="utf-8")
                template.title(_t="Search")
                template.link(rel="stylesheet", href="css/search_result_page.css")
                template.link(rel="stylesheet",
                              href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.5.16/css/mdb.min.css")
                template.script(src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-alpha1/jquery.min.js")
                template.script(src="https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min.js")
            # create body
            with template.body():
                # create header
                with template.div(id="header"):
                    with template.div(id="topbar"):
                        template.img(id="searchbarimage", src="../images/icon.png")
                        # create search bar
                        with template.div(id="searchbar", type="text"):
                            template("<input id=\"searchbartext\" type=\"text\" value=")
                            template("\"" + query + "\"")
                            template(">")
                            # with template.button(id="searchbarmic"):
                            #     template.img(src="images/Google_mic.svg.png")
                            with template.button(id="searchbarbutton"):
                                with template.svg(focusable="false", xmlns="http://www.w3.org/2000/svg",
                                                  viewBox="0 0 24 24"):
                                    template(
                                        "<path d=\"M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z\"></path>")
                        # template("<div id=\"boxesicon\"></div>")
                        # template("<img id=\"bellicon\" src=\"images/google_apps.png\">")
                        # template("<img id=\"profileimage\" src=\"images/google_account.png\">")

                    # create category options
                    with template.div(id="optionsbar"):
                        template("<ul id=\"optionsmenu1\"></ul>")
                    #     with template.ul(id="optionsmenu1"):
                    #             template(
                    #                 "<li id=\"optionsmenuactive\">ALL</li>")
                    #             template(
                    #                 "<li>NEWS</li>")
                    #             template(
                    #                 "<li>VIDEOS</li>")
                    #             template(
                    #                 "<li>IMAGES</li>")
                    #             template(
                    #                 "<li>MORE</li>")
                    #
                    #     with template.ul(id="optionsmenu2"):
                    #             template(
                    #                 "<li>Settings</li>")
                    #             template(
                    #                 "<li>Tools</li>")
                template(
                    " <button class=\"btn sunny-morning-gradient\" id=\"submitCode\"  disabled onclick=\"next();\" style=\"display: none; position:fixed; top:20px; left:80%;\" >Answer Question</button>")
                # search result part
                with template.div(id="searchresultsarea"):
                    with template.p(id="searchresultsnumber"):
                        # template(
                        #     "About x results (y seconds) ")

                        E_counter = 0
                        I_counter = 0
                        U_counter = 0
                        A_counter = 0
                        position_counter = 1
                        for item in sequence:
                            if item == 'Y':
                                if E_counter >= len(effective):
                                    if FILL_THE_EMPTY != False and FILL_THE_EMPTY != False:
                                        E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "Y",
                                                                                      position_counter)
                                else:
                                    entry = choice(effective)
                                    with template.div(klass="searchresult"):
                                        with template.p():
                                            template(
                                                entry['URL'])
                                        with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                                                        onclick="url(" + str(position_counter) + ");"):
                                            with template.h2():
                                                template(
                                                    entry['title'])
                                        with template.p(id="description"):
                                            template(
                                                entry['description'])
                                    E_counter += 1
                                    effective.remove(entry)
                                position_counter += 1

                            elif item == 'N':
                                if I_counter >= len(ineffective)and FILL_THE_EMPTY != False:
                                        E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "N",
                                                                                      position_counter)
                                else:
                                    entry = choice(ineffective)
                                    with template.div(klass="searchresult"):
                                        with template.p():
                                            template(
                                                entry['URL'])
                                        with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                                                        onclick="url(" + str(position_counter) + ");"):
                                            with template.h2():
                                                template(
                                                    entry['title'])
                                        with template.p(id="description"):
                                            template(
                                                entry['description'])
                                    I_counter += 1
                                    ineffective.remove(entry)
                                position_counter += 1

                            elif item == 'M' \
                                         '':
                                if U_counter >= len(unknown) and FILL_THE_EMPTY != False:
                                        E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "M",
                                                                                      position_counter)
                                else:
                                    entry = choice(unknown)
                                    with template.div(klass="searchresult"):
                                        with template.p():
                                            template(
                                                entry['URL'])
                                        with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                                                        onclick="url(" + str(position_counter) + ");"):
                                            with template.h2():
                                                template(
                                                    entry['title'])
                                        with template.p(id="description"):
                                            template(
                                                entry['description'])
                                    U_counter += 1
                                    unknown.remove(entry)
                                position_counter += 1

                            elif item == 'A':
                                # ad
                                A = ad[0]
                                if A['img_ad']:
                                    with template.card(style="padding:10px;"):
                                        template(
                                            "<b style=\"color:black;display:inline-block;\">Ads · &nbsp; </b>" + "<p style=\"display:inline-block;\">" + " " +
                                            data['query'] + "</p>")
                                        with template.div(klass="img-ad",
                                                          style="height:235px;width:135px;z-index:2;border-radius: 25px;padding:15px; margin-top: 30px;margin-left: 10px;box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"):
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
                                                        with template.a(href=A['URL'], target="_blank",
                                                                        style="text-decoration: none;", onclick="ad();"):
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
                                else:
                                    if ad_loaded:
                                        with template.div(klass="searchresult"):
                                            with template.p():
                                                template(
                                                    A['URL'])
                                            with template.a(href=A['URL'], target="_blank", style="text-decoration: none;"):
                                                with template.h2():
                                                    template(
                                                        "<b style=\"color:black;\">Ad</b> · " + A['title'])

                                            with template.p():
                                                template(
                                                    A['description'])
                                                with template.div(klass="rating"):
                                                    rating = A['rating'] * 20
                                                    with template.div(klass="rating-upper",
                                                                      style=("width:" + str(rating) + "%")):
                                                        template(
                                                            "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                                                    with template.div(klass="rating-lower"):
                                                        template(
                                                            "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                                                    with template.div(klass="rating-comment"):
                                                        with template.p():
                                                            template(
                                                                A['rating comment'])
                        if len(sequence) < (len(effective) + len(ineffective) + len(unknown) + 1) and fill == True:
                            fill_up = (len(effective) + len(ineffective) + len(unknown) + 1) - len(sequence)
                            for i in range(0, fill_up):
                                E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "",
                                                                                  position_counter)
                                position_counter += 1

            with template.script():

                template("var mouse_movement = [];")
                template("var basic = [];")
                template("var user_action = [];")
                template("var user_view = [];")

                template("var exp_id = random_exp_id();")
                template("var window_width = document.body.scrollWidth;")
                template("var window_height = document.body.scrollHeight;")

                template("$.get(\"https://ipinfo.io\", function(response) {")
                template("    user_id =response.ip;")
                template("    upload_basic();")
                template("}, \"json\")")

                template("window.setInterval(function () {")
                template("    upload_view(document.documentElement.scrollTop);")
                template("}, 3000);")

                template("function url(link_id) {")
                template("    document.getElementById(\"submitCode\").disabled = false;")
                template("    document.getElementById(\"submitCode\").style.display = \"block\";")
                template("    upload_action(\"click link\",link_id);")
                template("}")

                template("function ad() {")
                template("    upload_action(\"click ad\",0);")
                template("}")

                template("function next() {")
                template("        upload_action(\"close_page\", 0);")
                template("        var end_time = new Date().toLocaleString('en-US');")
                template("        basic.push(end_time);")
                template("        $.cookie('basic', JSON.stringify(basic));")
                template("        // $.cookie('mouse_movement', JSON.stringify(mouse_movement));")
                template("        $.cookie('user_action', JSON.stringify(user_action));")
                template("        $.cookie('user_view', JSON.stringify(user_view));")
                template("        window.location.href='post_question.php';")
                template("    }")

                template("mouse_wheel();")
                template("function mouse_wheel() {")
                template("    var scrollFunc = function (e) {")
                template("        var e = window.event || e;")
                template("        if (e.wheelDelta) {")
                template("            if (e.wheelDelta > 0) {")
                template("                upload_action(\"scroll up\",0)")
                template("            }")
                template("            if (e.wheelDelta < 0) {")
                template("                upload_action(\"scroll down\",0)")
                template("            }")
                template("        } else if (e.detail) {")
                template("            if (e.detail> 0) {")
                template("               upload_action(\"scroll up\",0)")
                template("            }")
                template("            if (e.detail< 0) {")
                template("                upload_action(\"scroll down\",0)")
                template("            }")
                template("        }")
                template("    };")
                template("    if (document.addEventListener) {")
                template("        document.addEventListener('DOMMouseScroll', scrollFunc, false);")
                template("    }")
                template("    window.onmousewheel = document.onmousewheel = scrollFunc;")
                template("}")

                template("function mouse_position(e, obj) {")
                template("    var e = window.event || e;")
                template("    var position = [e.clientX, e.clientY];")
                template("    upload_position(position[0],position[1]);")
                template("}")

                template("window.onload = function() {")
                template("    document.onmousemove = function(event) {mouse_position(event, this);}")
                template("}")

                #             template("window.onbeforeunload = function (event) {")
                #             template("    return \"Hey, you're leaving the site. Bye!\";")
                #             template("}")

                template("function upload_basic() {")
                template("    var time = new Date().toLocaleString('en-US');")
                template("    basic = [exp_id, window_width, window_height, time];")
                template("}")

                template("//function upload_position(x,y) {")
                template("//     var time = new Date().toLocaleString();")
                template("//     var position = [x,y,time];")
                template("//     mouse_movement.push(position);")
                template("// }")

                template("function upload_action(type,link_id) {")
                template("    var time = new Date().toLocaleString('en-US');")
                template("    var action = [link_id, type, time];")
                template("    user_action.push(action);")
                template("}")

                template("function upload_view(view) {")
                template("    var time = new Date().toLocaleString('en-US');")
                template("    var v = [view, time];")
                template("    user_view.push(v);")
                template("}")

                template("function random_exp_id() {")
                template("    var t = \"ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678\",")
                template("    a = t.length,")
                template("    id = \"\";")
                template("    for (i = 0; i < 8; i++) id += t.charAt(Math.floor(Math.random() * a));")
                template("    return id")
                template("}")

                # #related
                # with template.div(id="relatedsearches"):
                #     with template.h3():
                #         template(
                #             "Searches related to" + ad["query"])
                #     with template.div(klass="relatedlists"):
                #         with template.ul(id="relatedleft"):
                #                 template(
                #                     "<li>a</li>")
                #                 template(
                #                     "<li>b</li>")
                #                 template(
                #                     "<li>c</li>")
                #                 template(
                #                     "<li>d</li>")
                #         with template.ul(id="relatedright"):
                #                 template(
                #                     "<li>e</li>")
                #                 template(
                #                     "<li>f</li>")
                #                 template(
                #                     "<li>g</li>")
                #                 template(
                #                     "<li>h</li>")
                # #page list bar
                # with template.div(klass="pagebar"):
                #     with template.ul(klass="pagelist"):
                #         template(
                #             "<li class=\"pagelistprevious\">Previous</li>")
                #         template(
                #             "<li class=\"pagelistfirst\">1</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">2</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">3</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">4</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">5</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">6</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">7</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">8</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">9</li>")
                #         template(
                #             "<li class=\"pagelistnumber\">10</li>")
                #         template(
                #             "<li class=\"pagelistnext\">Next</li>")
                # create footer
                # with template.div(id="footer"):
                #     with template.div(id="footerlocation"):
                #         with template.p():
                #             template("Somewhere")
                #         with template.p():
                #             template("- From your place (Location History) - Use precise location - Learn more")
                #
                #     with template.ul(id="footermenu"):
                #         template(
                #             "<li>Help</li>")
                #         template(
                #             "<li>Send feedback</li>")
                #         template(
                #             "<li>Privacy</li>")
                #         template(
                #             "<li>Terms</li>")

        # load as html
        html = str(template)  # casting to string extracts the value

        # output html file
        with open(query + "-" + sequence + str(i) + '.html', 'w', encoding='utf-8') as f:
            f.write(str(html))
db.close()
