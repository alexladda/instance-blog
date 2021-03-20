from flask import Flask, redirect, url_for, render_template
from flaskext.markdown import Markdown
app = Flask(__name__)
Markdown(app)

@app.route('/')
def home():
    return render_template("home.html", pages=["page1", "page2", "page3"])

@app.route('/pages/')
def pages():
    return 'here are pages'

@app.route('/pages/architecture')
def architecture():
    return render_template("architecture.md")

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
    app.run()
