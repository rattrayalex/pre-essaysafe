#include "essaysafedesktopclient.h"

HHOOK g_hKeyboardHook;

EssaySafeDesktopClient::EssaySafeDesktopClient(QWidget *parent, Qt::WFlags flags)
	: QMainWindow(parent, flags)
{
	beforeTest = true;
	ui.setupUi(this);
}

EssaySafeDesktopClient::~EssaySafeDesktopClient()
{

}

LRESULT CALLBACK LowLevelKeyboardProc( int nCode, WPARAM wParam, LPARAM lParam )
{
    if (nCode < 0 || nCode != HC_ACTION )  // do not process message 
        return CallNextHookEx( g_hKeyboardHook, nCode, wParam, lParam); 
 
    bool bEatKeystroke = false;
    KBDLLHOOKSTRUCT* p = (KBDLLHOOKSTRUCT*)lParam;
    switch (wParam) 
    {
        case WM_KEYDOWN:  
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

void EssaySafeDesktopClient::buttonClicked() {
	if(beforeTest) {
		beforeTest = false;
		emit changeText("Stop Test");
		g_hKeyboardHook = SetWindowsHookEx( WH_KEYBOARD_LL,  LowLevelKeyboardProc, GetModuleHandle(NULL), 0 );
	}
	else {
		UnhookWindowsHookEx( g_hKeyboardHook );
		exit(0);
	}
}