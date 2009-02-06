CC=gcc
CFLAGS=-Wall -O -g -I/home/druk/Code/C/networking/libs/
LDFLAGS=
SOURCES=/home/druk/Code/C/networking/libs/netlib.c /home/druk/Code/C/networking/libs/errlib.c traceroute.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=traceroute

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(SOURCES)
	$(CC) $(CFLAGS) $(LDFLAGS) $(SOURCES) -o $@

