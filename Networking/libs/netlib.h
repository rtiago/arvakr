#ifndef NETLIB_H_
#define NETLIB_H_

//network headers
#include <arpa/inet.h>

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <netdb.h>
#include <string.h>

//prototypes
char *hostntop(const struct sockaddr*, socklen_t);
int hostpton(const struct sockaddr*, const char*);
void sock_set_port(struct sockaddr*,socklen_t salen_t,int);
int sock_cmp_addr(const struct sockaddr*,const struct sockaddr*,socklen_t);

#endif
