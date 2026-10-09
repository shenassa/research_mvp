from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Matrix(Base):
    __tablename__ = "matrices"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(String(300), nullable=False)

    items = relationship(
        "MatrixItem",
        back_populates="matrix",
        cascade="all, delete-orphan"
    )


class MatrixItem(Base):
    __tablename__ = "matrix_items"

    id = Column(Integer, primary_key=True, index=True)

    matrix_id = Column(
        Integer,
        ForeignKey("matrices.id"),
        nullable=False
    )

    subject = Column(String(300), nullable=False)
    responsible = Column(String(200))
    status = Column(String(50), default="OPEN")
    next_action = Column(Text)
    deadline = Column(String(20))

    matrix = relationship(
        "Matrix",
        back_populates="items"
    )