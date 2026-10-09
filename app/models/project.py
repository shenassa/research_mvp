from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(300), nullable=False)
    description = Column(Text)

    objectives = Column(Text)
    outputs = Column(Text)

    manager_id = Column(Integer, ForeignKey("users.id"))
    owner_department_id = Column(Integer, ForeignKey("departments.id"))

    beneficiary = Column(String(300))
    beneficiary_department_id = Column(Integer, ForeignKey("departments.id"))

    status = Column(String(50), default="NOT_STARTED")
    progress_percent = Column(Float, default=0)

    start_date = Column(Date)
    end_date = Column(Date)

    manager = relationship(
        "User",
        foreign_keys=[manager_id]
    )

    owner_department = relationship(
        "Department",
        foreign_keys=[owner_department_id]
    )

    beneficiary_department = relationship(
        "Department",
        foreign_keys=[beneficiary_department_id]
    )

    subprojects = relationship(
        "SubProject",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    issues = relationship(
        "Issue",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    knowledge_records = relationship(
        "KnowledgeRecord",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    participants = relationship(
        "ProjectParticipant",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class ProjectParticipant(Base):
    __tablename__ = "project_participants"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    name = Column(String(200), nullable=False)
    organization = Column(String(300))
    role = Column(String(200))

    project = relationship(
        "Project",
        back_populates="participants"
    )