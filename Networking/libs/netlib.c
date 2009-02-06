#include "netlib.h"

/* Network Library */

/*TODO: Implement other adress families */
/* convert an address in numeric format (network format) to text string */

char *hostntop(const struct sockaddr *sa, socklen_t salen)
{
  static char host[128]; /* unix domain can be large*/

  switch(sa->sa_family) {
    case AF_INET:
    {
      struct sockaddr_in *sin = (struct sockaddr_in *) sa;
    
      if (inet_ntop(AF_INET,&sin->sin_addr,host,sizeof(host)) == NULL)
        return (NULL);
      return(host);
    }
  }
  return (NULL);
}

/* convert an address in text string format to numeric (network format) */

int hostpton(const struct sockaddr *sa,const char *addr)
{
  switch(sa->sa_family)
  {
    case AF_INET:
    {
      struct sockaddr_in *sin = (struct sockaddr_in *) sa;
      if (inet_pton(AF_INET,addr,&sin->sin_addr) == 0)
        return 1;
    }
  }
  return 0;
}

/* set socket port to various address families */

void sock_set_port(struct sockaddr *sa, socklen_t salen, int port)
{
  switch(sa->sa_family)
  {
    case AF_INET:
    {
      struct sockaddr_in *sin = (struct sockaddr_in *) sa;
      
      sin->sin_port = port;
      return;
    }
  }
  return;
}


/* compare two addresses */

int sock_cmp_addr(const struct sockaddr *sa1, const struct sockaddr *sa2, socklen_t salen)
{
  if (sa1->sa_family != sa2->sa_family)
    return -1;
  
  switch(sa1->sa_family)
  {
    case AF_INET:
    {
      return(memcmp( &((struct sockaddr_in *) sa1)->sin_addr,
               &((struct sockaddr_in *) sa2)->sin_addr,
               sizeof(struct in_addr)));
    }
  }
  return -1;
}
