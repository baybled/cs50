import os
import html
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")


@app.route("/articles")
def articles():
    """Look up articles for geo"""

    # Get geo from url, usually arrived to by GET request
    geo = request.args.get("geo")

    # Return list of found articles
    found = lookup(geo)
      
    return jsonify(found)


@app.route("/search")
def search():
    """Search for places that match query"""

    # Escape most odd characters
    query = html.unescape(request.args.get("q"))
    escape_list = [",", "US", "USA", "us", "usa"]
    for i in range(len(escape_list)):
      query = query.replace(escape_list[i], "")

    # prepare list for jsonify
    found = []

    # Check for postal code, meaning rest of query is redundant
    for i in range(len(query)-4):
      postal = query[i] + query[i+1] + query[i+2] + query[i+3] + query[i+4]
      if postal.isnumeric():
        found = db.execute("SELECT * FROM places WHERE postal_code = :p", p=postal)
        return jsonify(found)

    # Check if query is multiple words, then check for state
    if " " in query:
      split = query.split()
      for i in split:
        if len(i) < 3:
          state = i
          query = query.replace(" " + state, "")
          found = db.execute("SELECT * FROM places WHERE admin_code1 = :a AND (admin_name1 = :q OR admin_name2 = :q OR place_name = :q)", a=state, q=query)

      # Else search admin_name1 for city, admin_name2 and place_name for query
        else:

          # Check if city was added, such as Cambridge, Massachusetts, Would be improved by checking against a word list of cities
          if len(split) > 2:
            city = split[-1] + "%"
            query = query.replace(city, "").rstrip()
            found = db.execute("SELECT * FROM places WHERE admin_name1 = :c AND (admin_name2 = :q OR place_name = :q)", c=city, q=query)

    # If singular word, search admin_name1, admin_name2 and place_name for query
    else:
      found = db.execute("SELECT * FROM places WHERE admin_name1 = :q OR admin_name2 = :q OR place_name = :q", q=query)

    return jsonify(found)


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
