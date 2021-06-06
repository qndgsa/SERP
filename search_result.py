import json

from airium import Airium

template = Airium()

#load dataset
with open('data.json', 'rb') as f:
	data = json.load(f)
with open('ad_no_image.json', 'rb') as d:
	ad = json.load(d)

template('<!DOCTYPE html>')
with template.html(lang="pl"):
    #create header and load css
    with template.head():
        template.meta(charset="utf-8")
        template.title(_t="Google Search")
        template.link(rel="stylesheet",href="css/search_result_page.css")
        template.link(rel="shortcut icon", type="image/ico", href="images/favicon.ico")
    #create body
    with template.body():
        #create header
        with template.div(id="header"):
            with template.div(id="topbar"):
                template.img(id="searchbarimage",src="images/googlelogo_color_272x92dp.png")
                # create search bar
                with template.div(id="searchbar",type="text"):
                    template("<input id=\"searchbartext\" type=\"text\" value=")
                    template("\""+ ad['query'] +"\"")
                    template(">")
                    with template.button(id="searchbarmic"):
                        template.img(src="images/Google_mic.svg.png")
                    with template.button(id="searchbarbutton"):
                        with template.svg(focusable="false", xmlns="http://www.w3.org/2000/svg", viewBox="0 0 24 24"):
                            template(
                                "<path d=\"M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z\"></path>")
                template("<div id=\"boxesicon\"></div>")
                template("<img id=\"bellicon\" src=\"images/google_apps.png\">")
                template("<img id=\"profileimage\" src=\"images/google_account.png\">")
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

        #search result part
        with template.div(id="searchresultsarea"):
            with template.p(id="searchresultsnumber"):
                template(
                    "About x results (y seconds) ")
                data.sort(key=lambda s: s['ranking'],reverse=True)
                #10 search result, load from json file
                position = 0
                for item in data:
                    if ad['position'] == position:
                        # ad
                        with template.div(klass="searchresult"):
                            with template.h2():
                                template(
                                    ad['title'])
                            with template.a():
                                template(
                                    ad['URL'])

                            with template.p():
                                template(
                                    ad['description'])
                            with template.p():
                                template(
                                    ad['rating comment'])
                                with template.div(klass="rating"):
                                    rating = ad['rating'] * 20
                                    with template.div(klass="rating-upper", style=("width:" + str(rating) + "%")):
                                        template(
                                            "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                                    with template.div(klass="rating-lower"):
                                        template(
                                            "<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>")
                    with template.div(klass="searchresult"):
                        with template.h2():
                            template(
                                item['title'])
                        with template.a():
                            template(
                                item['URL'])

                        with template.p():
                            template(
                                item['description'])
                    position+=1


            #related
            with template.div(id="relatedsearches"):
                with template.h3():
                    template(
                        "Searches related to" + ad["query"])
                with template.div(klass="relatedlists"):
                    with template.ul(id="relatedleft"):
                            template(
                                "<li>a</li>")
                            template(
                                "<li>b</li>")
                            template(
                                "<li>c</li>")
                            template(
                                "<li>d</li>")
                    with template.ul(id="relatedright"):
                            template(
                                "<li>e</li>")
                            template(
                                "<li>f</li>")
                            template(
                                "<li>g</li>")
                            template(
                                "<li>h</li>")
            #page list bar
            with template.div(klass="pagebar"):
                with template.ul(klass="pagelist"):
                    template(
                        "<li class=\"pagelistprevious\">Previous</li>")
                    template(
                        "<li class=\"pagelistfirst\">1</li>")
                    template(
                        "<li class=\"pagelistnumber\">2</li>")
                    template(
                        "<li class=\"pagelistnumber\">3</li>")
                    template(
                        "<li class=\"pagelistnumber\">4</li>")
                    template(
                        "<li class=\"pagelistnumber\">5</li>")
                    template(
                        "<li class=\"pagelistnumber\">6</li>")
                    template(
                        "<li class=\"pagelistnumber\">7</li>")
                    template(
                        "<li class=\"pagelistnumber\">8</li>")
                    template(
                        "<li class=\"pagelistnumber\">9</li>")
                    template(
                        "<li class=\"pagelistnumber\">10</li>")
                    template(
                        "<li class=\"pagelistnext\">Next</li>")
        #create footer
        with template.div(id="footer"):
            with template.div(id="footerlocation"):
                with template.p():
                    template("Somewhere")
                with template.p():
                    template("- From your place (Location History) - Use precise location - Learn more")

            with template.ul(id="footermenu"):
                template(
                    "<li>Help</li>")
                template(
                    "<li>Send feedback</li>")
                template(
                    "<li>Privacy</li>")
                template(
                    "<li>Terms</li>")

#load as html
html = str(template) # casting to string extracts the value

#output html file
with open('search_example.html', 'w', encoding='utf-8') as f:
    f.write(str(html))