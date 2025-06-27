from flask import Flask, render_template, request
import locale
import os

app = Flask(__name__)

# Set locale for currency formatting (US)
locale.setlocale(locale.LC_ALL, '')

@app.route("/", methods=["GET", "POST"])
def index():
    total = None
    interest = None

    if request.method == "POST":
        try:
            principal = float(request.form.get("principal", ""))
            rate = float(request.form.get("rate", ""))
            term = int(request.form.get("term", ""))
            compound = int(request.form.get("compound", ""))

            if all(val > 0 for val in [principal, rate, term, compound]):
                total_value = principal * (1 + rate / compound) ** (compound * term)
                interest_value = total_value - principal
                total = "${:,.2f}".format(total_value)
                interest = "${:,.2f}".format(interest_value)
        except (ValueError, ZeroDivisionError):
            # Invalid form values or division by zero
            total = interest = None

    return render_template("index.html", total=total, interest=interest)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
