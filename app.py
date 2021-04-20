from flask import Flask, redirect, url_for, render_template
from flaskext.markdown import Markdown
# from flask_minify import minify
import pathlib
import os
from flask import send_from_directory

app = Flask(__name__)
md = Markdown(app, safe_mode=True)
# minify(app=app, html=True, js=True, cssless=True)

# TODO: pass navigation as decorator (see code repetitions)
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
    # removing __archive.md entry
    content_list.pop(0)
    return content_list


# inline CSS and Javascript
def get_css():
    '''
    collects all styles from the static directory into one string
    '''
    styles = ["normalize.css", "milligram.css", "main.css", "nav.css"]
    css = ""
    for style in styles:
        path = "static/" + style
        with open(path) as f:
            css = css + f.read()
    return css


def get_elements():
    """
    gets reocurring elements: list of pages and projects (for navigation), css,
    js and returns them in a dictionary.
    """
    # TODO: footer
    pages = get_content("pages")
    projects = get_content("projects")
    css = get_css()
    elements = {'pages': pages,
                'projects': projects,
                'css': css}
    return elements


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    # passing all pages to render navigation in base.html
    elements = get_elements()
    return render_template("home.html",
                           nav_pages=elements['pages'],
                           nav_projects=elements['projects'],
                           css=elements['css'])


@app.route('/<page>')
def page(page):
    path = "pages/" + page + ".md"
    file = pathlib.Path(path)
    # passing all pages and projects to render navigation in base.html
    elements = get_elements()
    if file.exists():
        with open(path) as f:
            markup = f.read()
        return render_template("page.html",
                               page_body=markup,
                               page_title=page,
                               nav_pages=elements['pages'],
                               nav_projects=elements['projects'],
                               css=elements['css'])
    else:
        return redirect(url_for("search", search_query=page))


@app.route('/projects/')
def projects():
    # passing all pages and projects to render navigation in base.html
    # TODO: Archive page to aggregate all Projects
    elements = get_elements()
    markup = "TODO: Archive page to aggregate all Projects"
    return render_template("page.html",
                           page_body=markup,
                           page_title=project,
                           nav_pages=elements['pages'],
                           nav_projects=elements['projects'],
                           css=elements['css'])


@app.route('/projects/<project>')
def project(project):
    path = "projects/" + project + ".md"
    file = pathlib.Path(path)
    # passing all pages and projects to render navigation in base.html
    if file.exists():
        with open(path) as f:
            markup = f.read()
        return render_template("page.html",
                               page_body=markup,
                               page_title=project,
                               nav_pages=elements['pages'],
                               nav_projects=elements['projects'],
                               css=elements['css'])
    else:
        return redirect(url_for("search", search_query=page))


@app.route('/<search_query>')
def search(search_query):
    # FEATURE: add site search
    # TODO: everything
    return render_template("search.html", content=search_query)


@app.route("/confidential")
def confidential():
    # FEATURE: add confindential content
    # TODO: everything
    return redirect(url_for("search", search_query="confidential"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
