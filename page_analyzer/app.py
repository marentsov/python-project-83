import os
import requests
import psycopg2

from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for

from page_analyzer.parser import get_data
from page_analyzer.url_validator import normalize_url
from page_analyzer.url_validator import validate_url
from page_analyzer.data_base import UrlRepository

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template(
        'index.html',
    )


@app.route('/urls', methods=['POST'])
def urls_index():
    url = request.form.to_dict()
    normalized_url = normalize_url(url['url'])

    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_url(normalized_url)
    if url_info is not None:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=url_info.get('id')))
    id = repo.add_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=id))


@app.route('/urls/<int:id>')
def get_url(id):
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_id(id)

    if not url_info:
        return 'OOPS', 404

    return render_template(
        'url.html',
        url_info=url_info
    )

@app.route('/urls', methods=['GET'])
def get_urls():
    repo = UrlRepository(DATABASE_URL)
    urls_info = repo.get_all_urls()
    return render_template(
        'urls.html',
        urls_info=urls_info,
    )




