# Launch with
#
#gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --error-logfile error.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    #return render_template('articles.html', articles = articles[1:])
    return render_template('articles.html', articles = articles)

@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    fname = [a[0] for a in articles]
    f = topic+'/'+filename
    current = articles[fname.index(f)]
    recommend = recommended(current, articles, 5)
    text = current[2]
    lines = text.splitlines()

    return render_template('article.html', current = current, recommend = recommend, lines = lines)

#initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
articles = load_articles(articles_dirname, gloves)