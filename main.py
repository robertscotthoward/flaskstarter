'''

'''

import os
import sys
import requests
from flask import Flask, jsonify, render_template, abort, request
#from flask_cors import CORS

root = os.path.dirname(__file__)
webFolder = '.'
staticFolder = os.path.join(root, 'static')
templatesFolder = os.path.join(root, 'templates')

app = Flask(__name__, static_folder=staticFolder,)
#CORS(app)  # Enable CORS for all routes


def readFile(fn):
  with open(fn) as f:
    return f.read()


def search_books(query):
  if not query:
    return []
  url = f"https://www.googleapis.com/books/v1/volumes?q=${query}"
  response = requests.get(url)
  data = response.json()
  for item in data['items']:
    vo = item.get('volumeInfo', {})
    identifiers = vo.get('industryIdentifiers', [])
    isbn_10 = next((identifier.get('identifier') for identifier in identifiers if identifier.get('type') == 'ISBN_10'), None)
    isbn_13 = next((identifier.get('identifier') for identifier in identifiers if identifier.get('type') == 'ISBN_13'), None)

    book = {
      "id": vo.get('id'),
      "title": vo.get('title'),
      "authors": vo.get('authors', []) or [],
      "categories": vo.get('categories', []) or [],
      "publisher": vo.get('publisher'),
      "year": vo.get('publishedDate'),
      "description": vo.get('description'),
      "image": vo.get('imageLinks', {}).get('thumbnail', ''),
      "ISBN10": isbn_10,
      "ISBN13": isbn_13
    }
    book['keywords'] = book['title'] + ' '.join(book['authors'])
    yield book



@app.route('/api/books/<search>', methods=['GET'])
def api_get_books(search):
  return jsonify([book for book in search_books(search)])


@app.route('/books', methods=['GET'])
def get_books():
  search = request.args.get('search')
  print(f"search: {search}")
  books = list(search_books(search))
  model = {
    'search': search or '',
    'books': books
  }
  for book in books:
    print(book['title'], book['authors'])
  return render_template('books.html', model=model)


# Define a catch all route that will return the index.html, and defer to the static folder otherwise
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
  if not path:
    path = 'index.html'
  fp = os.path.join(staticFolder, path)
  if fp.endswith('.html'):
    return render_template(path)
  if not os.path.isfile(fp):
    abort(404)
  return app.send_static_file(path)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
