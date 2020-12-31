/*
* Functions:		socket_create, receive_from_send_to_client
* 					
* Global variables:	SERVER_PORT, RX_BUFFER_SIZE, TX_BUFFER_SIZE, MAXCHAR,
* 					dest_addr, source_addr, rx_buffer, tx_buffer,
* 					ipv4_addr_str, ipv4_addr_str_client, listen_sock, line_data, input_fp, output_fp, currentnumber, nextnumber, pos, firsttime
* 					
*/



#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>


// Constants defined
#define SERVER_PORT 3333
#define RX_BUFFER_SIZE 1024
#define TX_BUFFER_SIZE 1024

#define MAXCHAR 1000				// max characters to read from txt file

// Global variables
struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;

char rx_buffer[RX_BUFFER_SIZE];		// buffer to store data from client
char tx_buffer[RX_BUFFER_SIZE];		// buffer to store data to be sent to client

char ipv4_addr_str[128];			// buffer to store IPv4 addresses as string
char ipv4_addr_str_client[128];		// buffer to store IPv4 addresses as string

int listen_sock;

char line_data[MAXCHAR];

FILE *input_fp, *output_fp;

int currentnumber, nextnumber=-1, pos;

int firsttime = 2;



/*
* Function Name:	socket_create
* Inputs:			dest_addr [ structure type for destination address ]
* 					source_addr [ structure type for source address ]
* Outputs: 			my_sock [ socket value, if connection is properly created ]
* Purpose: 			the function creates the socket connection with the server
* Example call: 	int sock = socket_create(dest_addr, source_addr);
*/
int socket_create(struct sockaddr_in dest_addr, struct sockaddr_in source_addr){

	int addr_family;
	int ip_protocol;
	int addrlen = sizeof(source_addr);

	dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(SERVER_PORT);
	addr_family = AF_INET;
	ip_protocol = IPPROTO_IP;

	int my_sock, newsock;

	newsock = socket(addr_family, SOCK_STREAM, ip_protocol);
	if(newsock==0){
		printf("Error opening the socket");
		exit(1);
	}
	if(bind(newsock, (struct sockaddr*) &dest_addr, sizeof(dest_addr))!=0){
		printf("Error binding the socket!");
		exit(1);
	}
	if(listen(newsock, 1)!=0){
		printf("Error while calling the listen function!");
		exit(1);
	}

	if((my_sock = accept(newsock, (struct sockaddr*) &source_addr, (socklen_t*)&addrlen))<0){
		printf("Error in accepting a connection from the client");
	}
    listen_sock = newsock;
	return my_sock;
}


/*
* Function Name:	receive_from_send_to_client
* Inputs:			sock [ socket value, if connection is properly created ]
* Outputs: 			None
* Purpose: 			the function receives the data from server and updates the 'rx_buffer'
*					variable with it, sends the obstacle position based on obstacle_pos.txt
*					file and sends this information to the client in the provided format.
* Example call: 	receive_from_send_to_client(sock);
*/
int receive_from_send_to_client(int sock){
	memset(tx_buffer, 0 , sizeof(tx_buffer));
	memset(rx_buffer, 0 , sizeof(rx_buffer));

	char nextnum[10] = "";
	char tuple[100];

	int start, end;

	if(nextnumber==-1){
	while(line_data[pos]!=':')
	{
	    nextnum[pos] = line_data[pos];
	    pos+=1;
	}
	nextnum[pos] = 0;
	nextnumber = atoi(nextnum);   
	}

	int bytesread = read(sock, rx_buffer, MAXCHAR);

	if(currentnumber==nextnumber)
	{
	//we have entries in this line to be printed
	//read the next tuple
	//find the opening bracket
	while(line_data[pos++]!='(');
	start = pos-1;
	//find the closing paranthesis
	while(line_data[pos++]!=')');
	//send this to the client
	int k = 0;
	tx_buffer[k++] = '@';
	for(int i=start;i<pos;i++) tx_buffer[k++] = line_data[i];
	tx_buffer[k++] = '@';
	tx_buffer[k] = 0;
	send(sock, tx_buffer, sizeof(tx_buffer),0);
		


	if(line_data[pos]!=';'){
	    //read the next line from the file
			memset(line_data,0,sizeof(line_data));	
			if(fgets(line_data, MAXCHAR, input_fp)==NULL){
				strcpy(line_data, "0:");
			}
			if(strlen(line_data)<=5)
			{
				if(fgets(line_data, MAXCHAR, input_fp)==NULL){
				strcpy(line_data, "0:");
			}
			}
			pos = 0;
			nextnumber = -1;
	}

	}
	
	else{
	strcpy(tx_buffer, "@$@");
	send(sock, tx_buffer, sizeof(tx_buffer),0);
		currentnumber+=1;
		if(firsttime){
				firsttime = 0;
				fseek(input_fp, 0, SEEK_SET);
				memset(line_data, 0, sizeof(line_data));
				if(fgets(line_data, MAXCHAR, input_fp)==NULL){
				strcpy(line_data, "0:");
			}
				currentnumber = 0;
				nextnumber =-1;
		}
	}

	return 0;
}


/*
* Function Name:	main()
* Inputs:			None
* Outputs: 			None
* Purpose: 			the function solves Task 1B problem statement by making call to
* 					functions socket_create() and receive_from_send_to_client()
*/
int main() {
	
    char *input_file_name = "obstacle_pos.txt";
	char *output_file_name = "data_from_client.txt";

	// Create socket and accept connection from client
	int sock = socket_create(dest_addr, source_addr);

	input_fp = fopen(input_file_name, "r");

	if (input_fp == NULL){
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}

	fgets(line_data, MAXCHAR, input_fp);

	output_fp = fopen(output_file_name, "w");

	if (output_fp == NULL){
		printf("Could not open file %s\n",output_file_name);
		return 1;
	}

	while (1) {

		// Receive and send data from client and get the new shortest path
		receive_from_send_to_client(sock);
		
		fputs(rx_buffer, output_fp);
		fputs("\n", output_fp);

	}

	return 0;
}

