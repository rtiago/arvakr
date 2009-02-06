/* traceroute usage */
/* ./traceroute -t <ttl> -v hostname */

#include "traceroute.h"

/* default */
u_int datalen = sizeof(struct rec);
u_short max_ttl = 30;
int verbose = 0;
const char *hostname;


struct proto	proto_v4 = { icmpv4, recv_v4, NULL, NULL, NULL, NULL, 0,
							 IPPROTO_ICMP, IPPROTO_IP, IP_TTL };

void tv_sub(struct timeval *out, struct timeval *in)
{
  if ( (out->tv_usec -= in->tv_usec) < 0)
  { 
    --out->tv_sec;
    out->tv_usec += 1000000;
  }
  out->tv_sec -= in->tv_sec;
}

void traceloop(void)
{ 
  int seq,code,done;
  double rtt;
  struct rec *rec;
  struct timeval tvrecv;

 
  if (( recvfd = socket(pr->sasend->sa_family,SOCK_RAW,pr->icmpproto)) < 0)
    err_sys("socket error");

  if (( sendfd = socket(pr->sasend->sa_family,SOCK_DGRAM,0)) < 0)
    err_sys("socket error");

  pr->sabind->sa_family = pr->sasend->sa_family;
  /* source port */
  sport = (getpid() & 0xffff) | 0x8000;
  sock_set_port(pr->sabind,pr->salen,htons(sport));
  if (bind(sendfd,pr->sabind,pr->salen) < 0)
    err_sys("bind error");
  
  seq = 0;
  done = 0;

  for (ttl = 1; ttl <= max_ttl && done == 0; ttl++)
  {
    if (setsockopt(sendfd,pr->ttllevel,pr->ttloptname, &ttl,sizeof(int)) < 0)
      err_sys("socket error");
    bzero(pr->salast,pr->salen);
  
    printf("%2d  ", ttl);
    fflush(stdout);

    for (probe = 0; probe < nprobes; probe++)
    {
      rec = (struct rec *) sendbuf;
      rec->rec_seq = ++seq;
      rec->rec_ttl = ttl;
      gettimeofday(&rec->rec_tv,NULL);

      sock_set_port(pr->sasend,pr->salen,htons(dport + seq));
      sendto(sendfd,sendbuf,datalen,0,pr->sasend,pr->salen);
  
      if ( (code = (*pr->recv)(seq, &tvrecv))  == -3 )
        printf(" *");
      else 
      {
        char str[NI_MAXHOST];

        if (sock_cmp_addr(pr->sarecv,pr->salast,pr->salen) != 0)
        {
          if(getnameinfo(pr->sarecv,pr->salen,str,sizeof(str),NULL,0,0) == 0)
            printf(" %s (%s)", str, hostntop(pr->sarecv,pr->salen));
          else
            printf(" %s", hostntop(pr->sarecv,pr->salen));
          memcpy(pr->salast,pr->sarecv,pr->salen);
        }
        tv_sub(&tvrecv,&rec->rec_tv);
        rtt = tvrecv.tv_sec * 1000.0 + tvrecv.tv_usec / 1000.0;
        printf(" %.3f ms",rtt);

        /* port unreachable at destination */
        if (code == -1)
          done++;
        else if (code >= 0)
          printf(" (ICMP %s)",(*pr->icmpcode)(code));
      }
      fflush(stdout);
    }
    printf("\n");
  }
}


/* receive function */
/* Return:
 * -3 on timeout
 *  -2 on ICMP time exceeded in transit (caller keeps going)
 *  >= 0 return value is some other ICMP unreachable code */

int recv_v4(int seq, struct timeval *tv)
{
  /* we set alarm to 3 seconds and when fired, recvfrom 
   * will be interrupted and errnot set to EINTR */
  unsigned int hlen1, hlen2, icmplen;
  socklen_t len;
  ssize_t n;
  struct ip *ip, *hip;
  struct icmp *icmp;
  struct udphdr *udp;
  alarm(3);
  for(;;)
  {
    len = pr->salen;
    n = recvfrom(recvfd,recvbuf,sizeof(recvbuf),0,pr->sarecv,&len);
    if (n < 0) {
      if (errno == EINTR) 
      {
        return(-3); 
      }
      else
        err_sys("recvfrom error");
    }
    /* lets get the time of packet arrival */
    if (gettimeofday(tv,NULL) == -1)
      err_sys("gettimeofday error");
      
    
    /* start of IP header */ 
    ip = (struct ip *) recvbuf;
    hlen1 = ip->ip_hl << 2;
    
    /* start of ICMP header */
    icmp = (struct icmp *) (recvbuf + hlen1);
    if ( (icmplen = n - hlen1) < 8)
      err_quit("icmplen (%d) < 8",icmplen);

    /* Check if this message comes from one of your probes */
    if (icmp->icmp_type == ICMP_TIMXCEED &&
     icmp->icmp_code == ICMP_TIMXCEED_INTRANS) {
      if (icmplen < 8 + 20 + 8)
        err_quit("icmplen (%d) < 8 + 20 + 8",icmplen);

      hip = (struct ip *) (recvbuf + hlen1 + 8);
      hlen2 = hip->ip_hl << 2;
      udp = (struct udphdr *) (recvbuf + hlen1 + 8 + hlen2);
      if (hip->ip_p == IPPROTO_UDP && 
        udp->source == htons(sport) &&
        udp->dest == htons(dport + seq))
        /* we hit and intermediate router */
        return(-2);
    }
    else if (icmp->icmp_type == ICMP_UNREACH)
    {
      if (icmplen < 8 + 20 + 8)
        err_quit("icmplen (%d) < 8 + 20 + 8",icmplen);

      hip = (struct ip *) (recvbuf + hlen1 + 8);
      hlen2 = hip->ip_hl << 2;
      udp = (struct udphdr *) (recvbuf + hlen1 + 8 + hlen2);
      if (hip->ip_p == IPPROTO_UDP && 
        udp->source == htons(sport) && 
        udp->dest == htons(dport + seq)) {
        if (icmp->icmp_code == ICMP_UNREACH_PORT)
          /* reached the destination */
          return(-1); 
        else
          /* other codes */
          return(icmp->icmp_code); 
      }
    }
    else if (verbose)
    {
      /* some other ICMP error, recvfrom() again */
      printf(" (from %s: type = %d, code = %d)\n",
      hostntop(pr->sarecv,pr->salen),
      icmp->icmp_type,icmp->icmp_code);
    }
  }
}

/* ICMPv4 Codes */
char *icmpv4(int code)
{
  switch(code)
  {
    case 0: return("Net Unreachable");
    case 1: return("Host Unreachable");
    case 2: return("Protocol Unreachable");
    case 3: return("Port Unreachable");
    case 4: return("Fragmentation Needed and Don't Fragment was Set");
    case 5: return("Source Route Failed");
    case 6: return("Destination Network Unknown");
    case 7: return("Destination Host Unknown");
    case 8: return("Source Host Isolated");
    case 9: return("Communication with Destination Network Administratively Prohibited");
    case 10: return("Communication with Destination Host Administratively Prohibited");
    case 11: return("Destination Network Unreachable for Type of Serivice");
    case 12: return("Destination Host Unreachable for Type of Service");
    case 13: return("Communication Administratively Prohibited");
    case 14: return("Host Precedence Violantion");
    case 15: return("Precedence cutoff in effect");
    default: return("Unknown ICMP Code");
  }
}

/* handler for caught signals */
static void onsig(int signal)
{
  err_quit("SIGNAL: Program interrupted\n");
}

/* catch signals from SIGHUP to SIGTERM except SIGKILL */ 
void catchsignals()
{
  int nsig;
  for (nsig = SIGHUP; nsig < SIGTERM; ++nsig)
  {
    if (nsig == SIGKILL)
      signal(nsig,onsig);
  }
}

int main(int argc, char *argv[])
{
  int c;
  struct addrinfo *hints;
  opterr = 0;
  while ((c = getopt(argc,argv,"t:v")) != -1)
  {
    switch(c)
    {
      case 't':
        if (atoi(optarg) > 255)
          max_ttl=255;
        else
          max_ttl=atoi(optarg);
        #ifdef DEBUG
        printf("TTL is %d\n", max_ttl);
        #endif
        break;
      case 'v':
        #ifdef DEBUG
        printf("Verbose is selected\n");
        #endif
        verbose = 1;
        break;
      case '?':
        err_quit("unrecognized option: %c\n",c);
        break;
    }
  }

  if (optind != argc-1)
    err_quit("Usage: traceroute <-t ttl> <-v> hostname\n");

  hostname = argv[optind];
  #ifdef DEBUG
  printf("Hostname is %s\n",hostname);
  #endif

  catchsignals();

  hostname = "www.cern.ch";
  bzero(hints,sizeof(struct addrinfo));
  hints->ai_flags = AI_CANONNAME;
  hints->ai_family = 0;
  hints->ai_socktype = 0; 

  if ( ( c = getaddrinfo(hostname, NULL, hints, &hints)) != 0)
    err_quit(gai_strerror(c));

  printf("traceroute to %s (%s): %d hops max, %d data bytes\n",hints->ai_canonname,hostntop(hints->ai_addr,hints->ai_addrlen),max_ttl,datalen);

  if(hints->ai_family == AF_INET)  
    pr = &proto_v4;
  else
    err_quit("unknown address family %d",hints->ai_family);

  pr->sasend = hints->ai_addr; /* contains destination address */
  pr->sarecv = calloc(1,hints->ai_addrlen);
  pr->salast = calloc(1, hints->ai_addrlen);
  pr->sabind = calloc(1,hints->ai_addrlen);
  pr->salen = hints->ai_addrlen;

  traceloop();  
  exit(0);
}
