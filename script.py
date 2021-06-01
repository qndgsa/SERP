from airium import Airium

template = Airium()

template('<!DOCTYPE html>')
with template.html(lang="pl"):
    #create header and load css
    with template.head():
        template.meta(charset="utf-8")
        template.title(_t="example")
        template.link(rel="stylesheet",href="css/style.css")
        template.link(href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",rel="stylesheet",integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN",crossorigin="anonymous")

    #create body
    with template.body():
        #create nav bar
        with template.nav(klass="header"):
            with template.div(klass="col-xs-8"):
                with template.ul():
                    #element in nav bar
                    with template.li():
                        template(
                            "<li><a href=\"\#\"><i class=\"fa fa-2x fa-user-circle-o\" aria-hidden=\"true\"></i></a></li>")
                        template(
                            "<li><a href=\"\#\"><i class=\"fa fa-2x fa-bell\" aria-hidden=\"true\"></i></a></li>")
                        template(
                            "<li><a href=\"\#\"><i class=\"fa fa-2x fa-bars\" aria-hidden=\"true\"></i></a></li>")
                        template(
                            "<li><a href=\"\#\">Images</a></li>")
                        template(
                            "<li><a href=\"\#\">Mail</a></li>")
        #create search bar
        with template.div(klass="logo"):
            template.img(src="img/google.jpg", height="85px", width="250px", alt="logo", title="logo")
        with template.div(klass="logo"):
            template("<input type=\"text\" name=\"searchBar\" id=\"searchbar\" placeholder=\"Search\">")
            template("<input type=\"button\" value=\"Google Search\" id=\"search_button\">")
        # create footer
        with template.div( klass="footer"):
            template("<a href=\"#\">Advertising</a><a href=\"#\">Business</a><a href=\"#\">About</a>")

#load as html
html = str(template) # casting to string extracts the value

#output html file
with open('example.html', 'w') as f:
    f.write(str(html))
