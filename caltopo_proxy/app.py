from flask import Flask, render_template, make_response, request
from flask_cors import cross_origin

import requests


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/link/<map_id>")
def network_link(map_id=None):

    response = make_response(
        render_template(
            "network_link.kml", map_id=map_id, url_root=request.url_root
        )
    )

    response.headers["Content-Type"] = "application/vnd.google-earth.kml+xml"
    response.headers["Content-Disposition"] = f"attachment; filename={map_id}.kml"

    return response


@app.route("/m/<map_id>")
@cross_origin()
def proxy_request(map_id=None):

    proxy_request = requests.get(f"https://caltopo.com/m/{map_id}?format=kml")

    response = make_response(proxy_request.text, proxy_request.status_code)

    response.headers["Content-Type"] = proxy_request.headers["Content-Type"]

    return response


if __name__ == "__main__":
    app.run()
