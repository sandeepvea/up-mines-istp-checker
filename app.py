from flask import Flask, render_template, request
import requests
import re
import time

app = Flask(__name__)

MAX_IDS = 50
TIMEOUT = 15

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = ""

    if request.method == "POST":
        try:
            start_id = int(request.form.get("start_id", "0"))
            end_id = int(request.form.get("end_id", "0"))
            destinations = [
                x.strip().upper()
                for x in request.form.get("destinations", "").split(",")
                if x.strip()
            ]

            if start_id <= 0 or end_id < start_id:
                raise ValueError("Valid start aur end eID bharo.")

            if end_id - start_id + 1 > MAX_IDS:
                raise ValueError("Ek baar mein maximum 50 eID check kar sakte ho.")

            if len(destinations) > 10:
                raise ValueError("Maximum 10 destinations allowed.")

            error = (
                "Official UP Mines ISTP PDF endpoint aur uska "
                "response format verify karna abhi baaki hai. "
                "Bina verified source ke records ka result nahi banaya jayega."
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        results=results,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
