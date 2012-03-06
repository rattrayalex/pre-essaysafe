#include <QPushButton>
#include <qstring.h>

class MyButton : public QPushButton {
	Q_OBJECT
	public:
		MyButton(QWidget*);

	public slots:
		void changeText(QString);
    
};