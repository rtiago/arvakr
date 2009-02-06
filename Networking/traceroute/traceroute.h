#ifndef TRACEROUTE_H_
#define TRACEROUTE_H_

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <signal.h>
#include <unistd.h>
#include <netdb.h>
#include <string.h>

/* template for IPv4 header in a raw socket */
#include <netinet/ip.h>
/* template for ICMP packets */
#include <netinet/ip_icmp.h>
/* udp packets */
#include <netinet/udp.h>

//external library
#include "netlib.h"
#include "errlib.h"

#define BUFSIZE 2000

enum {false=0,true=1};

char recvbuf[BUFSIZE];
char sendbuf[BUFSIZE];

int ttl,probe,nprobes;
int sendfd, recvfd; /* send on UDP sock, read on raw ICMP sock*/
u_short sport,dport;

struct rec {
  u_short rec_seq; /* sequence number */
  u_short rec_ttl; /* ttl packet left with */
  struct timeval rec_tv; /* time packet left */
};

struct proto {
  char *(*icmpcode)(int);
  int (*recv)(int, struct timeval *);
  struct sockaddr *sasend; /* sockaddr{} for send, from getaddrinfo */
  struct sockaddr *sarecv; /* sockaddr{} for receiving */
  struct sockaddr *salast; /* last sockaddr{} for receiving */
  struct sockaddr *sabind; /* sockaddr{} for binding source port */
  socklen_t salen; /* length of sockaddr{}s */
  int icmpproto; /* IPPROTO_xxx value for ICMP */
  int ttllevel; /* setsockopt() level to set TTL */
  int ttloptname; /* setsockopt() name to set TTL */
} *pr;

/* prototypes */
static void onsig();
void catchsignals();
void tv_sub(struct timeval *, struct timeval *);
void traceloop(void);
int recv_v4(int, struct timeval *);
char *icmpv4(int);


#endif
