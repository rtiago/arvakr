#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>

#include "dpm_api.h"
#include "u64subr.h"
#include "errlib.h"
#include "serrno.h"

/* network headers */
#include "unistd.h"

#define BUF_SIZE 256
#define SECONDS_IN_A_HOUR 3600

/* for portability */
#define bzero(b,len) (memset((b), '\0', (len)), (void) 0)

/* TODO */
/* Add command line options - Server and poolname */

char *server="vtb-generic-85.cern.ch";
char info[BUF_SIZE];

struct dpm_pool *dpm_pools;
struct dpm_fs *dpmfs;
struct dpm_space_metadata *dpmsmd;

char *randstr = NULL;
char **stokens = NULL; 

/* flag to check if we are running the tests on the dpm or not */
u_short local = 0;

/* check if we are on the DPM */
void verify_hostname(void)
{
	char hostname[BUF_SIZE];
	if (gethostname(hostname,sizeof(hostname)) < 0)
		err_quit("could not retrieve the hostname of this machine\n");
	if (hostname == server) {
		printf(" => running all tests\n");
		local = 1;
	}
	else {
		printf(" => running only remote tests\n");
		local = 0;
	}
}

/* release the memory on exit */
void cleanup(void)
{
	free(stokens);
	free(randstr);
	free(dpm_pools);
	free(dpmfs);
}

/* clean the buffer */
void clean_buf(char *buf, unsigned short len)
{
  bzero(buf,len);
}

/* verify that the dpm is alive and get the version number */
void ping(void)
{
  if (dpm_ping(server,info) < 0)
    err_quit("dpm_ping failed\n"); 
 
  printf("dpm server is running version %s\n",info);
}

/* get pool and filesystem information from the dpm */
void query_conf(void)
{
  unsigned int nbpools = 0, nbfs = 0;
  unsigned short i,j;

  if (dpm_getpools(&nbpools,&dpm_pools) < 0)
    err_quit("dpm_getpools failed\n");

  printf("There are %d pool(s) in %s\n",nbpools,server);
  for (i = 0 ; i < nbpools ; i++)
  {
    printf("Pool %s info:\n",(dpm_pools+i)->poolname);
    printf(" => start threshold: %d\n",dpm_pools->gc_start_thresh);
    printf(" => stop threshold: %d\n",dpm_pools->gc_stop_thresh);
    printf(" => retention policy: %c \n",dpm_pools->ret_policy);
    printf(" => lifetime: %.1f hour(s)\n",(float) dpm_pools->def_lifetime/SECONDS_IN_A_HOUR);
    printf(" => pintime: %.1f hour(s)\n",(float) dpm_pools->defpintime/SECONDS_IN_A_HOUR);
    printf(" => max lifetime: %.1f hour(s)\n",(float) dpm_pools->max_lifetime/SECONDS_IN_A_HOUR);
    printf(" => max pintime: %.1f hour(s)\n",(float) dpm_pools->maxpintime/SECONDS_IN_A_HOUR);
    printf(" => fss policy: %s\n",dpm_pools->fss_policy);
    printf(" => gc policy: %s\n",dpm_pools->gc_policy);
    printf(" => mig policy: %s\n",dpm_pools->mig_policy);
    printf(" => rs policy: %s\n",dpm_pools->rs_policy);
    printf(" => space type: %c\n",dpm_pools->s_type);
    clean_buf(info,BUF_SIZE);
    printf(" => capacity: %s\n",u64tostru(dpm_pools->capacity,info,0));
    clean_buf(info,BUF_SIZE);
    printf(" => free: %s\n",u64tostru(dpm_pools->free,info,0));
    /* get the dpm filesystem */
    if (dpm_getpoolfs((dpm_pools+i)->poolname,&nbfs,&dpmfs) < 0)
      err_quit("dpm_getpoolfs failed\n");
    for (j = 0; j < nbfs;j++)
    {
      printf("Filesystem %s info:\n",(dpmfs+j)->fs);
      printf(" => pool: %s\n",(dpmfs+j)->poolname);
      printf(" => server: %s\n",(dpmfs+j)->server);
      clean_buf(info,BUF_SIZE);
      printf(" => capacity: %s\n",u64tostru((dpmfs+j)->capacity,info,0));
      clean_buf(info,BUF_SIZE);
      printf(" => free: %s\n",u64tostru((dpmfs+j)->free,info,0));
      printf(" => status: %d\n",(dpmfs+j)->status);
    }
  }
}

/* create a random alphanumeric string */
char *random_string(void)
{
	char Base[62]="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	unsigned int i,index;
	randstr = malloc(sizeof(char)*16);
	for (i = 0; i<15; i++) {
		index = rand() % 61;
		randstr[i] = Base[index];
	}	
	randstr[15]='\0';
	return randstr;
}

/* reserve a space with a token description */
void reserve_space_token(const char *token_desc)
{
	time_t lifetime = 600;
	clean_buf(info,BUF_SIZE);
	if (dpm_reservespace('P',token_desc,'R','O',strtou64("20000")*1024,strtou64("20000")*1024,lifetime,0,"the_dpm_pool",NULL,NULL,NULL,NULL,info) < 0)
		err_quit("reserve space token error: %s\n",sstrerror(serrno));
	else {
		printf("allocated token: %s",info);
		printf(" => OK\n");
	}
}

/* get space based on a token and its descriptions */
int get_space_token(const char *token_desc)
{
	int nbreplies = 0;
	u_short i;
	/* get all the space tokens associated with this user */
	if (dpm_getspacetoken(token_desc,&nbreplies,&stokens) < 0)
		err_quit("getting space token error: %s\n",sstrerror(serrno));
	else {
		for (i = 0; i<nbreplies; i++)
		{
			printf("%s",stokens[i]);
			printf(" => OK\n");
		}
	}
	return nbreplies;	
}

/* release a space based on a token and its description */
void release_reserved_space(char **tokens,int nbreplies)
{
	u_short i;
	for (i = 0; i < nbreplies; i++) 
	{
		if (dpm_releasespace(tokens[i],1) < 0)
			err_quit("could not release space: %s\n",sstrerror(serrno));
		else 
		{
			printf("%s",tokens[i]);
			printf(" => Released\n");
		}
	}
}

/* get space metadata */
void get_space_metada(char **tokens,int replies)
{
	u_short i;
	int nbreplies;
	if (dpm_getspacemd(replies,tokens,&nbreplies,&dpmsmd) < 0)
		err_quit("get space metadata failed: %s\n",sstrerror(serrno));
	else
	{
		for (i = 0; i < nbreplies; i++)
		{
			printf(" => space type: %c\n",(dpmsmd+i)->s_type);
			printf(" => space token: %s\n",(dpmsmd+i)->s_token);
			printf(" => space user id: %d\n",(dpmsmd+i)->s_uid);
			printf(" => space group id: %d\n",(dpmsmd+i)->s_gid);
			printf(" => retention policy: %c\n",(dpmsmd+i)->ret_policy);
			printf(" => latency: %c\n",(dpmsmd+i)->ac_latency);
			printf(" => user token: %s\n",(dpmsmd+i)->u_token);
      clean_buf(info,BUF_SIZE);
			printf(" => total space: %s\n",u64tostru(((dpmsmd+i)->t_space),info,0));
			printf(" => guaranteed space: %s\n",u64tostru(((dpmsmd+i)->g_space),info,0));
			printf(" => pool name: %s\n",(dpmsmd+i)->poolname);
			printf(" => lifetime assigned: %.1f\n",(float)(dpmsmd+i)->a_lifetime);
			printf(" => remaining lifetime: %.1f\n",(float)(dpmsmd+i)->r_lifetime);
		}
		printf(" => OK\n");
	}	
}

/* add a pool to the dpm, I will just use
 * the previous pool options with a different 
 * name 
 * REQ: Needs admin permissions */
void add_pool()
{
	/*dpm_pools->poolname = "certification_pool_name";
  dpm_addpool(dpm_pools);*/
}


int main(void)
{
	int replies;
	const char *tk_desc = random_string();
	srand((unsigned int)time(NULL));

  printf("Testing DPM API\n");
	
	printf(" -- Trying to verify where we are --\n");
	verify_hostname();

  printf(" -- DPM Ping --\n");
  ping();  

  printf(" -- Query DPM Configuration --\n");
  query_conf();

	if (local) {
		printf(" -- Adding a pool --\n");

		printf(" -- Modify a pool --\n");

		printf(" -- Add a filesystem --\n");

		printf(" -- Remove a filesystem --\n");

		printf(" -- Remove a pool --\n");
	}

	printf(" -- Reserve space with a token description --\n");
	reserve_space_token(tk_desc);

	printf(" -- Get all space tokens from this user --\n");
	replies = get_space_token(NULL);

	printf(" -- Get space metada --\n");
	get_space_metada(stokens,replies);
		
	printf(" -- Release all space tokens from this user --\n");
	release_reserved_space(stokens,replies);

	printf(" -- Cleaning --\n");
	cleanup();

  exit(0); 
}
