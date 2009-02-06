//: MAZE.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include "require.h"
#include "MAZE.h"

using std::ifstream;
using std::cout;
using std::endl;

void Maze::Initialize()
{
  short value_x1 = 0;
  short value_y1 = 0;
  short value_x2 = 0;
  short value_y2 = 0;
  short type = 0;
  ifstream in(coordinatesFile);
  assure(in,coordinatesFile);
 
  in >> type >> value_x1 >> value_y1 >> value_x2 >> value_y2;
  while (in.good() && !in.eof() && !in.fail())
  {
    Line c = Line(type,value_x1,value_y1,value_x2,value_y2);
    coordinates.push_back(c);
    in >> type >> value_x1 >> value_y1 >> value_x2 >> value_y2;
  }
}

std::vector<Line> Maze::getCoordinates()
{
  return coordinates;
}

/* Line */

std::ostream & operator<<(std::ostream& os, const Line& t)
{
  os << "Line: type=" << t.getType() << "x=" << t.getX1() << " y=" << t.getY1() << " to x=" << t.getX2() << " y=" << t.getY2() << endl;
  return os;
}

