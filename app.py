import os
from flask import Flask, request, render_template
from service import create_db, execute_query, get_figure
from markupsafe import Markup
import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def query():
    if request.method == 'GET':
        results = get_figure()
        figJSON = results['figure']
        print(results['data'])
        data = results['data']
        return render_template('base.html', figJSON=figJSON, data=data)
    elif request.method == 'POST':
        req_query = request.form['query']
        if "moody" not in req_query.lower():
            return "Table Name is Moody"
        if "select" not in req_query.lower():
            return "You can only perform queries of type select score, grade,  from moody where condition"
        results = execute_query(request.form['query'])
        figJSON = results['figure1']
        data = results['data']
        figure2 = results['figure2']
        return render_template('index.html', figJSON=figJSON, figS=figure2, query=request.form['query'], data=data)

if __name__ == "__main__":
    if "moody.sqlite" not in os.listdir():
        create_db()
    app.run()
