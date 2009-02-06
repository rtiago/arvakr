CC=gcc
CFLAGS=-Wall -O -g -I libs/ -I /opt/lcg/include/dpm/ 
LDFLAGS=-L /opt/lcg/lib/ -lgfal -ldpm
SOURCES=cert_dpm.c libs/errlib.c
OBJECTS=
EXECUTABLE=cert_dpm

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE):  $(SOURCES)
	$(CC)	$(CFLAGS)	$(LDFLAGS)	$(SOURCES)	-o	$@
