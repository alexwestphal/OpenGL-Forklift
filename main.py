"""
The main module for assignment2.

@author Alex Westphal 9819 6992
@version 12-Oct-2010
"""

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from view import View
from scene import Scene
from scheduler import Scheduler
from animation import Animation

class Controller(object):
	"""The Controller for the OpenGL application."""

	MAX_X_DRAG_ROTATION = 120
	MAX_Y_DRAG_ROTATION = 90


	def __init__(self, scene, view):
		# Record the scene and view
		self.scene = scene
		self.view = view
		self.scheduler = Scheduler()
		self.animation = Animation(self.scene, self.scheduler)
		self.mouseX = 0   # Current mouse X coordinate in the window
		self.leftButtonState = GLUT_UP # Current left-button state
		
		glutDisplayFunc(self.view.display)
		glutReshapeFunc(self.view.reshape)
		glutMotionFunc(self.mouseMotionFunc)
		glutMouseFunc(self.mouseButtonFunc)
		glutKeyboardFunc(self.keyFunc)
		glutSpecialFunc(self.specialFunc)
		glutIdleFunc(self.idleFunc)


	def mouseButtonFunc(self, button, state, x, y):
		"""The GLUT mouseFunc handler. This is used to rotate the entire scene."""
		if button == GLUT_LEFT:
			self.mouseX = x
			self.mouseY = y
			self.leftButtonState = state


	def mouseMotionFunc(self, x, y):
		"""The GLUT mouse motion handler. This is used to rotate the entire scene."""
		if self.leftButtonState == GLUT_DOWN:
			(_, _, w, h) = glGetFloat(GL_VIEWPORT)
			y_rot = self.MAX_X_DRAG_ROTATION * (x - self.mouseX) / w # Compute horizontal rotation
			x_rot = self.MAX_Y_DRAG_ROTATION * (y - self.mouseY) / w # Compute vertical rotation
			self.mouseX = x
			self.mouseY = y
			self.view.incYRotation(y_rot)
			self.view.incXRotation(x_rot)
			glutPostRedisplay()


	def keyFunc(self, key, x, y):
		if key == '+': self.view.zoomIn()
		if key == '-': self.view.zoomOut()
		if key == '<': self.scheduler.decreaseSpeed()
		if key == '>': self.scheduler.increaseSpeed()
		if key == 'm': self.view.toggleViewMode()
		if key == 'r': self.animation.reset()
		if key == ']': self.animation.lift_riser()
		if key == '[': self.animation.drop_riser()
		if key == '1': self.animation.run1()
		if key == '2': self.animation.run2()
		
		glutPostRedisplay()


	def specialFunc(self, key, x, y):
		if key == GLUT_KEY_LEFT: self.animation.turn_left()
		if key == GLUT_KEY_RIGHT: self.animation.turn_right()
		if key == GLUT_KEY_UP: self.animation.move_forward()
		if key == GLUT_KEY_DOWN: self.animation.move_backward()
		glutPostRedisplay()

	def idleFunc(self):
		self.scheduler.run()
		glutPostRedisplay()


	def run(self):
		"""Start the app (just runs the GLUT main loop)"""
		glutMainLoop()


#==============================================================================

# The main body just creates the model, view and controller and wires them up
# (if the file is executed as the main program rather than just imported).

if __name__ == "__main__":

	EYE_POINT = (0, 1, 8)
	LOOK_AT = (0, 1, 0)

	scene = Scene()
	view = View(scene, EYE_POINT, LOOK_AT)
	controller = Controller(scene, view)
	controller.run()


