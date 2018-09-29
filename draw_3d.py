'''
Copyright (C) 2018 Jean Da Costa machado.
Jean3dimensional@gmail.com

Created by Jean Da Costa machado

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import bgl


class DrawObject:
    def __init__(self):
        self.commands = []

    def __call__(self,*args):
        self.draw()

    def add_line(self, start, end, width=1.5, color=(1, 0, 0, 1)):
        self.commands.append((start, end, width, color))

    def start_drawing(self):
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_LINES)

    def stop_drawing(self):
        bgl.glEnd()
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

    def line3d(self, start, end, width=1.5, color=(1, 0, 0, 1)):
        bgl.glLineWidth(width)
        bgl.glColor4f(*color)
        bgl.glVertex3f(*start)
        bgl.glVertex3f(*end)

    def draw(self):
        self.start_drawing()
        for c in self.commands:
            self.line3d(*c)
        self.stop_drawing()
