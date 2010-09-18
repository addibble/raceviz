#!/usr/bin/python

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import serial
import sys
import time
ser=serial.Serial('/dev/tty.usbserial-A600dSBx', 38400)

window = None
size = (320,240)

x_accel=0
y_accel=0
z_accel=0
x_gyro=0
y_gyro=0
z_gyro=0
x_mag=0
y_mag=0
z_mag=0

def display():
  glutSetWindow(window);
  glClearColor (0.5, 0.4, 0.3, 0.0)
  glClear(GL_COLOR_BUFFER_BIT)
  glFlush()
  glColor3f(1.0, 1.0, 1.0);
  glLineWidth(10.0)
  glBegin(GL_LINES)
  glVertex3f(0, 0, 0)
  glVertex3f((x_mag/1000), (y_mag/1000), (z_mag/1000))
  glEnd()
  
  glutSwapBuffers()


def reshape( *args ):
  global size 
  size = args
  glViewport( *( (0,0)+args) )
  display()


def myGLEvent( name ):
  def onevent( *args ):
    print '%s -> %s'%(name, ", ".join( [str(a) for a in args ]))
  return onevent

def idle():
  while 1:
    s=ser.read()
    if s == "$":
      ser.read()
      break

  line = ""
  while 1:
    s=ser.read()
    if s == "#":
      break
    else:
      line += s

  line=line[0:len(line)-1]
  (x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, x_mag, y_mag, z_mag) = map(int, line.split(","))
  print "accel: (%d,%d,%d) gyro: (%d,%d,%d) mag: (%d,%d,%d)" % (x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, x_mag, y_mag, z_mag)
  display()


def startupIMU():
  ser.open()
  time.sleep(1)
  ser.readline()
  ser.write('4')

if __name__ == "__main__":
  startupIMU()
  glutInit()
  glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
  glutInitWindowSize(800, 600)
  glutInitWindowPosition(100, 100)
  window = glutCreateWindow("viz")
  print 'window', repr(window)
  glutDisplayFunc(display)
  glutReshapeFunc(reshape)

  glutMouseFunc(myGLEvent( 'Mouse' ))
  glutEntryFunc(myGLEvent( 'Entry' ))
  glutKeyboardFunc( myGLEvent( 'Keyboard' ))
  glutKeyboardUpFunc( myGLEvent( 'KeyboardUp' ))
  glutMotionFunc( myGLEvent( 'Motion' ))
  glutPassiveMotionFunc( myGLEvent( 'PassiveMotion' ))
  glutVisibilityFunc( myGLEvent( 'Visibility' ))
  glutWindowStatusFunc( myGLEvent( 'WindowStatus' ))
  glutSpecialFunc( myGLEvent( 'Special' ))
  glutSpecialUpFunc( myGLEvent( 'SpecialUp' ))
  
  glutIdleFunc( idle )

  glutMainLoop()

