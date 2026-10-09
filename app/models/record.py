from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class KnowledgeRecord(Base):
    __tablename__ = "knowledge_records"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    type = Column(String(100), nullable=False)
    title = Column(String(300), nullable=False)

    date = Column(Date)

    source = Column(String(300))

    description = Column(Text)

    file_path = Column(String(500))
    url = Column(String(1000))

    created_by = Column(Integer, ForeignKey("users.id"))

    project = relationship(
        "Project",
        back_populates="knowledge_records"
    )

    creator = relationship("User")