#include "essaysafedesktopclient.h"
#include <QtGui/QApplication>
#include <iostream>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	EssaySafeDesktopClient w;
	w.show();
    
	return a.exec();
}
 