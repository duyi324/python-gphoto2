#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2018  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

from contextlib import contextmanager
from datetime import datetime
import logging
import os
import sys

import gphoto2 as gp

def cb_idle(context, data):
    print('cb_idle', data)

def cb_error(context, text, data):
    print('cb_error', text, data)

def cb_status(context, text, data):
    print('cb_status', text, data)

def cb_message(context, text, data):
    print('cb_message', text, data)

def cb_question(context, text, data):
    print('cb_question', text, data)
    return gp.GP_CONTEXT_FEEDBACK_OK

def cb_cancel(context, data):
    print('cb_cancel', data)
    return gp.GP_CONTEXT_FEEDBACK_OK

def cb_progress_start(context, target, text, data):
    print('cb_progress_start', target, text, data)
    return 123

def cb_progress_update(context, id_, current, data):
    print('cb_progress_update', id_, current, data)

def cb_progress_stop(context, id_, data):
    print('cb_progress_stop', id_, data)

@contextmanager
def context_with_callbacks():
    context = gp.Context()
    callbacks = []
    callbacks.append(context.set_idle_func(cb_idle, 'A'))
    callbacks.append(context.set_error_func(cb_error, 'B'))
    callbacks.append(context.set_status_func(cb_status, 'C'))
    callbacks.append(context.set_message_func(cb_message, 'D'))
    callbacks.append(context.set_question_func(cb_question, 'E'))
    callbacks.append(context.set_cancel_func(cb_cancel, 'F'))
    callbacks.append(context.set_progress_funcs(
        cb_progress_start, cb_progress_update, cb_progress_stop, 'G'))
    try:
        yield context
    finally:
        del callbacks

def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    with context_with_callbacks() as context:
        camera = gp.Camera()
        camera.init(context)
        text = camera.get_summary(context)
        config = camera.get_config(context)
        camera.exit(context)
    return 0

if __name__ == "__main__":
    sys.exit(main())