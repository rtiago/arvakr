//: MAZE.h
#ifndef MAZE_H
#define MAZE_H

#include <iostream>
#include <string>
#include <vector>
const int size = 5000;
const int fsize = 30;

class Line
{
  private:
    short type; 
    short x1; //x1 position
    short y1; //y1 position
    short x2; //x2 position
    short y2; //y2 position
  public:
    Line(short type_, short coord_x1, short coord_y1, short coord_x2, short coord_y2) : type(type_), x1(coord_x1), y1(coord_y1), x2(coord_x2), y2(coord_y2) {}
    ~Line() {}

    short getX1() const { return x1;}
    short getY1() const { return y1;}
    short getX2() const { return x2;}
    short getY2() const { return y2;}
    short getType() const { return type;}

    friend std::ostream & operator<<(std::ostream& os, const Line& c);
};

class Maze
{
  private:
    std::vector<Line> coordinates;
    const char* coordinatesFile; //This seems not to be safe??
  public:
    Maze(const char* filename) : coordinatesFile(filename) 
    { std::cout << "Maze constructor" << std::endl; }
    ~Maze() {}

    void Initialize();
    std::vector<Line> getCoordinates();

};


#endif // MAZE_H

