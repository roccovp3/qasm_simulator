from flask import Flask, render_template, request, send_file
import compute
import os
import webbrowser


TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

#app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
@app.route("/", methods=('GET', 'POST'))
def index():
    output = ''
    code = ''
    if request.method == 'POST' and request.form['button'] == "Calculate":
        output = compute.compute(int(request.form['shots']), request.form['code'])
    elif request.method == 'POST' and request.form['button'] == "Export":
        file = open('export.qasm', 'w+', newline='')
        file.write(request.form['code'])
        file.close()
        return send_file('export.qasm')
    elif request.method == 'POST' and request.form['button'] == "Import":
        file = request.files['file']
        file.save(file.filename)
        file = open(file.filename)
        code = file.read()
    #if code == '': bad request from this...
        #code = request.form['code']
    print(STATIC_DIR)
    parseCompute(output)
    return render_template("index.html", body=output, code=code)

def parseCompute(output):
    return


if __name__ == "__main__":
    app.run()
