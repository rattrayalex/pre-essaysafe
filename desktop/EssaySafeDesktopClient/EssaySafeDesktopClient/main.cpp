#include "essaysafedesktopclient.h"
#include <QtGui/QApplication>
#include <windows.h>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	EssaySafeDesktopClient w;
	w.show();
	int Dummy = 0;
	SystemParametersInfo (SPI_SETSCREENSAVERRUNNING, TRUE, NULL, 0);
	cout<<"No alt tab?";
	while(1)
		if(GetAsyncKeyState(VK_TAB) && GetAsyncKeyState(VK_MENU))
			cout<<"Alt-Tab";
	//Sleep(3000);
	cout<<"back";
	/*bool isMyKeyComboTrapped = RegisterHotKey(NULL, 100, MOD_ALT, VK_TAB);
	std::cout<<isMyKeyComboTrapped; 

	isMyKeyComboTrapped = UnregisterHotKey(NULL, 100);
	std::cout<<isMyKeyComboTrapped;*/
	return a.exec();
}
