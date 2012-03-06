/********************************************************************************
** Form generated from reading UI file 'essaysafedesktopclient.ui'
**
** Created: Sun Mar 4 17:41:35 2012
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
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QMainWindow>
#include <QtGui/QWidget>
#include "mybutton.h"

QT_BEGIN_NAMESPACE

class Ui_EssaySafeDesktopClientClass
{
public:
    QWidget *centralWidget;
    MyButton *pushButton;
    QLineEdit *lineEdit;
    QLineEdit *lineEdit_2;
    QLineEdit *lineEdit_3;
    QLabel *label;
    QLabel *label_2;
    QLabel *label_3;

    void setupUi(QMainWindow *EssaySafeDesktopClientClass)
    {
        if (EssaySafeDesktopClientClass->objectName().isEmpty())
            EssaySafeDesktopClientClass->setObjectName(QString::fromUtf8("EssaySafeDesktopClientClass"));
        EssaySafeDesktopClientClass->resize(533, 340);
        EssaySafeDesktopClientClass->setDocumentMode(false);
        centralWidget = new QWidget(EssaySafeDesktopClientClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        pushButton = new MyButton(centralWidget);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(180, 190, 151, 91));
        pushButton->setDefault(false);
        pushButton->setFlat(false);
        lineEdit = new QLineEdit(centralWidget);
        lineEdit->setObjectName(QString::fromUtf8("lineEdit"));
        lineEdit->setGeometry(QRect(280, 40, 113, 22));
        lineEdit_2 = new QLineEdit(centralWidget);
        lineEdit_2->setObjectName(QString::fromUtf8("lineEdit_2"));
        lineEdit_2->setGeometry(QRect(280, 80, 113, 22));
        lineEdit_3 = new QLineEdit(centralWidget);
        lineEdit_3->setObjectName(QString::fromUtf8("lineEdit_3"));
        lineEdit_3->setGeometry(QRect(280, 120, 113, 22));
        label = new QLabel(centralWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(120, 40, 71, 16));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(120, 80, 61, 16));
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(120, 120, 53, 16));
        EssaySafeDesktopClientClass->setCentralWidget(centralWidget);

        retranslateUi(EssaySafeDesktopClientClass);
        QObject::connect(EssaySafeDesktopClientClass, SIGNAL(changeText(QString)), pushButton, SLOT(changeText(QString)));
        QObject::connect(pushButton, SIGNAL(clicked()), EssaySafeDesktopClientClass, SLOT(buttonClicked()));
        QObject::connect(EssaySafeDesktopClientClass, SIGNAL(getText()), lineEdit_3, SLOT(getText()));
        QObject::connect(EssaySafeDesktopClientClass, SIGNAL(getText()), lineEdit_2, SLOT(getText()));
        QObject::connect(EssaySafeDesktopClientClass, SIGNAL(getText()), lineEdit, SLOT(getText()));
        QObject::connect(lineEdit, SIGNAL(sendText(QString)), EssaySafeDesktopClientClass, SLOT(receiveText(QString)));

        QMetaObject::connectSlotsByName(EssaySafeDesktopClientClass);
    } // setupUi

    void retranslateUi(QMainWindow *EssaySafeDesktopClientClass)
    {
        EssaySafeDesktopClientClass->setWindowTitle(QApplication::translate("EssaySafeDesktopClientClass", "EssaySafeDesktopClient", 0, QApplication::UnicodeUTF8));
        pushButton->setText(QApplication::translate("EssaySafeDesktopClientClass", "Start Test", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("EssaySafeDesktopClientClass", "Essay Name", 0, QApplication::UnicodeUTF8));
        label_2->setText(QApplication::translate("EssaySafeDesktopClientClass", "Full Name", 0, QApplication::UnicodeUTF8));
        label_3->setText(QApplication::translate("EssaySafeDesktopClientClass", "Gmail", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class EssaySafeDesktopClientClass: public Ui_EssaySafeDesktopClientClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ESSAYSAFEDESKTOPCLIENT_H
