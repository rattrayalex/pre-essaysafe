#include <QLineEdit>
#include <qstring.h>

class MyText : public QLineEdit {
	Q_OBJECT
	public:
		MyText(QWidget*);

	public slots:
		void getText();

	signals:
		void sendText(QString);
    
};