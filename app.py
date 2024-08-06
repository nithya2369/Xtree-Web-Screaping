from flask import Flask, request, render_template, send_file
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    tag = request.form['tag']
    class_name = request.form['class_name']
    file_name = request.form['file_name']

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if class_name:
        data = soup.find_all(tag, class_=class_name)
    else:
        data = soup.find_all(tag)

    extracted_data = [item.get_text(strip=True) for item in data]

    df = pd.DataFrame(extracted_data, columns=['Data'])
    csv_path = f"{file_name}.csv"
    df.to_csv(csv_path, index=False)

    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

