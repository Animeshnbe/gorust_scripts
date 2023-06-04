#include <windows.h>
#include <stdio.h>

STARTUPINFOW si;
PROCESS_INFORMATION pi;
int main(void){
    // MessageBoxW(
    //     NULL,
    //     L"MY First Message Box",
    //     L"YIPPIE!",
    //     MB_ICONEXCLAMATION | MB_OKCANCEL
    // );

    if (!CreateProcessW(
        L"C:\\Windows\\System32\\notepad.exe",
        NULL,
        NULL,
        NULL,
        FALSE,
        BELOW_NORMAL_PRIORITY_CLASS,
        NULL,
        NULL,
        &si,
        &pi
    )){
        printf("Failed to create process, error: %ld", GetLastError());
        return EXIT_FAILURE;
    }
    printf("Process started, pid: %ld",pi.dwProcessId);
    return EXIT_SUCCESS;
}