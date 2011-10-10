"""
The scene module for assignment2

@author Alex Westphal (9819 6992)
@version 13Sept-2010
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from texture import Surround

from math import sqrt
from random import random, randint

listID = 0

class Scene(object):
	"""A scene for display via OpenGL."""

	def __init__(self):
		"""Constructor"""
		self.forklift = Forklift()
		self.surround = Surround()
		
		self.init_stacks()

	def init_stacks(self):
		"""Setup the initial state of the crate stacks."""
		objects = [
			(lambda: glutSolidSphere(0.4,20,10), True),
			(lambda: glutSolidTorus(0.15,0.3,20,20), True),
			(self.dodecahedron, True),
			(self.octahedron, True),
			(self.tetrahedron, True),
			(self.icosahedron, True),
			(self.mini_forklift, False),
			(self.mini_robot, False),
		]
		
		self.stack1 = CrateStack(5,4, 90)
		self.stack2 = CrateStack(5,4, 90)
		self.stack3 = CrateStack(5,4, -90)
		self.stack4 = CrateStack(5,4, -90)
		
		for i in range(4):
			for j in range(4):
				(obj,canRot) = objects[randint(0, len(objects)-1)]
				self.stack1.insert(Crate(obj, canRot),i,j)
				(obj,canRot) = objects[randint(0, len(objects)-1)]
				self.stack2.insert(Crate(obj, canRot),i,j)
		

	def glInit(self):
		"""The View is expected to call this during OpenGL pipeline
		   initialisation. It sets up any once-only pipeline states that the
		   model wishes to use"""

		glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
		glEnable(GL_COLOR_MATERIAL)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		self.surround.glInit()


	def glDisplay(self):
		"""Output the entire scene to the OpenGL pipeline."""
		
		glLightfv(GL_LIGHT0, GL_POSITION, (-20,10,-19,0))
		
		self.surround.glDisplay()
		
		glPushMatrix()
		glTranslatef(6,0,0)
		self.stack1.display()
		glPopMatrix()
		
		glPushMatrix()
		glTranslatef(5,0,0)
		self.stack2.display()
		glPopMatrix()
		
		glPushMatrix()
		glTranslatef(-5,0,0)
		self.stack3.display()
		glPopMatrix()
		
		glPushMatrix()
		glTranslatef(-6,0,0)
		self.stack4.display()
		glPopMatrix()
		
		self.forklift.display()

	def mini_forklift(self):
		"""Draw a miniature forklift (sized to fit in a crate)."""
		glPushMatrix()
		glTranslatef(0,-0.45,0)
		glScalef(0.25,0.25,0.25)
		glRotate(90, 0,1,0)
		glTranslatef(0,0,-0.6)
		Forklift().display()
		glPopMatrix()

	def mini_robot(self):
		glPushMatrix()
		glTranslate(0,0,-0.1)
		glScalef(0.3,0.3,0.3)
		Robot().display()
		glPopMatrix()

	def dodecahedron(self):
		"""Draw a dodecahedron (sized to fit in a crate)."""
		glPushMatrix()
		glScalef(0.25,0.25,0.25)
		glutSolidDodecahedron()
		glPopMatrix()

	def octahedron(self):
		"""Draw an octahedron (sized to fit in a crate)."""
		glPushMatrix()
		glScalef(0.4,0.4,0.4)
		glutSolidOctahedron()
		glPopMatrix()

	def tetrahedron(self):
		"""Draw a tetrahedron (sized to fit in a crate)."""
		glPushMatrix()
		glScalef(0.4,0.4,0.4)
		glutSolidTetrahedron()
		glPopMatrix()

	def icosahedron(self):
		"""Draw an icosahedron (sized to fit in a crate)."""
		glPushMatrix()
		glScalef(0.4,0.4,0.4)
		glutSolidIcosahedron()
		glPopMatrix()


#=======================================================================


class CrateStack(object):
	"""2D Stack of Crates"""
	
	def __init__(self, width, height, angle):
		"""Initialise the stack.
		width - number of crates wide
		height - number of crates high
		angle - forklift load angle (around y-axis, from (0,0,1))
		"""
		self.width = width
		self.height = height
		self.angle = angle
		self.crates = map(lambda x: map(lambda y: None, range(height)), range(width))

	def insert(self, crate, col, level):
		self.crates[col][level] = crate

	def remove(self,col,level):
		result = self.crates[col][level]
		self.crates[col][level] = None
		return result

	def display(self):
		glPushMatrix()
		glTranslatef(0,0.5,0)
		for col in range(self.width):
			for level in range(self.height):
				crate = self.crates[col][level]
				if crate:
					glPushMatrix()
					glTranslatef(0,level,col)
					glRotatef(self.angle, 0,1,0)
					crate.display()
					glPopMatrix()
		glPopMatrix()


#=======================================================================


class Crate(object):
	
	COLOUR_CRATE = (0.5,0.5,0.5)
	
	def __init__(self, func, canRotate):
		self.func = func
		self.canRotate = canRotate
		if canRotate:
			self.x_rot = randint(0, 360)
			self.y_rot = randint(0, 360)
			self.z_rot = randint(0, 360)
			self.color = (random(), random(), random())
		else:
			self.x_rot = 0
			self.y_rot = 0
			self.z_rot = 0
			self.color = None
		

	def set_x_rot(self, rot):
		self.x_rot = rot

	def set_y_rot(self, rot):
		self.y_rot = rot

	def set_z_rot(self, rot):
		self.z_rot = rot

	def display(self):
		glColor3f(*self.COLOUR_CRATE)
		
		# Base
		glPushMatrix()
		glTranslatef(0,-0.45,0)
		glScalef(1,0.1,1)
		glutSolidCube(1)
		glPopMatrix()
		
		for a in [-0.45,0.45]:
			# Topbars
			glPushMatrix()
			glTranslatef(a,0.45,0)
			glScalef(0.1,0.1,1)
			glutSolidCube(1)
			glPopMatrix()
			
			glPushMatrix()
			glTranslatef(0,0.45,a)
			glScalef(0.8,0.1,0.1)
			glutSolidCube(1)
			glPopMatrix()
			
			# Uprights
			for b in [-0.45,0.45]:
				glPushMatrix()
				glTranslatef(a,0,b)
				glScalef(0.1,0.8,0.1)
				glutSolidCube(1)
				glPopMatrix()
		
		glPushMatrix()
		glScalef(0.9,0.9,0.9)
		
		glRotatef(self.x_rot, 1,0,0)
		glRotatef(self.y_rot, 0,1,0)
		glRotatef(self.z_rot, 0,0,1)
		if self.color: glColor3f(*self.color)
		self.func()
		
		glPopMatrix()


#=======================================================================


class Forklift(object):
	
	COLOUR_BODY_1 = (0.8,0.6,0.3)
	COLOUR_BODY_2 = (0.08,0.08,0.08)
	COLOUR_LIFT = (0.05,0.05,0.05)
	COLOUR_TYRE = (0.1,0.1,0.1)
	COLOUR_GLASS = (0.1,0.2,0.1,0.4)
	COLOUR_GLASS_SPECULAR = (0.4,0.4,0.4,1)
	
	COLOUR_TAILLIGHT_OFF = (0.25,0.025,0.025)
	COLOUR_TAILLIGHT_ON = (0.5,0.05,0.05,1)
	COLOUR_HEADLIGHT_OFF = (0.3,0.4,0.4)
	COLOUR_HEADLIGHT_ON = (0.6,0.8,0.8,1)
	COLOUR_INDICATOR_OFF = (0.4,0.2,0)
	COLOUR_INDICATOR_ON = (0.8,0.2,0,1)
	
	WHEEL_WIDTH = 0.2
	WHEEL_RADIUS = 0.4
	WHEEL_SLICES = 20
	WHEEL_STACKS = 10
	
	AXLE_LENGTH = 1.5
	AXLE_RADIUS = 0.25
	
	def __init__(self):
		self.tail_lights_on = False
		self.head_lights_on = False
		self.left_indicator_on = False
		self.right_indicator_on = False
		self.lift_angle = 0
		self.lift_height = 0
		self.payload = None
		self.location = [0,0,0]
		self.angle = 0

	def reset(self):
		Forklift.__init__(self)

	def set_tail_lights(self, on):
		self.tail_lights_on = on

	def set_head_lights(self, on):
		self.head_lights_on = on

	def set_left_indicator(self, on):
		self.left_indicator_on = on

	def set_right_indicator(self, on):
		self.right_indicator_on = on

	def set_lift_angle(self,theta):
		self.lift_angle = theta

	def set_lift_height(self, height):
		self.lift_height = height

	def set_payload(self, crate):
		self.payload = crate

	def remove_payload(self):
		payload = self.payload
		self.payload = None
		return payload


	def display(self):
		glPushMatrix()
		glTranslatef(*self.location)
		glRotatef(self.angle, 0,1,0)
		
		self.lift()
		
		global listID
		if listID == 0:
			listID = glGenLists(1)
			glNewList(listID, GL_COMPILE)
			self.core()
			self.top()
			self.cockpit()
			self.front_wheels()
			self.back_wheels()
			glEndList()
        
		glCallList(listID)
		
		self.lights()
		
		glPopMatrix()

	def lights(self):
		#Tail light colour
		glColor3f(*self.COLOUR_TAILLIGHT_OFF)
		if self.tail_lights_on:
			glMaterialfv(GL_FRONT,GL_EMISSION,self.COLOUR_TAILLIGHT_ON)

		# Left tail lights
		glPushMatrix()
		glTranslatef(0.5,1.025,-1.2)
		glScalef(0.2,0.2,0.1)
		glutSolidSphere(0.5,8,5)
		glPopMatrix()
		
		# Right tail lights
		glPushMatrix()
		glTranslatef(-0.5,1.025,-1.2)
		glScalef(0.2,0.2,0.1)
		glutSolidSphere(0.5,8,5)
		glPopMatrix()
		
		#Reset emission
		glMaterialfv(GL_FRONT,GL_EMISSION, [0,0,0,1])
		
		
		# Indicator colour
		glColor3f(*self.COLOUR_INDICATOR_OFF)
		if self.left_indicator_on:
			glMaterialfv(GL_FRONT,GL_EMISSION,self.COLOUR_INDICATOR_ON)

		# Left indicator
		glPushMatrix()
		glTranslatef(0.68,1.025,-1.2)
		glScalef(0.1,0.2,0.1)
		glutSolidSphere(0.5,8,8)
		glPopMatrix()
		
		# Reset emission
		glMaterialfv(GL_FRONT,GL_EMISSION, [0,0,0,1])
		
		# Indicator colour
		glColor3f(*self.COLOUR_INDICATOR_OFF)
		if self.right_indicator_on:
			glMaterialfv(GL_FRONT,GL_EMISSION,self.COLOUR_INDICATOR_ON)
		
		# Right indicator
		glPushMatrix()
		glTranslatef(-0.68,1.025,-1.2)
		glScalef(0.1,0.2,0.1)
		glutSolidSphere(0.5,8,8)
		glPopMatrix()
		
		# Reset emission
		glMaterialfv(GL_FRONT,GL_EMISSION, [0,0,0,1])
		
		# Headlight colour
		glColor3f(*self.COLOUR_HEADLIGHT_OFF)
		if self.head_lights_on:
			glMaterialfv(GL_FRONT,GL_EMISSION,self.COLOUR_HEADLIGHT_ON)
		
		# Left head light
		glPushMatrix()
		glTranslate(0.6,2.15,0.55)
		glScalef(0.2,0.2,0.1)
		glutSolidSphere(0.5,8,5)
		glPopMatrix()
		
		# Right head light
		glPushMatrix()
		glTranslate(-0.6,2.15,0.55)
		glScalef(0.2,0.2,0.1)
		glutSolidSphere(0.5,8,5)
		glPopMatrix()
		
		#Reset emission
		glMaterialfv(GL_FRONT,GL_EMISSION, [0,0,0,1])


	def lift(self):
		
		glPushMatrix()
		
		glTranslatef(0,0,1.2)
		if self.lift_angle:
			glTranslate(0,0.95,0)
			glRotatef(-self.lift_angle, 1,0,0)
			glTranslate(0,-0.95,0)
		
		#Main colour
		glColor3f(*self.COLOUR_LIFT)
		
		# Left upright
		glPushMatrix()
		glTranslatef(0.275,1.8,0.075)
		glScalef(0.05,3.2,0.15)
		glutSolidCube(1)
		glPopMatrix()
		
		# Right upright
		glPushMatrix()
		glTranslatef(-0.275,1.8,0.075)
		glScalef(0.05,3.2,0.15)
		glutSolidCube(1)
		glPopMatrix()
		
		# Tilt hinge
		glPushMatrix()
		glTranslatef(-0.325,0.95,0)
		glRotatef(90,0,1,0)
		glutSolidCylinder(0.1,0.65,20,20)
		glPopMatrix()

		# Cross braces
		for height in [0.3,1,2,2.7,3.3]:
			glPushMatrix()
			glTranslatef(0,height,0.025)
			glScalef(0.5,0.2,0.05)
			glutSolidCube(1)
			glPopMatrix()

		# Top bar
		glPushMatrix()
		glTranslate(0,3.35,0.1)
		glScalef(0.5,0.1,0.15)
		glutSolidCube(1)
		glPopMatrix()

		#Lift riser
		glPushMatrix()
		if self.lift_height:
			glTranslatef(0,self.lift_height,0)
		
		# Bottom lateral of lift riser
		glPushMatrix()
		glTranslatef(0,0.1,0.2)
		glScalef(1,0.2,0.1)
		glutSolidCube(1)
		glPopMatrix()
		
		# Top lateral of lift riser
		glPushMatrix()
		glTranslatef(0,0.5,0.2)
		glScalef(1,0.2,0.1)
		glutSolidCube(1)
		glPopMatrix()
		
		glColor3f(*self.COLOUR_BODY_1)
		
		# Left vertical of lift riser
		glPushMatrix()
		glTranslatef(0.25,0.3,0.22)
		glScalef(0.2,0.58,0.1)
		glutSolidCube(1)
		glPopMatrix()
		
		# Right vertical of lift riser
		glPushMatrix()
		glTranslatef(-0.25,0.3,0.22)
		glScalef(0.2,0.58,0.1)
		glutSolidCube(1)
		glPopMatrix()
		
		# Left fork of lift riser
		glPushMatrix()
		glTranslatef(0.25,0.05,0.7)
		glScalef(0.2,0.098,0.98)
		glutSolidCube(1)
		glPopMatrix()
		
		# Right fork of lift riser
		glPushMatrix()
		glTranslatef(-0.25,0.05,0.7)
		glScalef(0.2,0.098,0.98)
		glutSolidCube(1)
		glPopMatrix()
		
		if self.payload:
			glPushMatrix()
			glTranslatef(0,0.5,0.8)
			self.payload.display()
			glPopMatrix()
		
		glPopMatrix()

		
		glPopMatrix()


	def core(self):
		#Longitudinal undercairage
		glPushMatrix()
		glTranslatef(0,0.55,0)
		glScalef(0.6,0.7,2.2)
		glColor3f(*self.COLOUR_BODY_2)
		glutSolidCube(1)
		glPopMatrix()
		
		#yellow
		glColor3f(*self.COLOUR_BODY_1)
		
		#Lateral undercairage
		glPushMatrix()
		glTranslate(0,0.55,0)
		glScale(1.5,0.7,0.7)
		glutSolidCube(1)
		glPopMatrix()
		
		# Deck
		glPushMatrix()
		glTranslatef(0,0.9,0)
		glScalef(1.5,0.1,2.4)
		glutSolidCube(1)
		glPopMatrix()
		
		# Lower engine box
		glPushMatrix()
		glTranslatef(0,0.6725,-0.7)
		glScalef(0.9,0.35,1)
		glutSolidCube(1)
		glPopMatrix()


	def top(self):
		# Upper engine box
		glPushMatrix()
		glTranslatef(0,1.05,-0.8)
		glScalef(1.5,0.2,0.8)
		glColor3f(*self.COLOUR_BODY_1)
		glutSolidCube(1)
		glPopMatrix()
		
		# Upper engine box (centre)
		glPushMatrix()
		glTranslatef(0,1.075,-0.65)
		glScalef(0.8,0.25,1)
		glColor3f(*self.COLOUR_BODY_2)
		glutSolidCube(1)
		glPopMatrix()
		
		# hydralic tank
		glPushMatrix()
		glTranslate(0.4,1.1,-0.275)
		glRotatef(90,0,1,0)
		glColor3f(*self.COLOUR_BODY_2)
		glutSolidCylinder(0.1,0.32,20,20)
		glPopMatrix()
		

		# Cockpit base
		glPushMatrix()
		glTranslatef(0,1,0.4)
		glScalef(1.2,0.1,1.1)
		glColor3f(*self.COLOUR_BODY_2)
		glutSolidCube(1)
		glPopMatrix()


	def cockpit(self):

		# Cockpit frame (right back column)
		glColor3f(*self.COLOUR_BODY_2)
		glPushMatrix()
		glTranslatef(-0.475,1.55,-0.125)
		glScalef(0.051,1,0.051)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit frame (left back column)
		glPushMatrix()
		glTranslatef(0.475,1.55,-0.125)
		glScalef(0.051,1,0.051)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit frame (right front column)
		glPushMatrix()
		glTranslatef(-0.475,1.55,0.525)
		glScalef(0.051,1,0.051)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit frame (left front column)
		glPushMatrix()
		glTranslatef(0.475,1.55,0.525)
		glScalef(0.051,1,0.051)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit frame (back top bar)
		glPushMatrix()
		glTranslatef(0,2.025,-0.125)
		glScalef(0.9,0.051,0.051)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit frame (front top bar)
		glPushMatrix()
		glTranslatef(0,2.025,0.525)
		glScalef(0.9,0.051,0.051)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit frame (right top bar)
		glPushMatrix()
		glTranslatef(-0.475,2.025,0.2)
		glScalef(0.051,0.051,0.6)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit frame (left top bar)
		glPushMatrix()
		glTranslatef(0.475,2.025,0.2)
		glScalef(0.051,0.051,0.6)
		glutSolidCube(1)
		glPopMatrix()

		
		glColor4f(*self.COLOUR_GLASS)
		glMaterialfv(GL_FRONT, GL_SPECULAR, self.COLOUR_GLASS_SPECULAR)
		glMaterialf(GL_FRONT,GL_SHININESS, 10)
		
		# Cockpit (back)
		glPushMatrix()
		glTranslatef(0,1.55,0.2)
		glScalef(1,1,0.7)
		glutSolidCube(1)
		glPopMatrix()
		
		# Cockpit (front)
		glPushMatrix()
		glTranslatef(0,1.05,0.55)
		
		glBegin(GL_TRIANGLES)
		glNormal3f(-1,0,0)
		glVertex3f(-0.5,0,0)
		glNormal3f(sqrt(0.5),0,sqrt(0.5))
		glVertex3f(-0.4,0,0.3)
		glNormal3f(-sqrt(0.5),0,sqrt(0.5))
		glVertex3f(-0.5,1,0)
		glEnd()
		
		glBegin(GL_TRIANGLES)
		glNormal3f(sqrt(0.5),0,sqrt(0.5))
		glVertex3f(0.5,1,0)
		glNormal3f(sqrt(0.5),0,sqrt(0.5))
		glVertex3f(0.4,0,0.3)
		glNormal3f(1,0,0)
		glVertex3f(0.5,0,0)
		glEnd()
		
		glBegin(GL_QUADS)
		glNormal3f(0,sqrt(0.5),sqrt(0.5))
		glVertex3f(-0.5,1,0)
		glVertex3f(-0.4,0,0.3)
		glVertex3f(0.4,0,0.3)
		glVertex3f(0.5,1,0)
		glEnd()
		
		glPopMatrix()
		
		glMaterialfv(GL_FRONT, GL_SPECULAR, (0,0,0,1))
		glMaterialf(GL_FRONT,GL_SHININESS, 0)

		# Head light bar
		glPushMatrix()
		glTranslatef(0,2.15,0.5)
		glScalef(1.4,0.2,0.1)
		glColor3f(*self.COLOUR_BODY_2)
		glutSolidCube(1)
		glPopMatrix()
		


	def front_wheels(self):
		glPushMatrix()
		glTranslatef(-0.75,0.4,0.8)
		glRotatef(90,0,1,0)
		
		# Axle
		glColor3f(*self.COLOUR_BODY_2)
		glutSolidCylinder(self.AXLE_RADIUS,self.AXLE_LENGTH,self.WHEEL_SLICES,self.WHEEL_STACKS)

		glColor3f(*self.COLOUR_TYRE)
		
		# Outside right front wheel
		glTranslatef(0,0,0.02)
		glutSolidCylinder(self.WHEEL_RADIUS,self.WHEEL_WIDTH,self.WHEEL_SLICES,self.WHEEL_STACKS)

		# Inside right front wheel
		glTranslatef(0,0,0.22)
		glutSolidCylinder(self.WHEEL_RADIUS,self.WHEEL_WIDTH,self.WHEEL_SLICES,self.WHEEL_STACKS)
		
		# Inside left front wheel
		glTranslatef(0,0,0.82)
		glutSolidCylinder(self.WHEEL_RADIUS,self.WHEEL_WIDTH,self.WHEEL_SLICES,self.WHEEL_STACKS)
		
		# Outside left front wheel
		glTranslatef(0,0,0.22)
		glutSolidCylinder(self.WHEEL_RADIUS,self.WHEEL_WIDTH,self.WHEEL_SLICES,self.WHEEL_STACKS)

		glPopMatrix()

	def back_wheels(self):
		glPushMatrix()
		glTranslatef(-0.75,0.4,-0.8)
		glRotatef(90,0,1,0)
		
		# Axle
		glColor3f(*self.COLOUR_BODY_2)
		glutSolidCylinder(self.AXLE_RADIUS,self.AXLE_LENGTH,self.WHEEL_SLICES,self.WHEEL_STACKS)

		glColor3f(*self.COLOUR_TYRE)
		
		# Right back wheel
		glTranslatef(0,0,0.02)
		glutSolidCylinder(self.WHEEL_RADIUS,self.WHEEL_WIDTH,self.WHEEL_SLICES,self.WHEEL_STACKS)

		
		# Left back wheel
		glTranslatef(0,0,1.26)
		glutSolidCylinder(self.WHEEL_RADIUS,self.WHEEL_WIDTH,self.WHEEL_SLICES,self.WHEEL_STACKS)

		glPopMatrix()


#=======================================================================


class Robot(object):
	def display(self):
		"""Output the entire robot to the OpenGL pipeline."""
		self.torso()
		self.head()
		self.shoulder_pivot()
		self.left_arm()
		self.right_arm()

	def torso(self):
		glPushMatrix()
		glScalef(1,2,0.5)
		glColor3f(1, 0, 0)
		glutSolidCube(1)
		glPopMatrix()
		
	def head(self):
		glPushMatrix()
		glTranslatef(0,1.25,0)
		glRotatef(-15, 0,1,0)
		self.left_eye()
		self.right_eye()
		glScalef(0.5,0.5,0.3)
		glColor3f(0.5,0.2,0.2)
		glutSolidCube(1)
		glPopMatrix()
		
	def left_eye(self):
		glPushMatrix()
		glTranslatef(0.1,0.1,0.15)
		glScalef(0.06,0.05,0.04)
		glColor3f(1,1,0)
		glutSolidSphere(1,20,20)
		glPopMatrix()
		
	def right_eye(self):
		glPushMatrix()
		glTranslatef(-0.1,0.1,0.15)
		glScalef(0.06,0.05,0.04)
		glColor3f(1,1,0)
		glutSolidSphere(1,20,20)
		glPopMatrix()
		
	def shoulder_pivot(self):
		glPushMatrix()
		glTranslatef(-0.75,0.75,0)
		glRotatef(90, 0,1,0)
		
		glColor3f(0,0,1)
		glutSolidCylinder(0.02,1.5,20,20)
		glPopMatrix()
		
	def left_arm(self):
		glPushMatrix()
		glTranslatef(0.6,0.75,0)
		glRotatef(-30, 1,0,0)
		glTranslatef(0,-0.5,0)
		glScalef(0.2,1.2,0.15)
		
		glColor3f(0,1,0)
		glutSolidCube(1)
		glPopMatrix()
		
	def right_arm(self):
		glPushMatrix()
		glTranslatef(-0.6,0.75,0)
		glRotatef(-60, 1,0,0)
		glTranslatef(0,-0.5,0)
		glScalef(0.2,1.2,0.15)
		
		glColor3f(0,1,0)
		glutSolidCube(1)
		glPopMatrix()
		
		
		
		
		
		
