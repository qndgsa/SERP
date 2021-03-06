import json
import sys
import mysql.connector

from airium import Airium

template = Airium()

# data config
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="t00d00",
    database="serp"
)  # database connection

config_id = 0  # config id in the config sequence data table
query_id = 0  # query id in the config query data

GENERATE_ALL = False
# if this variable set to true, the generator will loop over two database to generate all
# possible configure combination

# read configuration data
cursor = db.cursor()
cursor.execute("SELECT sequence FROM config_sequence_data WHERE config_id = (%s)", (config_id,))
sequence_data = cursor.fetchall()

cursor.execute("SELECT entry_file FROM config_query_data WHERE query_id = (%s)", (query_id,))
query_data = cursor.fetchall()

entry_file = query_data[0][0]

sequence = sequence_data[0][0]
# the sequence determine the display order of entries by category
# "E" = effective, "I" = ineffective, "U" = unknown, "A" = Ad
# if gave number of the assigned category is more than entry_file's, program will replace
# them with other category in E,I,U order until run out all entries.

fill = True
# when set it as True, if the length of sequence is lower than total number of the entries, program will fill up
# the rest of entries in the html file

db.close()
# load dataset
try:
    with open(entry_file, 'rb') as f:
        data = json.load(f)
    effective = data['effective']
    ineffective = data['ineffective']
    unknown = data['unknown']
    ad = data['ad']

# entry file exception
except IOError:
    print("Could not load entry file:", entry_file)
    sys.exit(1)


# Handle exceptions
def entry_exception(E_counter, I_counter, U_counter, exception_pos, position_counter):
    if exception_pos != "E" and E_counter != len(effective):
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
            with template.p():
                template(
                    entry['description'])
        E_counter += 1
        print("replace with effective")

    elif exception_pos != "I" and I_counter != len(ineffective):
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
            with template.p():
                template(
                    entry['description'])
        I_counter += 1
        print("replace with ineffective")

    elif exception_pos != "U" and U_counter != len(unknown):
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
            with template.p():
                template(
                    entry['description'])
        U_counter += 1
        print("replace with unknown")

    else:
        print("No more entry for replacement")
    return E_counter, I_counter, U_counter


template('<!DOCTYPE html>')
with template.html(lang="pl"):
    # create header and load css
    with template.head():
        template.meta(charset="utf-8")
        template.title(_t="Search")
        template.link(rel="stylesheet", href="css/search_result_page.css")
        template.link(rel="shortcut icon", type="image/ico", href="images/favicon.ico")
    # create body
    with template.body():
        # create header
        with template.div(id="header"):
            with template.div(id="topbar"):
                template.img(id="searchbarimage", src="../images/icon.png")
                # create search bar
                with template.div(id="searchbar", type="text"):
                    template("<input id=\"searchbartext\" type=\"text\" value=")
                    template("\"" + data['query'] + "\"")
                    template(">")
                    # with template.button(id="searchbarmic"):
                    #     template.img(src="images/Google_mic.svg.png")
                    with template.button(id="searchbarbutton"):
                        with template.svg(focusable="false", xmlns="http://www.w3.org/2000/svg", viewBox="0 0 24 24"):
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

        # search result part
        with template.div(id="searchresultsarea"):
            with template.p(id="searchresultsnumber"):
                # template(
                #     "About x results (y seconds) ")
                # 10 search result, load from json file
                E_counter = 0
                I_counter = 0
                U_counter = 0
                A_counter = 0
                position_counter = 1
                for item in sequence:
                    if item == 'E':
                        if E_counter >= len(effective):
                            E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "E",
                                                                              position_counter)
                        else:
                            entry = effective[E_counter]
                            with template.div(klass="searchresult"):
                                with template.p():
                                    template(
                                        entry['URL'])
                                with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                                                onclick="url(" + str(position_counter) + ");"):
                                    with template.h2():
                                        template(
                                            entry['title'])
                                with template.p():
                                    template(
                                        entry['description'])
                            E_counter += 1
                        position_counter += 1

                    elif item == 'I':
                        if I_counter >= len(ineffective):
                            E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "I",
                                                                              position_counter)
                        else:
                            entry = ineffective[I_counter]
                            with template.div(klass="searchresult"):
                                with template.p():
                                    template(
                                        entry['URL'])
                                with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                                                onclick="url(" + str(position_counter) + ");"):
                                    with template.h2():
                                        template(
                                            entry['title'])
                                with template.p():
                                    template(
                                        entry['description'])
                            I_counter += 1
                        position_counter += 1

                    elif item == 'U':
                        if U_counter >= len(unknown):
                            E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "U",
                                                                              position_counter)
                        else:
                            entry = unknown[U_counter]
                            with template.div(klass="searchresult"):
                                with template.p():
                                    template(
                                        entry['URL'])
                                with template.a(href=entry['URL'], target="_blank", style="text-decoration: none;",
                                                onclick="url(" + str(position_counter) + ");"):
                                    with template.h2():
                                        template(
                                            entry['title'])
                                with template.p():
                                    template(
                                        entry['description'])
                            U_counter += 1
                        position_counter += 1

                    elif item == 'A':
                        # ad
                        A = ad[0]
                        if A['img_ad']:
                            with template.card(style="padding:10px;"):
                                template(
                                    "<b style=\"color:black;display:inline-block;\">Ads ?? &nbsp; </b>" + "<p style=\"display:inline-block;\">" + " " +
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
                                                    "<span>???</span><span>???</span><span>???</span><span>???</span><span>???</span>")
                                            with template.div(klass="rating-lower"):
                                                template(
                                                    "<span>???</span><span>???</span><span>???</span><span>???</span><span>???</span>")
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
                                                "<b style=\"color:black;\">Ad</b> ?? " + A['title'])

                                    with template.p():
                                        template(
                                            A['description'])
                                        with template.div(klass="rating"):
                                            rating = A['rating'] * 20
                                            with template.div(klass="rating-upper",
                                                              style=("width:" + str(rating) + "%")):
                                                template(
                                                    "<span>???</span><span>???</span><span>???</span><span>???</span><span>???</span>")
                                            with template.div(klass="rating-lower"):
                                                template(
                                                    "<span>???</span><span>???</span><span>???</span><span>???</span><span>???</span>")
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
        template("var exp_id = random_exp_id();")
        template("var second = 0;")
        template("var user_id = "";")
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
        template("    upload_action(\"click link\",link_id);")
        template("}")

        template("function ad() {")
        template("    upload_action(\"click ad\",0);")
        template("}")

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

        template("window.onbeforeunload = function (event) {")
        template("    upload_action(\"close_page\",0);")
        template("}")

        template("function upload_basic() {")
        template("    $.ajax({")
        template("        type        : 'POST',")
        template("        url         : '{% url 'Ginkgo' %}',")
        template("        data        : {")
        template("            user_id:user_id,")
        template("            exp_id:exp_id,")
        template("            action:\"basic_info\",")
        template("            window_width:window_width,")
        template("            window_height:window_height,")
        template("            test_url:\"{% url 'Ginkgo' %}\",")
        template("        },")
        template("    });")
        template("}")

        template("function upload_position(x,y) {")
        template("    $.ajax({")
        template("        type        : 'POST',")
        template("        url         : '{% url 'Ginkgo' %}',")
        template("        data        : {")
        template("            user_id:user_id,")
        template("            exp_id:exp_id,")
        template("            action:\"mouse_move\",")
        template("            x:x,")
        template("            y:y,")
        template("        },")
        template("    });")
        template("}")

        template("function upload_action(type,link_id) {")
        template("    $.ajax({")
        template("        type        : 'POST',")
        template("        url         : '{% url 'Ginkgo' %}',")
        template("        data        : {")
        template("            user_id:user_id,")
        template("            exp_id:exp_id,")
        template("            link_id:link_id,")
        template("            time:second,")
        template("            action:type,")
        template("        },")
        template("    });")
        template("}")

        template("function upload_view(view) {")
        template("    $.ajax({")
        template("        type        : 'POST',")
        template("        url         : '{% url 'Ginkgo' %}',")
        template("        data        : {")
        template("            user_id:user_id,")
        template("            exp_id:exp_id,")
        template("            view:view,")
        template("            action:\"view\",")
        template("        },")
        template("    });")
        template(" }")

        template("function random_exp_id() {")
        template("    var t = \"ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678\",")
        template("    a = t.length,")
        template("    id = "";")
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
with open('search_example.html', 'w', encoding='utf-8') as f:
    f.write(str(html))
