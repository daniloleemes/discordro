#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <netinet/tcp.h>
#include <net/if.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <netdb.h>
#include <arpa/inet.h>

const char* error_msg(void)
{
	static char buf[512];
	int code = errno;
	snprintf(buf, sizeof(buf), "error %d: %s", code, strerror(code));
	return buf;
}

int main() {
    int s;
    struct sockaddr_in remote;
    int res;
    fd_set readfds;

    s = socket(AF_INET, SOCK_STREAM, 0);
    printf("S is %d\n", s);

    remote.sin_family = AF_INET;
    remote.sin_addr.s_addr = htonl(inet_addr("127.0.0.1"));
    remote.sin_port = htons(5131);

    res = connect(s, (struct sockaddr *)(&remote), sizeof(struct sockaddr_in));

    printf("res is %d\n", res);
    if (res) {
        printf("Socket #%d %s", s, error_msg());
    }

    FD_SET(s, &readfds);

    char data[] = "\x0f&s1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\xa8""D\x01\x0b\x14";
    res = send(s, data, 56, 0);
    printf("res is %d\n", res);

    close(s);
    return 0;
}