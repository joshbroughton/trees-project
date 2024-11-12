from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
from tree.b_plus_tree import BPlusTree
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

tree = None
primary_key = 0

@app.route('/')
def index():
    global tree
    global primary_key
    if isinstance(tree, BPlusTree):
        tree_json = tree.to_json()
        print(tree_json)
    else:
        tree_json = {}
    return render_template('index.html', tree_json=tree_json)

@app.route('/update_tree', methods=['POST'])
def update_tree():
    global tree
    global primary_key
    command = request.form.get('command')
    command = command.lower().split(' ')
    if len(command) < 2:
        flash('Invalid command, please check your syntax and try again', 'error')
        return redirect(url_for('index'))
    if command[1] and command[1].isdigit():
        command[1] = int(command[1])
    match command[0]:
        case 'insert':
            if tree is None:
                tree = BPlusTree(1, primary_key, command[1])
                primary_key += 1
            else:
                tree.insert(command[1], primary_key)
                primary_key += 1
        case 'delete':
            result = tree.delete(command[1])
            if result is None:
                flash('Value not found in tree', 'error')
        case 'select':
            print('select')
        case _:
            print('test')
            flash('Invalid command, please check your syntax and try again', 'error')
    #parse command, update tree, and return updated tree
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
