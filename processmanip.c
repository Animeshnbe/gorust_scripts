// program to demonstrate OpenProcess of the Win32 API

#include <windows.h>
#include <stdio.h>

int main(int argc, char *argv[]){
    HANDLE hProcess;
    DWORD dwProcessId;
    char buf[1024];
    int i;
    
    if (argc < 2){
        printf("Usage: %s <pid>\n", argv[0]);
        return 1;
    }
    
    dwProcessId = atoi(argv[1]);
    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwProcessId);
    
    if (hProcess == NULL){
        printf("OpenProcess failed\n");
        return 1;
    }
    
    for (i = 0; i < 1024; i++){
        if (ReadProcessMemory(hProcess, buf, &buf[i], 1, NULL)){
            printf("%c", buf[i]);
        }
    }
    
    CloseHandle(hProcess);
    return 0;
}

// demo comment to test: Run gcc processmanip.c 