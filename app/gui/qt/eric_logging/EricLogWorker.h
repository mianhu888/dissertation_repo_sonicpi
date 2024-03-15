#ifndef ERICLOGWORKER_H
#define ERICLOGWORKER_H

#include <QEventLoop>
#include <QFuture>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QThread>
#include <QTimer>

class QString;
class QByteArray;

class EricLogWorker : public QObject
{
    Q_OBJECT

public:
    EricLogWorker();
    ~EricLogWorker();

public slots:
    QString requestGet();
    QString requestPost(QString, QString, bool);
    QString uploadLog(QVector<QString>);
    void endFunction();

signals:
    void finished();
};
#endif // !ERICLOGWORKER_H
