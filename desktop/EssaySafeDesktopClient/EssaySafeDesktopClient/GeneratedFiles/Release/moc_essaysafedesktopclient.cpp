/****************************************************************************
** Meta object code from reading C++ file 'essaysafedesktopclient.h'
**
** Created: Sun Mar 4 00:49:42 2012
**      by: The Qt Meta Object Compiler version 63 (Qt 4.8.0)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../essaysafedesktopclient.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'essaysafedesktopclient.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 63
#error "This file was generated using the moc from 4.8.0. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_EssaySafeDesktopClient[] = {

 // content:
       6,       // revision
       0,       // classname
       0,    0, // classinfo
       2,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: signature, parameters, type, tag, flags
      24,   23,   23,   23, 0x05,

 // slots: signature, parameters, type, tag, flags
      44,   23,   23,   23, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_EssaySafeDesktopClient[] = {
    "EssaySafeDesktopClient\0\0changeText(QString)\0"
    "buttonClicked()\0"
};

void EssaySafeDesktopClient::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        Q_ASSERT(staticMetaObject.cast(_o));
        EssaySafeDesktopClient *_t = static_cast<EssaySafeDesktopClient *>(_o);
        switch (_id) {
        case 0: _t->changeText((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 1: _t->buttonClicked(); break;
        default: ;
        }
    }
}

const QMetaObjectExtraData EssaySafeDesktopClient::staticMetaObjectExtraData = {
    0,  qt_static_metacall 
};

const QMetaObject EssaySafeDesktopClient::staticMetaObject = {
    { &QMainWindow::staticMetaObject, qt_meta_stringdata_EssaySafeDesktopClient,
      qt_meta_data_EssaySafeDesktopClient, &staticMetaObjectExtraData }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &EssaySafeDesktopClient::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *EssaySafeDesktopClient::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *EssaySafeDesktopClient::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_EssaySafeDesktopClient))
        return static_cast<void*>(const_cast< EssaySafeDesktopClient*>(this));
    return QMainWindow::qt_metacast(_clname);
}

int EssaySafeDesktopClient::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 2)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 2;
    }
    return _id;
}

// SIGNAL 0
void EssaySafeDesktopClient::changeText(QString _t1)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
QT_END_MOC_NAMESPACE
