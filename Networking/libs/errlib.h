#ifndef ERRLIB_H_
#define ERRLIB_H_

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
/* Max text line */
#define MAXLINE 4096 


/* Prototypes */
void err_ret(const char *fmt, ...);
void err_sys(const char *fmt, ...);
void err_dump(const char *fmt, ...);
void err_msg(const char *fmt, ...);
void err_quit(const char *fmt, ...);

#endif
