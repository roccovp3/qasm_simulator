from flask import Flask, render_template, request, send_file
import compute
import os
import matplotlib.pyplot as plt
import math

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

#app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route("/", methods=('GET', 'POST'))
def index():
    output = ''
    code = ''

    if request.method == 'POST':
        code = request.form['code']
    if request.method == 'POST' and request.form['button'] == "Calculate":
        try:
            output = compute.compute(int(request.form['shots']), request.form['code'])
        except ValueError:
            output = compute.compute(1024, request.form['code'])
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
    graphStateVector()
    return render_template("index.html", body=output, code=code)


def graphStateVector():
    # creating the dataset
    states = [('{0:0'+str(int(math.log2(len(compute.statevector))))+'b}').format(x) for x in range(len(compute.statevector))]
    fig = plt.figure(figsize=(16, 3))
    displayvector = [None]*len(compute.statevector)
    for i, x in enumerate(compute.statevector):
        displayvector[i] = compute.statevector[int((('{0:0'+str(int(math.log2(len(compute.statevector))))+'b}').format(i))[::-1],2)]
    # creating the bar plot
    plt.bar(states, [abs(x) for x in displayvector], color='blue', width=0.9)
    plt.tick_params(axis='x', which='major', labelsize=12, rotation=45)
    plt.xticks(ha="right")
    plt.xlabel("Computational Basis States")
    plt.ylabel("Amplitude")
    plt.ylim(0,1)
    plt.tight_layout(pad=2)
    plt.title("Statevector")
    plt.savefig("static/statevector.png")


if __name__ == "__main__":
    app.run()
