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
