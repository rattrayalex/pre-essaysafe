/********************************************************************************
** Form generated from reading UI file 'essaysafedesktopclient.ui'
**
** Created: Sun Mar 4 00:40:37 2012
**      by: Qt User Interface Compiler version 4.8.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ESSAYSAFEDESKTOPCLIENT_H
#define UI_ESSAYSAFEDESKTOPCLIENT_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QHeaderView>
#include <QtGui/QMainWindow>
#include <QtGui/QWidget>
#include "mybutton.h"

QT_BEGIN_NAMESPACE

class Ui_EssaySafeDesktopClientClass
{
public:
    QWidget *centralWidget;
    MyButton *pushButton;

    void setupUi(QMainWindow *EssaySafeDesktopClientClass)
    {
        if (EssaySafeDesktopClientClass->objectName().isEmpty())
            EssaySafeDesktopClientClass->setObjectName(QString::fromUtf8("EssaySafeDesktopClientClass"));
        EssaySafeDesktopClientClass->resize(600, 400);
        EssaySafeDesktopClientClass->setDocumentMode(false);
        centralWidget = new QWidget(EssaySafeDesktopClientClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        pushButton = new MyButton(centralWidget);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(190, 130, 231, 141));
        pushButton->setDefault(false);
        pushButton->setFlat(false);
        EssaySafeDesktopClientClass->setCentralWidget(centralWidget);

        retranslateUi(EssaySafeDesktopClientClass);
        QObject::connect(EssaySafeDesktopClientClass, SIGNAL(changeText(QString)), pushButton, SLOT(changeText(QString)));
        QObject::connect(pushButton, SIGNAL(clicked()), EssaySafeDesktopClientClass, SLOT(buttonClicked()));

        QMetaObject::connectSlotsByName(EssaySafeDesktopClientClass);
    } // setupUi

    void retranslateUi(QMainWindow *EssaySafeDesktopClientClass)
    {
        EssaySafeDesktopClientClass->setWindowTitle(QApplication::translate("EssaySafeDesktopClientClass", "EssaySafeDesktopClient", 0, QApplication::UnicodeUTF8));
        pushButton->setText(QApplication::translate("EssaySafeDesktopClientClass", "Start Test", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class EssaySafeDesktopClientClass: public Ui_EssaySafeDesktopClientClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ESSAYSAFEDESKTOPCLIENT_H
