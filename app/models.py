from core.database import Base
from sqlalchemy import Numeric, Column, Integer, String, DateTime, Text


class QrNotes(Base):
    __tablename__ = "qr_notes"

    id = Column(String, primary_key=True, index=True, autoincrement=True)
    qr = Column(Text)
    title = Column(Text)
    description = Column(Text)
