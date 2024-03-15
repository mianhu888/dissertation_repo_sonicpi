from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Text

Base = declarative_base()

# MySQL connection
CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
    drivername="mysql+pymysql",
    user="Your user",
    passwd="Your pass",
    host="localhost",
    port="3306",
    db_name="sonicpi",
)


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(CONNECTION_STRING)


def create_table(engine):
    Base.metadata.create_all(engine)


# Main event table
class MainEventTable(Base):
    __tablename__ = "main_event_table"

    eventID = Column("EventID", Integer, primary_key=True)
    eventType = Column("EventType", String(100))
    subjectID = Column("SubjectID", String(100))
    toolInstances = Column("ToolInstances", String(100))
    localTimeStamp = Column("LocalTimeStamp", String(15))
    serverTimeStamp = Column("ServerTimeStamp", String(15))
    compileMessageType = Column("CompileMessageType", String(100))
    compileMessageData = Column("CompileMessageData", Text)
    editType = Column("EditType", String(20))
    resourceViewTitle = Column("ResourceViewTitle", String(100))
    clipboardContent = Column("ClipboardContent", Text)
    editContent = Column("EditContent", Text)
    codeStateID = Column(Integer, ForeignKey("code_states.CodeStateID"))

    codeStates = relationship("CodeStates", backref="main_event_table")

    def __repr__(self):
        return "<MainEventTable(EventID=%r)>" % (self.eventID)


class CodeStates(Base):
    __tablename__ = "code_states"

    codeStateID = Column("CodeStateID", Integer, primary_key=True)
    code = Column("Code", Text)

    mainEventTable = relationship("MainEventTable", backref = "code_states")

    def __repr__(self):
        return "<CodeStates(CodeStateID=%r)>" % (self.codeStateID)
