#include "EricLogWorker.h"

EricLogWorker::EricLogWorker()
{
    qDebug() << "init EricLogWorker";
}

EricLogWorker::~EricLogWorker()
{
}

QString EricLogWorker::requestGet()
{
    QNetworkRequest request;
    request.setUrl(QUrl("http://127.0.0.1:5000/"));
    //request.setUrl(QUrl("https://sonorous-veld-288216.ue.r.appspot.com/"));
    QNetworkAccessManager* manager = new QNetworkAccessManager();
    QNetworkReply* reply = manager->get(request);
    QEventLoop eventLoop;
    QObject::connect(manager, SIGNAL(finished(QNetworkReply*)), &eventLoop, SLOT(quit()));
    eventLoop.exec();
    QString string = QString::fromUtf8(reply->readAll());
    qDebug() << "------------" << string;
    return string;
}

QString EricLogWorker::requestPost(QString kw, QString postString, bool routine)
{
    qDebug() << "------------start_post";
    QByteArray postArray;
    postArray.append(kw + "=" + postString);
    QNetworkRequest request;
    request.setUrl(QUrl("http://127.0.0.1:5000/"));
    //request.setUrl(QUrl("https://sonorous-veld-288216.ue.r.appspot.com/"));
    QNetworkAccessManager* manager = new QNetworkAccessManager();
    QNetworkReply* reply = manager->post(request, postArray);
    QEventLoop eventLoop;
    QObject::connect(manager, SIGNAL(finished(QNetworkReply*)), &eventLoop, SLOT(quit()));
    eventLoop.exec();
    QString responseString = QString::fromUtf8(reply->readAll());
    qDebug() << "------------" << responseString;
    if (routine == false)
    {
        emit finished();
        qDebug() << "emit finished";
    }
    return responseString;
}

void EricLogWorker::endFunction()
{
    qDebug() << "end function";
}

QString EricLogWorker::uploadLog(QVector<QString> logVector)
{
    QString str;
    for (int i = 0; i < logVector.size(); i++)
    {
        str = str + logVector.at(i) + ",";
    }
    QString queryCount = requestPost(QString("uploadJSON"), str, true);
    qDebug() << "upload callback in EricLogWorker.uploadLog" << queryCount;
    return queryCount;
}