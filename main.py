from flask import Flask, render_template, request

import baza
import hh_rest
from hh_rest import parse

from baza import query
from Alchemy import init, search, search_history
app = Flask(__name__)

history = dict()
@app.route("/")
def index():
    #
    main_data = {
        'a': 'A',
        'b': 'B',
        'c': 'C'
    }

    context = {
        'name': 'Mary',
        'age': 18
    }

    return render_template('main_page.html', main_data=main_data, **context)
    # return render_template('index.html', main_data=main_data, name='Leo', age=99)

@app.route('/contacts/')
def contacts():
    # где то взяли данные
    developer_name = ['M - Мася(человек)', 'V - Very nice kitty Нюся', 'C - cat Бося']
    # Контекст name=developer_name - те данные, которые мы передаем из view в шаблон
    # context = {'name': developer_name}
    # Словарь контекста context
    # return render_template('contacts.html', context=context)
    return render_template('contacts.html', name=developer_name, creation_date='05.05.2022')


@app.route('/results/')
def results():
    #text = "C#"
    global history
    return render_template('results.html', data=history)


@app.route('/history/')
def s_history():

    history = search_history()
    return render_template('history.html', data=history)


@app.route('/table/')
def table():
    res=baza.query()
    return render_template('table.html', data=res)

@app.route('/HH-parser/', methods=['GET'])
def run_get():
    #text = request.form['input_text']

    return render_template('HH-parser.html' )



@app.route('/HH-parser/', methods=['POST'])
def run_post():
    # Как получить данные формы
    text = request.form['input_text']

    rez = hh_rest.parse(text)
    global history
    history = rez

    search(text)
    return render_template('results.html',data=rez)

if __name__ == "__main__":
    init()
    app.run(debug=True)