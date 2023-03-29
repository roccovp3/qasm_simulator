from flask import Flask, render_template, request
import compute
import os


TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app = Flask(__name__)
@app.route("/", methods=('GET', 'POST'))
def index():
    output = compute.compute(int(request.form['shots']))
    print(STATIC_DIR)
    parseCompute(output)
    return render_template("index.html", body=output)

def parseCompute(output):
    return


if __name__ == "__main__":
    app.run()
