#!/usr/bin/env python2.7

import socket
import sys
import argparse
import hashlib
import random
import pyglet
import getpass

from protocol import *

sock = None
connection = None
key = None


def read_messages(dt):
    try:
        received = sock.recv(1024)
        if received:
            print "server:", received

        if BYE_RE.match(received):
            pass
    except:
        pass

def send_message(message):
    sock.sendto(MESSAGE.format(key=key, message=message), connection)

# the following is copied from the text_input demo

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )


class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), 
            dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(800, 600, caption='Client')

        self.batch = pyglet.graphics.Batch()
        self.labels = [
            pyglet.text.Label('Input', x=0, y=10, batch=self.batch)
        ]
        self.widgets = [
            TextWidget('', 200, 10, self.width - 210, self.batch)
        ]

        self.text_cursor = self.get_system_mouse_cursor('text')

        self.focus = None
        self.set_focus(self.widgets[0])

    def on_resize(self, width, height):
        super(Window, self).on_resize(width, height)
        for widget in self.widgets:
            widget.width = width - 110

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

        elif symbol == pyglet.window.key.RETURN:
            send_message(self.focus.document.text)
            self.focus.document.text = ''

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


def main(host, port):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)

    name = getpass.getuser() #raw_input("enter your login: ").strip()

    global key
    key = hashlib.sha1(str(random.getrandbits(128))).hexdigest()

    global connection
    connection = (host, port)

    sock.sendto(HELLO.format(name=name, key=key), connection)

    window = Window(resizable=True)
    pyglet.clock.schedule_interval(read_messages, 0.25)
    pyglet.app.run()


if __name__=='__main__':
    # TODO: parse args here

    host = "localhost"
    port = 8123
    main(host=host, port=port)

