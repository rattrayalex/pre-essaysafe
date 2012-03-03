#ifndef ESSAYSAFEDESKTOPCLIENT_H
#define ESSAYSAFEDESKTOPCLIENT_H

#include <QtGui/QMainWindow>
#include "ui_essaysafedesktopclient.h"

class EssaySafeDesktopClient : public QMainWindow
{
	Q_OBJECT

public:
	EssaySafeDesktopClient(QWidget *parent = 0, Qt::WFlags flags = 0);
	~EssaySafeDesktopClient();

private:
	Ui::EssaySafeDesktopClientClass ui;
};

#endif // ESSAYSAFEDESKTOPCLIENT_H
