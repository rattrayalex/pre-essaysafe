#ifndef ESSAYSAFEDESKTOPCLIENT_H
#define ESSAYSAFEDESKTOPCLIENT_H

#include <QtGui/QMainWindow>
#include "ui_essaysafedesktopclient.h"
#include <Windows.h>

class EssaySafeDesktopClient : public QMainWindow {
	Q_OBJECT

	public:
		EssaySafeDesktopClient(QWidget *parent = 0, Qt::WFlags flags = 0);
		~EssaySafeDesktopClient();

	private:
		Ui::EssaySafeDesktopClientClass ui;
		bool beforeTest;


	signals:
		void changeText(QString);

	public slots:
		void buttonClicked();


};

#endif // ESSAYSAFEDESKTOPCLIENT_H
