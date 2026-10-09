from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class SubProject(Base):
    __tablename__ = "subprojects"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(String(300), nullable=False)
    description = Column(Text)

    manager_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String(50), default="NOT_STARTED")
    progress_percent = Column(Float, default=0)

    start_date = Column(Date)
    end_date = Column(Date)

    project = relationship(
        "Project",
        back_populates="subprojects"
    )

    manager = relationship("User")