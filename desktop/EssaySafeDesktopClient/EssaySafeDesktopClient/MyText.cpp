#include "MyText.h"

MyText::MyText(QWidget *parent) : QLineEdit(parent) {}

void MyText::getText() {
	emit sendText(text());
}