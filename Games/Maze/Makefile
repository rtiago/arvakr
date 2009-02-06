CC = g++
CFLAGS= -Wno-deprecated -Wall -g -lglut -lGL -lGLU -I ../libs/
SOURCES=MAZE.cpp MAZEGAME.cpp 
EXECUTABLE=game

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES) -o $@

clean:
	rm $(EXECUTABLE)
