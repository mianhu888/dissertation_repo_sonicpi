from flask import Flask, request
from model import db_connect, create_table, MainEventTable, CodeStates
from sqlalchemy.orm import sessionmaker
import logging
from random import randint
import json
import time

app = Flask(__name__)
logging.getLogger().setLevel(logging.INFO)


@app.route('/', methods=['POST'])
# @app.route('/')
def hello_world():
    if(request.form.get('request_id')):
        return idGen()
    elif(request.form.get('uploadJSON')):
        jsonStr = request.form.get('uploadJSON')
        return process_uploaded_json(jsonStr)
    else:
        return "Hello_world"


def process_uploaded_json(jsonStr):
    print(jsonStr)
    jsonStrList = list(jsonStr.split("\n,"))
    jsonCleanedList = []
    for item in jsonStrList:
        if(item):
            b = json.loads(item)
            jsonCleanedList.append(b)
            print(b)
    return insert_to_main_table(jsonCleanedList)


def alignLocalTime(jsonCleanedList):
    localTimeStampList = []
    serverTimeStampList = []
    timeIntevel = 0
    for item in jsonCleanedList:
        localTimeStampList.append(item.get("LocalTimeStamp", "nan"))
    i = len(localTimeStampList) - 1
    now = int(time.time())
    serverTimeStampList.append(now)
    while True:
        if i == -1:
            break
        timeIntevel = localTimeStampList[i] - localTimeStampList[i - 1]
        serverTimeStampList.insert(0, now - timeIntevel)


def alignLocalTime(jsonCleanedList):
    i = len(jsonCleanedList) - 1
    jsonCleanedList[i]["ServerTimeStamp"] = int(time.time())
    while True:
        if i == 0:
            break
        serverTimeStamp = jsonCleanedList[i]["ServerTimeStamp"] - \
            int(jsonCleanedList[i]["LocalTimeStamp"]) + \
            int(jsonCleanedList[i - 1]["LocalTimeStamp"])
        jsonCleanedList[i - 1]["ServerTimeStamp"] = serverTimeStamp
        i -= 1
    return jsonCleanedList


def insert_to_main_table(jsonCleanedList):
    jsonCleanedList = alignLocalTime(jsonCleanedList)
    engine = db_connect()
    create_table(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    commit_count = 0
    logging.info("****insert_to_main_table: session start****")
    try:
        for item in jsonCleanedList:
            mainTable = MainEventTable()
            mainTable.subjectID = item.get("SubjectID", "nan")
            mainTable.toolInstances = item.get("ToolInstances", "nan")
            mainTable.localTimeStamp = item.get("LocalTimeStamp", "nan")
            mainTable.serverTimeStamp = str(item.get("ServerTimeStamp", "nan"))
            mainTable.eventType = item.get("EventType", "nan")
            mainTable.compileMessageData = item.get(
                "CompileMessageData", "nan")
            mainTable.compileMessageType = item.get(
                "CompileMessageType", "nan")
            mainTable.resourceViewTitle = item.get("ResourceViewTitle", "nan")
            mainTable.editType = item.get("EditType", "nan")
            mainTable.clipboardContent = item.get("ClipboardContent", "nan")
            mainTable.editContent = item.get("EditContent", "nan")
            exist_code = db_session.query(CodeStates).filter_by(code = item.get("Code", "nan")).first()
            if exist_code is not None:
                mainTable.codeStates = exist_code
            else:
                mainTable.codeStates = CodeStates(code = item.get("Code", "nan"))
            print(mainTable.eventType)
            db_session.add(mainTable)
            db_session.commit()
            commit_count = commit_count + 1
    except:
        db_session.rollback()
        commit_count = -1
        raise
    finally:
        db_session.close()
        logging.info("****insert_to_main_table: session closed****")

    return str(commit_count)


def query_from_main_table(**kw):
    engine = db_connect()
    create_table(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    logging.info("****query_from_main_table: session start****")
    try:
        print("Query: ", kw)
        main_event_table = db_session.query(
            MainEventTable).filter_by(**kw).first()
    except:
        raise
    finally:
        db_session.close()
        logging.info("****query_from_main_table: session closed****")

    return main_event_table


# Generate a random string of length KEY_LEN, which is not repeated in database
def idGen():
    KEY_LEN = 8
    # Exclude l, o, 0, 1.
    CHARS = "abcdefghijkmnpqrstuvwxyzABCDEFGHIJKMNPQRSTUVWXYZ23456789"
    max_index = len(CHARS) - 1
    id = "".join([CHARS[randint(0, max_index)] for x in range(KEY_LEN)])
    while(query_from_main_table(subjectID=id) is not None):
        id = "".join([CHARS[randint(0, max_index)] for x in range(KEY_LEN)])
    return id
