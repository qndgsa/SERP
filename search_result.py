import json
import sys

from airium import Airium

template = Airium()

# data config
entry_file = "data.json"
ad_file = "1.json"

sequence = "EEEAE"  # the sequence determine the display order of entries by category
                    # "E" = effective, "I" = ineffective, "U" = unknown, "A" = Ad
                    # if gave number of the assigned category is more than entry_file's, program will replace
                    # them with other category in E,I,U order until run out all entries.

fill = True  # when set it as True, if the length is lower than total number of the entries, program will fill up
             # the rest of entries in the html file

# load dataset
try:
    with open(entry_file, 'rb') as f:
        data = json.load(f)
    effective = data[0]['effective']
    ineffective = data[0]['ineffective']
    unknown = data[0]['unknown']

# entry file exception
except IOError:
    print("Could not load entry file:", entry_file)
    sys.exit(1)

try:
    with open(ad_file, 'rb') as d:
        ad = json.load(d)
    ad_loaded = True
# Ad file exception
except IOError:
    ad_loaded = False
    print("Ad file not loaded:", ad_file)


# Handle exceptions
def entry_exception(E_counter, I_counter, U_counter, exception_pos):
    if exception_pos != "E" and E_counter != len(effective):
        entry = effective[E_counter]
        with template.div(klass="searchresult"):
            with template.a():
                template(
                    entry['URL'])
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
                template.img(id="searchbarimage", src="images/icon.png")
                # create search bar
                with template.div(id="searchbar", type="text"):
                    template("<input id=\"searchbartext\" type=\"text\" value=")
                    template("\"" + data[0]['query'] + "\"")
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
                for item in sequence:
                    if item == 'E':
                        if E_counter >= len(effective):
                            E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "E")
                        else:
                            entry = effective[E_counter]
                            with template.div(klass="searchresult"):
                                with template.a():
                                    template(
                                        entry['URL'])
                                with template.h2():
                                    template(
                                        entry['title'])
                                with template.p():
                                    template(
                                        entry['description'])
                            E_counter += 1

                    if item == 'I':
                        if I_counter >= len(ineffective):
                            entry_exception()
                        else:
                            entry = ineffective[I_counter]
                            with template.div(klass="searchresult"):
                                with template.a():
                                    template(
                                        entry['URL'])
                                with template.h2():
                                    template(
                                        entry['title'])
                                with template.p():
                                    template(
                                        entry['description'])
                            I_counter += 1
                    if item == 'U':
                        if U_counter >= len(unknown):
                            entry_exception()
                        else:
                            entry = unknown[U_counter]
                            with template.div(klass="searchresult"):
                                with template.a():
                                    template(
                                        entry['URL'])
                                with template.h2():
                                    template(
                                        entry['title'])
                                with template.p():
                                    template(
                                        entry['description'])
                            U_counter += 1
                    if item == 'A':
                        # ad
                        if ad_loaded:
                            with template.div(klass="searchresult"):
                                with template.a():
                                    template(
                                        ad['URL'])
                                with template.h2():
                                    template(
                                        "<b style=\"color:black\">Ad</b> " + ad['title'])

                                with template.p():
                                    template(
                                        ad['description'])
                                    with template.div(klass="rating"):
                                        rating = ad['rating'] * 20
                                        with template.div(klass="rating-upper", style=("width:" + str(rating) + "%")):
                                            template(
                                                "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                                        with template.div(klass="rating-lower"):
                                            template(
                                                "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                                        with template.div(klass="rating-comment"):
                                            with template.p():
                                                template(
                                                    ad['rating comment'])
                if len(sequence) < (len(effective) + len(ineffective) + len(unknown)+1) and fill == True:
                    fill_up = (len(effective) + len(ineffective) + len(unknown)+1) - len(sequence)
                    for i in range(0,fill_up):
                        E_counter, I_counter, U_counter = entry_exception(E_counter, I_counter, U_counter, "")

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
