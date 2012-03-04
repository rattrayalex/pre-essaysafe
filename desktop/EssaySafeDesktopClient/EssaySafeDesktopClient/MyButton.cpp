#include "MyButton.h"

MyButton::MyButton(QWidget *parent) : QPushButton(parent) {}

void MyButton::changeText(QString text) {
	setText(text);
}