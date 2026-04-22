from flask import Flask, render_template, request, make_response
from io import StringIO
import csv
from utils import get_keywords

app = Flask(__name__, template_folder='.')

@app.route('/styles.css')
def styles():
    with open('styles.css', 'r', encoding='utf-8') as css_file:
        response = make_response(css_file.read())
        response.headers['Content-Type'] = 'text/css'
        return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seed_keyword = request.form.get('seed_keyword', '').strip()
        if not seed_keyword:
            return render_template('index.html', keywords=None, seed_keyword='', error='Please enter a seed keyword.')
        keywords_data = get_keywords(seed_keyword)
        return render_template('index.html', keywords=keywords_data, seed_keyword=seed_keyword, error=None)

    return render_template('index.html', keywords=None, seed_keyword='', error=None)

@app.route('/download', methods=['POST'])
def download():
    seed_keyword = request.form.get('seed_keyword', '').strip()
    keywords_data = get_keywords(seed_keyword)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=['keyword', 'volume', 'competition', 'intent', 'difficulty'])
    writer.writeheader()
    writer.writerows(keywords_data)

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={seed_keyword or "keywords"}-research.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

if __name__ == '__main__':
    app.run(debug=True)
