#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>

int
get_plugin_info(int opcode, char *buf, int buflen)
{ 
  char cmd[1024];
  switch(opcode) {
  case 0:
    strncpy(buf, "simple output plugin", buflen);
    break;
  }
  sprintf(cmd, "python3 vgui.py");

  system(cmd);
  return 0;
}
void
result_best_str(char *result_str, char *stm)
{
  char use[1024];
  char cmd[1024];
  if (result_str == NULL) {
    printf("[failed]\n");
  } else {

    printf("%s\n", result_str);
    printf("%c\n", result_str[4]);

    sprintf(cmd, "%s\n", result_str);

    system(cmd);
/*
    if ('b' == result_str[4]) {
      //sprintf(cmd, "open -a Safari https://www.google.co.jp/");
      sprintf(cmd, "python3 ~/browser.py");

      system(cmd);
    }
    if ('p' == result_str[4]) {
      sprintf(cmd, "open ~/test.jpg");

      system(cmd);
    }
    if ('t' == result_str[4]) {
      sprintf(cmd, "open -a MacVim ~/test.c -n");

      system(cmd);
    }
    if ('y' == result_str[4]) {
      sprintf(cmd, "open -a Safari https://youtu.be/cMRYfNTlpqo");

      system(cmd);
    }
*/
  }
}
