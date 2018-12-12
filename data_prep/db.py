from sqlalchemy import JSON, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///simpsons.sqlite3", echo=False)
Base = declarative_base()


Session = sessionmaker(bind=engine)


class CharacterModel(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    page_id = Column(Integer, unique=True, nullable=False, index=True)
    descr = Column(String)
    aliases = Column(String)
    response = Column(String)
    response_html = Column(String)
    tokenized_descr = Column(String)

    def __repr__(self):
        return f"<CaracterModel(name={self.name}, pageID={self.page_id})>"


class EpisodeModel(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    page_id = Column(Integer, unique=True, nullable=False, index=True)
    response_appearances = Column(String)
    response_quotes = Column(String)
    tokenized_quotes = Column(String)

    def __repr__(self):
        return f"<CaracterModel(name={self.name}, pageID={self.page_id})>"


Base.metadata.create_all(engine)
