from flask import Flask, redirect, url_for, render_template
from flaskext.markdown import Markdown
# from flask_minify import minify
import pathlib

app = Flask(__name__)
Markdown(app, safe_mode=True)
# minify(app=app, html=True, js=True, cssless=True)


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
    return content_list


# def get_css():
#     '''
#     collects all styles from the static directory into one string
#     '''
#     styles = ["main.css", "nav.css", "normalize.css"]
#     css = ""
#     for style in styles:
#         path = "static/" + style
#         with open(path) as f:
#             css = css + f.read()
#     return css


@ app.route('/')
def home():
    # passing all pages to render navigation in base.html
    pages = get_content("pages")
    projects = get_content("projects")
    return render_template("home.html",
                           nav_pages=pages,
                           nav_projects=projects)


@ app.route('/about/<page>')
def pages(page):
    path = "pages/" + page + ".md"
    file = pathlib.Path(path)
    # passing all pages and projects to render navigation in base.html
    pages = get_content("pages")
    projects = get_content("projects")
    if file.exists():
        with open(path) as f:
            markup = f.read()
        return render_template("page.html",
                               page_body=markup,
                               page_title=page,
                               nav_pages=pages,
                               nav_projects=projects)
    else:
        return redirect(url_for("search", search_query=page))


@ app.route('/projects/<project>')
def projects(project):
    path = "projects/" + project + ".md"
    file = pathlib.Path(path)
    # passing all pages and projects to render navigation in base.html
    pages = get_content("pages")
    projects = get_content("projects")
    if file.exists():
        with open(path) as f:
            markup = f.read()
        return render_template("page.html",
                               page_body=markup,
                               page_title=project,
                               nav_pages=pages,
                               nav_projects=projects)
    else:
        return redirect(url_for("search", search_query=page))


@ app.route('/about/')
def about():
    return 'about'


@ app.route('/<search_query>')
def search(search_query):
    return render_template("search.html", content=search_query)


@ app.route("/confidential")
def confidential():
    # FEATURE: add confindential content
    # TODO: this ends in a redirect loop
    return redirect(url_for("search", search_query="confidential"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
