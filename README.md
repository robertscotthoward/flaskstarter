# Flask-Vue Starter Template

This site creates a python Flask web site that serves up an API and a Vue3/Bootstrap5 web site from the same folder and web server. Although not optimized, it has these advantages:

* CDN references for Vue and Bootstrap used
* Node and npm is not required
* No need to build/compile the site
* No CORS configuration since both API and web are served from same site

Purpose: teaching high school students

Requirements:

* Python 3; e.g. 3.11 in this case

# Description

This web site has a page that allows you to search books online. It uses the Google API

Example: https://www.googleapis.com/books/v1/volumes?q=alaskan%20wolves

# Usage

```
cd SOMEFOLDER
git clone https://github.com/robertscotthoward/flaskvue.git
cd flaskvue
python main.py
```

Open http://127.0.0.1:5001 in browser