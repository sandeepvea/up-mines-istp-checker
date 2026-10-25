
from flask import Flask, render_template, request, Response
import csv
import io

app = Flask(__name__)

MAX_IDS = 50

FIELDS = [
    "eID",
    "ISTP No.",
    "Origin Transit Pass No.",
    "Origin Transit Pass Generation Date",
    "Destination District",
    "Mineral",
    "Quantity",
]

@app.route("/", methods=["GET", "POST"])
@app.route("/check", methods=["GET", "POST"])
def index():
    results = []
    error = ""

    if request.method == "POST":
        try:
            start_id = int(request.form.get("start_id", "0"))
            end_id = int(request.form.get("end_id", "0"))

            destinations = [
                item.strip().upper()
                for item in request.form.get(
                    "destinations", ""
                ).split(",")
                if item.strip()
            ]

            if start_id <= 0 or end_id < start_id:
                raise ValueError("Valid start aur end eID bharo.")

            if end_id - start_id + 1 > MAX_IDS:
                raise ValueError(
                    "Ek batch mein maximum 50 IDs allowed hain."
                )

            if not destinations or len(destinations) > 10:
                raise ValueError(
                    "1 se 10 destinations comma se alag likho."
                )

            error = (
                "Form sahi submit hua. Actual ISTP PDF fetching "
                "aur field extraction abhi configure karni hai."
            )

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return render_template(
        "index.html",
        results=results,
        error=error,
        fields=FIELDS,
    )


@app.route("/export.csv", methods=["POST"])
def export_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    writer.writeheader()

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=istp_results.csv"
        },
    )


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
