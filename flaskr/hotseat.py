from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

bp = Blueprint('hotseat', __name__)

#pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

@bp.route('/play_hotseat')
def play_hotseat():
#    from playsound import playsound
    #https://www.soundjay.com/button/beep-07.wav
    return render_template('hotseat/hotseat.html')
