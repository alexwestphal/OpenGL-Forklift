"""
The texture module for assignment2.

@author Alex Westphal 9819 6992
@version 12-Oct-2010
"""

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image

def readImage(path):
    image = Image.open(path)
    (width, height) = image.size
    stringImage = image.tostring("raw", "RGB", 0, -1)
    return (width, height, stringImage)


class Surround(object):
    """The courtyard scene for experimenting with texture mapping."""

    
    TEX_FLOOR_REPS = 4
    FLOOR_SIZE = 15
    WALL_HEIGHT = 15

    def glInit(self):
        """Set up OpenGL pipeline stuff needed by this particular scene"""
        
        # Left Wall Texture
        self.wall_1_id = glGenTextures(1)
        (w,h,pattern) = readImage("pan_1.jpg")
        glBindTexture(GL_TEXTURE_2D, self.wall_1_id)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, w, h, GL_RGB, GL_UNSIGNED_BYTE, pattern)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
        
        # Front Wall Texture
        self.wall_2_id = glGenTextures(1)
        (w,h,pattern) = readImage("pan_2.jpg")
        glBindTexture(GL_TEXTURE_2D, self.wall_2_id)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, w, h, GL_RGB, GL_UNSIGNED_BYTE, pattern)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
        
        # Right Wall Texture
        self.wall_3_id = glGenTextures(1)
        (w,h,pattern) = readImage("pan_3.jpg")
        glBindTexture(GL_TEXTURE_2D, self.wall_3_id)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, w, h, GL_RGB, GL_UNSIGNED_BYTE, pattern)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
        
        # Left Wall Texture
        self.wall_4_id = glGenTextures(1)
        (w,h,pattern) = readImage("pan_4.jpg")
        glBindTexture(GL_TEXTURE_2D, self.wall_4_id)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, w, h, GL_RGB, GL_UNSIGNED_BYTE, pattern)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
        
        
        # Floor Texture
        self.floorTextureID = glGenTextures(1)
        (w,h,pattern) = readImage("scree.tga")
        glBindTexture(GL_TEXTURE_2D, self.floorTextureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, pattern)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
        
        

        
    def walls(self):
        

        # BACK WALL
        glBindTexture(GL_TEXTURE_2D, self.wall_4_id)
        glBegin(GL_QUADS)

        glNormal3f(0, 1, 0)
        
        glTexCoord2f(0, 1)
        glVertex3f(-self.FLOOR_SIZE, self.WALL_HEIGHT, -self.FLOOR_SIZE)
        
        glTexCoord2f(0, 0)
        glVertex3f(-self.FLOOR_SIZE, 0, -self.FLOOR_SIZE)
        
        glTexCoord2f(1, 0)
        glVertex3f(self.FLOOR_SIZE, 0, -self.FLOOR_SIZE)
        
        glTexCoord2f(1, 1)
        glVertex3f(self.FLOOR_SIZE, self.WALL_HEIGHT, -self.FLOOR_SIZE)
        
        glEnd()

        # FRONT WALL
        glBindTexture(GL_TEXTURE_2D, self.wall_2_id)
        glBegin(GL_QUADS)

        glNormal3f(0, 1, 0)
        
        glTexCoord2f(1, 1)
        glVertex3f(-self.FLOOR_SIZE, self.WALL_HEIGHT, self.FLOOR_SIZE)
        
        glTexCoord2f(1, 0)
        glVertex3f(-self.FLOOR_SIZE, 0, self.FLOOR_SIZE)
        
        glTexCoord2f(0, 0)
        glVertex3f(self.FLOOR_SIZE, -0, self.FLOOR_SIZE)
        
        glTexCoord2f(0, 1)
        glVertex3f(self.FLOOR_SIZE, self.WALL_HEIGHT, self.FLOOR_SIZE)
        
        glEnd()

        # LEFT WALL
        glBindTexture(GL_TEXTURE_2D, self.wall_3_id)
        glBegin(GL_QUADS)

        glNormal3f(0, 1, 0)
        
        glTexCoord2f(1, 1)
        glVertex3f(-self.FLOOR_SIZE, self.WALL_HEIGHT, -self.FLOOR_SIZE)
        
        glTexCoord2f(1, 0)
        glVertex3f(-self.FLOOR_SIZE, 0, -self.FLOOR_SIZE)
        
        glTexCoord2f(0, 0)
        glVertex3f(-self.FLOOR_SIZE, 0, self.FLOOR_SIZE)
        
        glTexCoord2f(0, 1)
        glVertex3f(-self.FLOOR_SIZE, self.WALL_HEIGHT, self.FLOOR_SIZE)
        
        glEnd()
        
        # RIGHT WALL

        glNormal3f(0, 1, 0)
        glBindTexture(GL_TEXTURE_2D, self.wall_1_id)
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 1)
        glVertex3f(self.FLOOR_SIZE, self.WALL_HEIGHT, -self.FLOOR_SIZE)
        
        glTexCoord2f(0, 0)
        glVertex3f(self.FLOOR_SIZE, 0, -self.FLOOR_SIZE)
        
        glTexCoord2f(1, 0)
        glVertex3f(self.FLOOR_SIZE, 0, self.FLOOR_SIZE)
        
        glTexCoord2f(1, 1)
        glVertex3f(self.FLOOR_SIZE, self.WALL_HEIGHT, self.FLOOR_SIZE)

        glEnd()

    

    def floor(self):
        glBindTexture(GL_TEXTURE_2D, self.floorTextureID)
        
        glNormal3f(0, 1, 0)
        glBegin(GL_QUADS);
        
        glTexCoord2f(0, self.TEX_FLOOR_REPS)
        glVertex3f(-self.FLOOR_SIZE, 0, -self.FLOOR_SIZE)
        
        glTexCoord2f(0, 0)
        glVertex3f(-self.FLOOR_SIZE, 0, self.FLOOR_SIZE)
        
        glTexCoord2f(self.TEX_FLOOR_REPS,0)
        glVertex3f(self.FLOOR_SIZE, 0, self.FLOOR_SIZE)
        
        glTexCoord2f(self.TEX_FLOOR_REPS, self.TEX_FLOOR_REPS)
        glVertex3f(self.FLOOR_SIZE, 0, -self.FLOOR_SIZE)
        glEnd()


    def glDisplay(self):
        """Output the entire scene to the OpenGL pipeline.
        
        This method is expected to be called by a View object, after the
        model view matrix has been set up for an appropriate view and the
        various buffers cleared.
        """
        glEnable(GL_TEXTURE_2D)
        glColor3f(1,1,1)
        self.walls()
        self.floor()
        glDisable(GL_TEXTURE_2D)
