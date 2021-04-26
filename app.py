from flask import Flask, redirect, url_for, render_template, abort, Response
from flaskext.markdown import Markdown
import pathlib
import os
from flask import send_from_directory
from matplotlib.figure import Figure
import random
from htmlmin.minify import html_minify
from csscompressor import compress
from jsmin import jsmin

# from flask_minify import minify

import include.weather_station as ws

app = Flask(__name__)
md = Markdown(app, safe_mode=True)
# minify(app=app, html=True, js=True, cssless=True)

# TODO: pass navigation differently (see code repetitions)
# TODO: footer for all pages


def get_content(category):
    '''
    collects all content from the respective directory into one list
    '''
    # define the path
    content_directory = pathlib.Path(category)
    # define the pattern
    content_pattern = "*.md"
    # initiate empty list variable
    content_list = []
    for content in content_directory.glob(content_pattern):
        content_list.append(content.stem)
    content_list.sort()
    # removing entry for __archive.md
    content_list.pop(0)
    return content_list


@app.context_processor
def utility_processor():
    # inline CSS and Javascript
    def get_css():
        """
        collects all styles from the static directory into one string
        """
        styles = ["normalize.css",
                  "milligram.css",
                  "main.css",
                  "nav.css",
                  "socialicons.css"]
        css = ""
        for file in styles:
            path = "static/" + file
            with open(path) as f:
                css = css + f.read()
        css = compress(css)
        return css

    def get_js():
        """
        collects all scripts from the static directory into one string
        """
        scripts = ["nav.js", "shynet.js"]
        js = ""
        for file in scripts:
            path = "static/" + file
            with open(path) as f:
                js = js + f.read()
        js = jsmin(js)
        return js

    def get_nav(folder):
        nav = get_content(folder)
        return nav

    def get_footer():
        # TODO
        pass

    return dict(get_css=get_css,
                get_js=get_js,
                get_nav=get_nav,
                get_footer=get_footer)


def get_elements():
    """
    gets reocurring elements: list of pages and projects (for navigation)
    and returns them in a dictionary.
    """
    # TODO: footer
    pages = get_content("pages")
    projects = get_content("projects")
    elements = {'pages': pages,
                'projects': projects}
    return elements


def get_markup(folder, file):
    """
    fetches the whole contents of the .md file and returns as a string
    """
    path = folder + file + ".md"
    file = pathlib.Path(path)

    if file.exists():
        with open(path) as f:
            markup = f.read()
            return markup
    else:
        abort(404)


@app.route('/plots/<plot>.svg')
def plot_svg(plot):
    svg = ws.plot_temp(ws.query_db())
    return Response(svg, mimetype='image/svg+xml')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt',
                               mimetype='text/plain')


@app.route('/')
def home():
    rendered_html = render_template("home.html")
    return html_minify(rendered_html)


@app.route('/<page>/')
def page(page):
    path = "pages/" + page + ".md"
    file = pathlib.Path(path)
    if file.exists():
        with open(path) as f:
            markup = f.read()
        return render_template("page.html",
                               page_body=markup,
                               page_title=page)
    else:
        abort(404)


@app.route('/projects/')
def projects_archive():
    # TODO: Archive page to aggregate all Projects
    markup = get_markup('projects/', '__archive')
    return render_template("page.html",
                           page_body=markup,
                           page_title='projects')


@app.route('/projects/<project>/')
def projects(project):
    path = "projects/" + project + ".md"
    file = pathlib.Path(path)
    if file.exists():
        with open(path) as f:
            markup = f.read()
        return render_template("page.html",
                               page_body=markup,
                               page_title=project)
    else:
        abort(404)


# @app.route('/search/<search_query>')
# def search(search_query):
#     # FEATURE: add site search
#     # TODO: everything
#     elements = get_elements()
#     content = 'Looks like you were looking for <em>{}</em>.'.format(search_query)
#     return render_template("search.html",
#                            content=content,
#                            list=['dummy', 'dummy', 'dummy'],
#                            page_title='site search',
#                            nav_pages=elements['pages'],
#                            nav_projects=elements['projects'])


# @ app.route("/confidential/")
# def confidential():
#     # FEATURE: add confindential content
#     # TODO: everything
#     return redirect(url_for("search", search_query="confidential"))


@ app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    elements = get_elements()
    return render_template('404.html',
                           page_title='404',
                           nav_pages=elements['pages'],
                           nav_projects=elements['projects']), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
