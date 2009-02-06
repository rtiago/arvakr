#include "errlib.h"

/* Extremely useful error library to have */

/* ANSI C header file */
#include <stdarg.h>
/* for syslog() */
#include <syslog.h>


int daemon_proc; /* set nonzero by daemon_init() */

static void err_doit(int, int, const char *, va_list);

/* Nonfatal error related to a system call 
 * Print a message and return */
void err_ret(const char *fmt, ...)
{
  va_list ap;

  va_start(ap,fmt);
  err_doit(1,LOG_INFO,fmt,ap);
  va_end(ap);
  return;
}

/* Fatal error related to a system call
 * Print a message and terminate */
void err_sys(const char *fmt, ...)
{
  va_list ap;
  
  va_start(ap,fmt);
  err_doit(1,LOG_ERR,fmt,ap);
  va_end(ap);
  exit(1);
}

/* Fatal error related to a system call
 * Print a message, dump core and terminate */
void err_dump(const char *fmt, ...)
{
  va_list ap;
  
  va_start(ap,fmt);
  err_doit(1,LOG_ERR,fmt,ap);
  va_end(ap);
  abort();
  exit(1);
}

/* Nonfatal error unrelated to a system call
 * Print a message and return */
void err_msg(const char *fmt, ...)
{
  va_list ap;
  
  va_start(ap,fmt);
  err_doit(0,LOG_INFO,fmt,ap);
  va_end(ap);
  return;
}

/* Fatal error unrelated to a system call
 * Print a message and terminate */
void err_quit(const char *fmt, ...)
{
  va_list ap;

  va_start(ap,fmt);
  err_doit(0,LOG_ERR,fmt,ap);
  va_end(ap);
  exit(1);
}

/* Print a message and return to caller 
 * Caller specifies "errnoflag" and "level" */
static void err_doit(int errnoflag, int level, const char *fmt, va_list ap)
{
  int errno_save, n;
  char buf[MAXLINE];

  /* value caller might want printed */
  errno_save = errno;
  /* this is safe */
  vsnprintf(buf,sizeof(buf),fmt,ap);
  n = strlen(buf);
  if (errnoflag)
    snprintf(buf+n,sizeof(buf)-n,": %s",strerror(errno_save));

  if (daemon_proc)
  {
    syslog(level,buf);
  }
  else
  {
    /* in case stdout and stderr are the same */
    fflush(stdout);
    fputs(buf,stderr);
    fflush(stderr);
  }
  return;
}
