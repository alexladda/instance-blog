from flask import Flask, render_template, Response

import base64
from io import BytesIO, StringIO
from matplotlib.figure import Figure

app = Flask(__name__)


def plot():
    """
    generate a generic figure for testing
    """
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 1, 2, 3, 5, 8, 13, 21, 34])
    return fig


def hellopng(fig):
    """
    returns an <img> tag with inline png
    """
    # creating a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def hellosvg64(fig):
    """
    returns an <img> tag with inline svg (b64)
    """
    # creating a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="svg")
    # Return the svg as a string.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/svg+xml;base64,{data}'/>"


def hellosvg(fig):
    """
    returns an string with svg definitions
    """
    # creating a temporary buffer.
    buf = StringIO()
    fig.savefig(buf, format="svg")
    # Return the svg as a string.
    svg = buf.getvalue()
    # cut away the xml bit
    svg = '<svg' + svg.split('<svg')[1]
    return svg


@app.route("/helloworld")
def helloworld():
    png = hellopng(plot())
    svg64 = hellosvg64(plot())
    svg = hellosvg(plot())
    return render_template('hellosvg.html',
                           png=png,
                           svg64=svg64,
                           svg=svg)


@app.route("/plot.svg")
def plotsvg():
    fig = plot()
    buf = StringIO()
    fig.savefig(buf, format="svg")
    svg = buf.getvalue()
    svg = '<svg' + svg.split('<svg')[1]
    # Return the svg as a string.
    # data = base64.b64encode(buf.getbuffer())
    return Response(svg, mimetype='image/svg+xml')


@app.route("/plot.png")
def plotpng():
    fig = plot()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    figdata_png = buf.getvalue()
    # Return the svg as a string.
    # data = base64.b64encode(buf.getbuffer())
    return Response(figdata_png, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
