from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
import sys

import psycopg2
from flaskr.db import connect

import json

bp = Blueprint('blog', __name__)

# index page displaying all blog posts
@bp.route('/')
def index():
    conn = None

    # checks if DB connection can be made and excepts otherwise. Check is built here since
    #index is the first page a user lands on
    try:
        # create a cursor from db file
        conn = connect()
        cur = conn.cursor()

        cur.execute('select id, ISBN, title, author, year from books')

        posts = cur.fetchmany(10)

        return render_template('index.html', posts=posts)

     # close the communication with the PostgreSQL
        #cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        flash (error)
        return render_template('404.html')

# view page - this method handles all logic for individual book pages
# receives internal book ID as parameter
@bp.route('/api/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    #connect to DB
    conn = connect()
    cur = conn.cursor()
    # grab user (mainly for reviews) and book id
    user_id = session.get('user_id')
    book_id = id

    # find the book being requested
    cur.execute(
        'SELECT id,ISBN,title,author,year FROM books WHERE id = (%s)', (id,))
    result = cur.fetchone()

    # return 404 if no book is found
    if result is None:
        flash ("Sorry but the book you are looking for is in another castle")
        return render_template('404.html')

    # fetch all reviews for this book with join between reviws and users
    cur.execute(
        'SELECT user_id, username, review_value, review_text FROM reviews join users on (reviews.user_id = users.id) WHERE book_id = (%s) and user_id != (%s)', (book_id,user_id))
    show_reviews = cur.fetchall()

    #make API call to goodreads reviews
    try:
        import requests
        book_id_goodreadsApi = str(result[1])
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "a05KtlQOvVuVdhCmDxs6g", "isbns":book_id_goodreadsApi})
        goodreadsAPI = res.json()
    except Exception as error:
        flash (error)
        goodreadsAPI = None

    # method is post only when a user submits a review
    # grab parameters from user review area
    if request.method == 'POST':
        review = request.form['review']
        if request.form['review_text'] is not None:
            review_text = request.form['review_text']
        else:
            review_text = "No description provided"

        error = None

        if not review:
            error = 'Review is required.'

        # check if this user has already left a review
        cur.execute(
            'select id,user_id,book_id from reviews where user_id = (%s) and book_id = (%s)', (user_id, book_id))
        review_check = cur.fetchone()
        if review_check is not None:
            error = 'This user has already left a review for this book'

        if error is not None:
            flash(error)

        # if above checks pass, save review and proceed
        else:
            cur.execute(
                'insert into reviews (user_id, book_id, review_value, review_text) VALUES (%s,%s,%s,%s)', (user_id,book_id,review,review_text))
            conn.commit()
            flash("Review successfully submitted")

            return render_template('blog/view.html', post=result, show_reviews=show_reviews,goodreadsAPI=goodreadsAPI)

    return render_template('blog/view.html', post=result, show_reviews=show_reviews,goodreadsAPI=goodreadsAPI)

# search driver for AJAX search
@bp.route('/search')
@login_required
def search():
    #connect to DB
    conn = connect()
    cur = conn.cursor()

    search_text = request.args['searchText'].lower() # get the text to search for
    args = ('%' +search_text+'%') # add wild cards to each side of search parameter

    cur.execute(
        'select id, ISBN, author, title from books where LOWER(ISBN) LIKE (%s) OR LOWER(author) like (%s) OR LOWER(title) like (%s)', (args,args,args))

    query_result = cur.fetchall()

    if cur.rowcount > 0:
        return (json.dumps({"results":query_result}))
    else:
        query_result = [[0, "Results Not Found", "No Results Found", " "]] #build element in results structure so JS still understands it
        return json.dumps({"results":query_result}) # sample real result: [516, "0743290119", "Lauren Weisberger", "Chasing Harry Winston"]

# JSON API Driver
@bp.route('/api/<string:id>/json', methods=('GET','POST')) # takes string ISBN as parameter
@login_required
def json_output(id):

    #connect to DB
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        'SELECT id,ISBN,title,author,year FROM books WHERE ISBN = (%s)', (id,))
    result = cur.fetchone()

    if result is None:
        flash ("Sorry but the ISBN you are looking for is in another castle")
        return render_template('404.html')

    #make API call to goodreads reviews
    try:
        import requests
        book_id_goodreadsApi = str(result[1])
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "a05KtlQOvVuVdhCmDxs6g", "isbns":book_id_goodreadsApi})
        goodreadsAPI = res.json()
    except Exception as error:
        flash (error)
        goodreadsAPI = None

    #construct JSON to return
    json_string = x = {
        "title": result[2],
        "author": result[3],
        "year": result[4],
        "isbn": result[1],
        "review_count": goodreadsAPI["books"][0]["reviews_count"],
        "average_score": goodreadsAPI["books"][0]["average_rating"]
}
    json_string = json.dumps(json_string)

    return json_string
