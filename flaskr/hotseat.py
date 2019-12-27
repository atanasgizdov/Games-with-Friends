#import pyglet
#pyglet.resource.path = ['/static']
#pyglet.resource.reindex()

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

bp = Blueprint('hotseat', __name__)

#pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

@bp.route('/play_hotseat')
def play_hotseat():
#    sound = pyglet.media.StaticSource(pyglet.media.load('sounds/blarap.wav'))
#    sound.play()
    return render_template('picolo/add_prompts.html')
