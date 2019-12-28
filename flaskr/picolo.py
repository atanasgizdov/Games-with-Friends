from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
import sys

import psycopg2
from flaskr.db import connect

import json
from random import randrange
import random

bp = Blueprint('picolo', __name__)

players_list = []

# index page displaying all blog posts
@bp.route('/')
def index():

    return render_template('index.html')

@bp.route('/players')
def add_players():

    return render_template('picolo/add_players.html')

@bp.route('/custom_prompt', methods=('GET', 'POST'))
def custom_prompt():
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
                cur.execute("INSERT INTO picolo_prompts (summary, category, custom, author) VALUES (%s, %s, %s, %s)", (summary, category, True, author))
                conn.commit()
                success=True
                return render_template('picolo/add_prompts.html', success=success)
            except (Exception, psycopg2.DatabaseError) as error:
                flash (error)
                return render_template('404.html')
        flash(error)

    return render_template('picolo/add_prompts.html')

# search driver for AJAX adding and removal of players
@bp.route('/add_remove_players')
def add_remove_players():

    if request.args['trigger'] == 'add_player': # get the text to search for
        players_list.append(request.args['player_name'])
    if request.args['trigger'] == 'remove_player':
        players_list.remove(request.args['player_name'])

    current_list = provide_players_list()
    return current_list


@bp.route('/players_list')
def provide_players_list():
    return json.dumps({"results":players_list})

#globals to keep track of active prompts and game state during game_running
game_running = False
prompts = None

@bp.route('/play')
def play_game():

    global game_running
    global prompts

    if not game_running:
        try:
            game_running = False
            # create a cursor from db file
            conn = connect()
            cur = conn.cursor()

            cur.execute('select * from picolo_prompts')

            prompts = cur.fetchmany(50)
            print(prompts)
            random.shuffle(prompts)
         # close the communication with the PostgreSQL
            cur.close()
            game_running = True
        except (Exception, psycopg2.DatabaseError) as error:
            flash (error)
            return render_template('404.html')

    current_prompt = prompts[0]
    prompts.pop(0)

    print(current_prompt)

    type_of_prompt = current_prompt[2]
    print(type_of_prompt)

    if type_of_prompt == "choose_two":

        #grab 2 random unique values from player list
        selected_players_choice = random.sample(players_list, 2)
        print(selected_players_choice)

        payload = {
            "player1": selected_players_choice[0],
            "player2": selected_players_choice[1],
            "summary": current_prompt[1],
            "author": current_prompt[4]
        }

        print(payload)

    elif type_of_prompt == "choose_one":
        payload = {
            "player": random.choice(players_list),
            "summary": current_prompt[1],
            "author": current_prompt[4]
        }

        print(payload)

    else:
        payload = {
            "summary": current_prompt[1],
            "author": current_prompt[4]
        }

        print(payload)

    if not prompts:
        game_running = False
        return render_template('picolo/game_over.html')


    if type_of_prompt == "choose_one" or type_of_prompt == "choose_two":
        return render_template('picolo/play_game_card.html', payload=payload)


    return render_template('picolo/play_game_card.html', payload=payload)

    # grab all results from the DB
    # prompt # ID
    # Body
    # sub-heading
    # type (virus, CaH, Would you rather, etc)
    # Custom (made by a player)
    # number of players required to be chosen (1-2?)
    # author
    # number of drinks to take for this
    # upvotes
    # downvotes

#@bp.route('/vote')
#def vote():
