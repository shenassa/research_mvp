from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    subproject_id = Column(
        Integer,
        ForeignKey("subprojects.id"),
        nullable=True
    )

    title = Column(String(300), nullable=False)
    description = Column(Text)

    owner_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String(50), default="OPEN")
    next_action = Column(Text)

    project = relationship(
        "Project",
        back_populates="issues"
    )

    owner = relationship("User")