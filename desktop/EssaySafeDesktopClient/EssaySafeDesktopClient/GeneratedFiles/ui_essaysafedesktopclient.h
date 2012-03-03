/********************************************************************************
** Form generated from reading UI file 'essaysafedesktopclient.ui'
**
** Created: Sat Mar 3 14:08:02 2012
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
#include <QtGui/QMenuBar>
#include <QtGui/QStatusBar>
#include <QtGui/QToolBar>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_EssaySafeDesktopClientClass
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *EssaySafeDesktopClientClass)
    {
        if (EssaySafeDesktopClientClass->objectName().isEmpty())
            EssaySafeDesktopClientClass->setObjectName(QString::fromUtf8("EssaySafeDesktopClientClass"));
        EssaySafeDesktopClientClass->resize(600, 400);
        menuBar = new QMenuBar(EssaySafeDesktopClientClass);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        EssaySafeDesktopClientClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(EssaySafeDesktopClientClass);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        EssaySafeDesktopClientClass->addToolBar(mainToolBar);
        centralWidget = new QWidget(EssaySafeDesktopClientClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        EssaySafeDesktopClientClass->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(EssaySafeDesktopClientClass);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        EssaySafeDesktopClientClass->setStatusBar(statusBar);

        retranslateUi(EssaySafeDesktopClientClass);

        QMetaObject::connectSlotsByName(EssaySafeDesktopClientClass);
    } // setupUi

    void retranslateUi(QMainWindow *EssaySafeDesktopClientClass)
    {
        EssaySafeDesktopClientClass->setWindowTitle(QApplication::translate("EssaySafeDesktopClientClass", "EssaySafeDesktopClient", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class EssaySafeDesktopClientClass: public Ui_EssaySafeDesktopClientClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ESSAYSAFEDESKTOPCLIENT_H
