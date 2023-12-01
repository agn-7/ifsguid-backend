import uuid

from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import as_declarative, declared_attr, relationship
from sqlalchemy.dialects.postgresql import UUID

from . import utils


@as_declarative()
class Base(object):
    """A class describing the declarative base of the model classes

    Attributes
    ----------
    id: int
        The primary key of a an instance of Base
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """A declared attribute for __tablename__

        The __tablename__ for a classed derived from Base is its own name in
        lowercase by default.

        Returns
        -------
        str
            The class name in lowercase
        """

        return str(cls.__name__.lower())

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )


class Interaction(Base):
    created_at = Column(
        DateTime(timezone=True), index=True, default=utils.datetime_now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        index=True,
        default=utils.datetime_now(),
        onupdate=utils.datetime_now(),
    )
    settings = Column(JSON)

    messages = relationship("Message", back_populates="interaction", lazy="selectin")


class Message(Base):
    created_at = Column(
        DateTime(timezone=True), index=True, default=utils.datetime_now()
    )
    role = Column(String, index=True)
    content = Column(String)
    interaction_id = Column(String, ForeignKey("interaction.id"))

    interaction = relationship("Interaction", back_populates="messages")
