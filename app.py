from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    total = interest = None
    if request.method == "POST":
        principal = float(request.form["principal"])
        rate = float(request.form["rate"])
        term = int(request.form["term"])
        compound = int(request.form["compound"])
        total = principal * (1 + rate/compound)**(compound*term)
        interest = total - principal
    return render_template("index.html", total=total, interest=interest)
    
if __name__ == "__main__":
    app.run(debug=True)
