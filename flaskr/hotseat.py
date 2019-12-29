from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

import psycopg2
from flaskr.db import connect

import json
import random

bp = Blueprint('hotseat', __name__)

#pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

@bp.route('/play_hotseat')
def play_hotseat():
#    from playsound import playsound
    #https://www.soundjay.com/button/beep-07.wav
    return render_template('hotseat/hotseat.html')

@bp.route('/get_hotseat_prompts')
def get_hotseat_prompts():
    try:
        # create a cursor from db file
        conn = connect()
        cur = conn.cursor()

        cur.execute('select summary from hotseat_prompts')

        hotseat_prompts = cur.fetchmany(50)
        random.shuffle(hotseat_prompts)
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        flash (error)
        return render_template('404.html')

    json_string = json.dumps({"results":hotseat_prompts})
    print (json_string)

    return json_string

@bp.route('/custom_prompt_hotseat', methods=('GET', 'POST'))
def custom_prompt_hotseat():
    #grab passed values from POST
    if request.method == 'POST':
        summary = request.form['summary']
        author = request.form['author']
        category = request.form['category']

        print(summary)
        print(author)
        print(category)

        #connect to DB
        conn = connect()
        cur = conn.cursor()
        error = None

        #validate UN and PW were entered or and user isn't already registered
        if not summary:
            error = 'Username is required'
        elif not author:
            error = 'Password is required'
        elif not category:
            error = 'Category is required'

        # if passed above checks, register user and redirect to login page
        if error is None:
            try:
                cur.execute("INSERT INTO hotseat_prompts (summary, category, custom, author) VALUES (%s, %s, %s, %s)", (summary, category, True, author))
                conn.commit()
                success=True
                return render_template('hotseat/add_prompts.html', success=success)
            except (Exception, psycopg2.DatabaseError) as error:
                flash (error)
                return render_template('404.html')
        flash(error)

    return render_template('hotseat/add_prompts.html')
