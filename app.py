from flask import Flask, redirect, url_for, render_template
from flaskext.markdown import Markdown
import pathlib

app = Flask(__name__)
Markdown(app)

def get_pages():
    # collects all pages from the pages directory into one list
    pages_directory = pathlib.Path('pages') # define the path
    pages_pattern = "*.md"                  # define the pattern
    list=[]                                 # initiate empty list variable
    for page in pages_directory.glob(pages_pattern):
        list.append(page.stem)
    return list


@app.route('/')
def home():
    pages = get_pages()                     # passing all pages to render navigation in base.html
    return render_template("home.html", nav_pages=pages)

@app.route('/pages/<page>')
def pages(page):
    path = "pages/" + page + ".md"
    file = pathlib.Path(path)
    pages = get_pages()                     # passing all pages to render navigation in base.html
    if file.exists() :
        with open(path) as f:
            page_markup = f.read()
        return render_template("page.html", page_body=page_markup, page_title=page, nav_pages=pages)
    else :
        return redirect(url_for("search", search_query=page))

@app.route('/projects/')
def projects():
    return 'here are projects'

@app.route('/about/')
def about():
    return 'about'

@app.route('/<search_query>')
def search(search_query):
    return render_template("search.html", content=search_query)

@app.route("/confidential")
def confidential():
    #FEATURE: add confindential content
    #TODO: this ends in a redirect loop
    return redirect(url_for("search", search_query="confidential"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
