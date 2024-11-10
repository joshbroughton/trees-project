from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    #dummy data for testing front end
    tree = {
            '0': [[['jackie', 'jim']]],
            '1': [[['bob'], ['jill'], ['jimmy']]],
            '2': [[['bob'], ['jackie']], [['jane', 'jill'], ['jim']], [['jimmy'], ['joe', 'rick']]]
        }
    return render_template('index.html', tree=tree)

@app.route('/update_tree', methods=['POST'])
def update_tree():
    command = request.form.get('command')
    #parse command, update tree, and return updated tree
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)