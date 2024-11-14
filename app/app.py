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
    query_result = request.args.to_dict(flat=False).get('query_result')
    order = request.args.get('order')
    if isinstance(tree, BPlusTree):
        tree_json = tree.to_json()
    else:
        tree_json = {}
    return render_template('index.html', tree_json=tree_json, query_result=query_result, order=order)

@app.route('/update_tree', methods=['POST'])
def update_tree():
    global tree
    global primary_key
    query_result = None
    command = request.form.get('command')
    order = request.form.get('order')
    command = command.lower().split(' ')

    if len(command) < 2:
        flash('Invalid command, please check your syntax and try again', 'error')
        return redirect(url_for('index'))
    if command[1].isdigit():
        command[1] = int(command[1])
    if len(command) > 2 and command[2].isdigit():
        command[2] = int(command[2])
    match command[0]:
        case 'insert':
            if tree is None:
                tree = BPlusTree(int(order), primary_key, command[1])
                primary_key += 1
            else:
                tree.insert(command[1], primary_key)
                primary_key += 1
        case 'delete':
            result = tree.delete(command[1])
            if result is None:
                flash('Value not found in tree', 'error')
        case 'select':
            if len(command) < 2:
                flash('Invalid command, please check your syntax and try again', 'error')
                return redirect(url_for('index'))
            if command[1] == '=':
                query_result = tree.search(command[2])
            elif command[1] == 'between':
                if command[2].isdigit():
                    query_result = tree.search_range(int(command[2]), int(command[4]))
                else:
                    query_result = tree.search_range(command[2], command[4])
            if query_result is None:
                flash('Value not found in tree', 'error')
        case _:
            flash('Invalid command, please check your syntax and try again', 'error')
    #parse command, update tree, and return updated tree
    return redirect(url_for('index', query_result=query_result, order=order))

@app.route('/reset_tree', methods=['POST'])
def reset_tree():
    global tree
    global primary_key
    tree = None
    primary_key = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
