from flask import Flask, render_template, request, send_file
import compute
import os
import matplotlib.pyplot as plt


TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

#app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route("/", methods=('GET', 'POST'))
def index():
    output = ''
    code = ''
    graphStateVector()
    if request.method == 'POST':
        code = request.form['code']
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
    print(STATIC_DIR)
    return render_template("index.html", body=output, code=code)


def graphStateVector():
    # creating the dataset
    states = range(len(compute.statevector)+1)
    print(compute.statevector)
    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(states, compute.statevector, color='blue', width=0.4)

    plt.xlabel("Computational Basis States")
    plt.ylabel("Amplitude")
    plt.title("Statevector")
    plt.savefig("statevector.png")


if __name__ == "__main__":
    app.run()
