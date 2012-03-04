#include "essaysafedesktopclient.h"
#include <iostream>

using namespace std;

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
    switch (wParam) {
        case VK_LWIN:
        case VK_RWIN:
		case VK_MENU:
		case VK_F11:
            bEatKeystroke = true;
            break;
		default:
			cout<<p->vkCode;
    }
	//1,0 = Windows button
	if( ((p->vkCode == 91) && (p->flags == 1)) || ((p->vkCode == 92) 
		&& (p->flags == 1)) || p->flags == LLKHF_ALTDOWN||p->vkCode == 122)
		bEatKeystroke = true;

    if( bEatKeystroke )
        return 1;
    else
        return CallNextHookEx( g_hKeyboardHook, nCode, wParam, lParam );
}

void GenerateKey ( int vk , BOOL bExtended)
{
  KEYBDINPUT  kb={0};
  INPUT    Input={0};
  // generate down 
  if ( bExtended )
    kb.dwFlags  = KEYEVENTF_EXTENDEDKEY;
  kb.wVk  = vk;  
  Input.type  = INPUT_KEYBOARD;

  Input.ki  = kb;
  ::SendInput(1,&Input,sizeof(Input));

  // generate up 
  ::ZeroMemory(&kb,sizeof(KEYBDINPUT));
  ::ZeroMemory(&Input,sizeof(INPUT));
  kb.dwFlags  =  KEYEVENTF_KEYUP;
  if ( bExtended )
    kb.dwFlags  |= KEYEVENTF_EXTENDEDKEY;

  kb.wVk    =  vk;
  Input.type  =  INPUT_KEYBOARD;
  Input.ki  =  kb;
  ::SendInput(1,&Input,sizeof(Input));
}





void EssaySafeDesktopClient::buttonClicked() {
	if(beforeTest) {
		beforeTest = false;
		system("\"C:\\Users\\Geoff\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe\" localhost:8080/take/Humanities101/Geoff/yefim323@gmail.com");
		GenerateKey(VK_F11, false);
		emit changeText("Stop Test");
		g_hKeyboardHook = SetWindowsHookEx( WH_KEYBOARD_LL,  LowLevelKeyboardProc, GetModuleHandle(NULL), 0 );

	}
	else {
		UnhookWindowsHookEx( g_hKeyboardHook );
		exit(0);
	}
}