#include <iostream>
#include "MAZE.h"

//OpenGL headers
#include "GL/gl.h"
#include "GL/glu.h"
#include "GL/glut.h"
#include "GL/freeglut.h"


using std::cout;
using std::endl;

std::vector<Line> map;

void drawMaze(void)
{
  Maze mz("maze.txt");

  //open file with coordinates
  mz.Initialize();
  map = mz.getCoordinates();
}


void RenderScene(void)
{
  //clear the window with current clearing color
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  glColor3f(0.0f,1.0f,0.0f);
  glLineWidth(1.0f);
  std::vector<Line>::iterator it;
  for(it=map.begin(); it<map.end(); it++)
  {
/*    glRectf(last_x+(*it).getX(),last_y+(*it).getY(),last_x+(*it).getX()+(*it).getDiameter(),last_y);
    last_x += (*it).getX();
    last_y += (*it).getY();
    cout << *it << endl;
*/
		if ((*it).getType() == 1) {
    	glBegin(GL_LINE);
	      glVertex2i((*it).getX1(),(*it).getY1());
  	    glVertex2i((*it).getX2(), (*it).getY2());
 	  	glEnd();
    	glBegin(GL_LINE);
	      glVertex2i((*it).getX1()+5,(*it).getY1()-5);
  	    glVertex2i((*it).getX2()+5, (*it).getY2()-5);
 	  	glEnd();
		}
		else if ((*it).getType() == 2) {
			glBegin(GL_LINE);
		    glVertex2i((*it).getX1(),(*it).getY1());
  	    glVertex2i((*it).getX2(), (*it).getY2());		
			glEnd();
			glBegin(GL_LINE);
		    glVertex2i((*it).getX1()+5,(*it).getY1());
  	    glVertex2i((*it).getX2()+5, (*it).getY2());		
			glEnd();
			//glRecti((*it).getX1(),(*it).getY1(),(*it).getX2(),(*it).getY2());
		}

  }
  //flush drawing commands
  glutSwapBuffers();
}

void ChangeSize(GLsizei w, GLsizei h)
{
  //prevent divide by zero
  if (h == 0)
    h = 1;

  //set viewport to window dimensions
  glViewport(0,0,w,h);

  //set the perspective coordinate system
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluOrtho2D(0.0,810.0,0.0,750.0);

  //insert the mode view and matrix stack
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

}

void SetupRC(void)
{
  //black background
  glClearColor(0.0f,0.0f,0.0f,1.0f);
}


int main(int argc, char* argv[])
{
  cout << "Initializing Graphics" << endl;
  glutInit(&argc,argv);
  //single buffer window and use rgb color
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowSize(810,750);
  glutCreateWindow("MazeGL");
  glutReshapeFunc(ChangeSize);
  glutDisplayFunc(RenderScene);

  drawMaze(); 
  SetupRC();

  glutMainLoop();
}
