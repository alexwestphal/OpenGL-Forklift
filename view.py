"""
The view module for assignment2.

@author Alex Westphal 9819 6992
@version 12-Oct-2010
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin,cos,sqrt, radians

#==============================================================================

class View(object):
    """ A View object provides a view of a scene."""
    
    VIEW_MODE_FOLLOW = 0
    VIEW_MODE_GLOBAL = 1
    VIEW_MODE_INSIDE = 2
    
    MAX_ZOOM_IN = 2
    MAX_ZOOM_OUT = 90

    
    def __init__(self, scene, eye_point, look_at, view_up=(0,1,0),
                 field_of_view=40, near=0.1, far=100, aspectRatio=1):
        """Initialise the view, with lots of common default parameters"""
        self.scene = scene
        self.eye_point = tuple(eye_point)
        self.look_at = tuple(look_at)
        self.view_up = tuple(view_up)
        self.modal_fov = [field_of_view,field_of_view,60]
        self.aspect = aspectRatio
        self.near = near
        self.far = far
        self.width = self.height = 0
        self.modal_x_angle = [0,0,0]
        self.modal_y_angle = [0,0,0]
        self.view_mode = self.VIEW_MODE_FOLLOW
        
        self.camera_position = [0,0,0]
        
        #Initialise GLUT and create a window
        
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(500, 501)
        glutInitWindowPosition(0, 0)
        glutCreateWindow("Assignment 2")
        
        # Set up the OpenGL engine into a simple basic state
        
        glClearColor( 0.95, 0.95, 0.95, 1 ) # Background colour			       
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        
        # Lastly let the scene set any OpenGL state it requires
        
        self.scene.glInit()


    def reshape(self, width, height ):
        """ Reshape function, called whenever user resizes window.

            This function is expected to be called directly by OpenGL, as
            a consequence of a setup call of the form
            glutReshapeFunc(view.reshape)."""
    
        glViewport(0, 0, width, height)
        self.width = width
        self.height = height
        self.aspect = width / float(height)
        
        
    def incYRotation(self, theta):
        """Add theta degrees to the current x-rotation angle of the scene"""
        self.modal_y_angle[self.view_mode] += theta
        if self.view_mode == self.VIEW_MODE_INSIDE:
            self.modal_y_angle[self.view_mode] = min(max(self.modal_y_angle[self.view_mode], -50),50)
        
    def incXRotation(self, theta):
        """Add theta degrees to to the current y-rotation angle of the scene"""
        self.modal_x_angle[self.view_mode] += theta
        self.modal_x_angle[self.view_mode] = min(max(self.modal_x_angle[self.view_mode], 0),80)
    
    def zoomIn(self):
        self.modal_fov[self.view_mode] -= 2
        self.modal_fov[self.view_mode] = max(self.modal_fov[self.view_mode], self.MAX_ZOOM_IN)
        
    def zoomOut(self):
        self.modal_fov[self.view_mode] += 2
        self.modal_fov[self.view_mode] = min(self.modal_fov[self.view_mode], self.MAX_ZOOM_OUT)
        
    def toggleViewMode(self):
        if self.view_mode == self.VIEW_MODE_FOLLOW:
            self.view_mode = self.VIEW_MODE_GLOBAL
        elif self.view_mode == self.VIEW_MODE_GLOBAL:
            self.view_mode = self.VIEW_MODE_INSIDE
        else:
            self.view_mode = self.VIEW_MODE_FOLLOW
            
    def display(self):
        """Display the scene with the current viewing parameters"""
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity( )
        gluPerspective(self.modal_fov[self.view_mode], self.aspect, self.near, self.far)
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        gluLookAt(*(self.eye_point+self.look_at+self.view_up))
        
        if self.view_mode != self.VIEW_MODE_INSIDE:
            glRotatef(self.modal_x_angle[self.view_mode], 1,0,0)
            glRotatef(self.modal_y_angle[self.view_mode], 0,1,0)
        
        if self.view_mode == self.VIEW_MODE_FOLLOW:
            pos_x,pos_y,pos_z = self.scene.forklift.location
            glTranslatef(-pos_x,-pos_y,-pos_z)
        
        if self.view_mode == self.VIEW_MODE_INSIDE:
            pos_x,pos_y,pos_z = self.scene.forklift.location
            angle = self.scene.forklift.angle+self.modal_y_angle[2]
            theta = radians(angle)
            glTranslate((pos_x*cos(theta) - pos_z*sin(theta)), 0, (pos_x*sin(theta) + pos_z*cos(theta)))
            glTranslatef(0,-0.5,8.3)
            glRotatef(180-angle, 0,1,0)
            
            
        
        
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear frame buffer
        self.scene.glDisplay()
        glutSwapBuffers()
        
