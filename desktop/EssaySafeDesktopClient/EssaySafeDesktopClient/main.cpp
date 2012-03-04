#include "essaysafedesktopclient.h"
#include <QtGui/QApplication>
#include <windows.h>
#include <iostream>

using namespace std;

HHOOK g_hKeyboardHook;
BOOL g_bFullscreen;

LRESULT CALLBACK LowLevelKeyboardProc( int nCode, WPARAM wParam, LPARAM lParam )
{
    bool bEatKeystroke = false;
    KBDLLHOOKSTRUCT* p = (KBDLLHOOKSTRUCT*)lParam;
    switch (wParam)
    {
        case WM_KEYDOWN:
		case WM_SYSKEYDOWN:
		case WM_SYSKEYUP:
        case WM_KEYUP:
		case VK_MENU:
		case VK_F11:
		case 0x4B:
        {
            bEatKeystroke = true;
            break;
        }

    }
 
    if( bEatKeystroke )
        return 1;
    else
        return CallNextHookEx( g_hKeyboardHook, nCode, wParam, lParam );
}

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	EssaySafeDesktopClient w;
	w.show();
    g_hKeyboardHook = SetWindowsHookEx( WH_KEYBOARD_LL,  LowLevelKeyboardProc, GetModuleHandle(NULL), 0 );
	Sleep(15000);
    UnhookWindowsHookEx( g_hKeyboardHook );
	return a.exec();
}
 