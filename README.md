Algorithm 

The DNS client program uses a key and a challenge string to create a digest and sends the challenge string as well as the digest to the authentication server. The authentication sever, sends ONLY the challenge string to both the TLDS servers and the TLDS servers return the respective digests. The TLDS servers each store a key and only of them matches the key that the client used to create the digest. Hence, only one of the responses from the TLDS servers match the digest sent by the client. The Authentication server (root server) sends the hostname of the TLDS server with the correct match to the client. The DNS client then connects to that TLDS server with a query string and obtains the A record (if found) from the authenticated TLDS server. The two TS servers each maintain a DNS_table consisting of three fields: Hostname, IP address, Flag (A). In addition, the TS servers each maintain a key which is used to create a digest from a challenge. When the DNS client connects to the authenticated TLDS server, it sends the hostname as a string. The TLDS server does a look up in the DNS_table and if there is a match, sends the DNS table entry as a string [“Hostname IPaddress A”]. If the host name does not exist, then an error string Error: HOST NOT FOUND is returned. Note, that in this Project, the DNS client connects to the TLDS server to get the IP address for a given hostname. The hostname string, the Key and the challenge will be given one per line in a file (PROJ3-HNS.txt) and the keys one per line will be in a file PROJ3-KEY1.txt and PROJ3-KEY2.txt. The DNS tables entries will also be one per line and will be in PROJ3-TLDS1.txt and PROJ3-TLDS2.txt. The TLDS servers, in addition to reading the DNS entries, will each obtain its key by reading the value from the corresponding key files. TLDS1 will read the key from PROJ3-KEY1.txt and TLDS2 will read the key from PROJ3-KEY2.txt Your client program should output the results to a file RESOLVED.txt. As part of your submission, you need to submit four program files as well as the output file. The DNS client will read from PROJ3-HNS.txt. Each line will contain a key, a challenge and a hostname (k3521 arianna www.princeton.edu). Using the key and the challenge, the DNS client creates a digest. Then connects to the AS server and sends ONLY the challenge string and the digest to the AS server. The AS server then sends ONLY the challenge string to both the TLDS servers and collects the responses (digests). Then it does a digest compare and sends the name of the TLDS server that returns the correct digest. Note: as the keys read by the TLDS servers are different, only one digest will match. The DNS client then sends the hostname part of the query string to that TLDS server returned by the AS sever and writes the response received from the TLDS server and the hostname of the TLDS server to the output file RESOLVED.txt 

Procedure 

First start the two TLDS servers, then the AS server and then the client program. This will start communication of the port number and hostname of TS servers to the AS server and hostname of the AS server to the client program. Data structure for the DNS table as well as to store KEYS and digests is a text file
