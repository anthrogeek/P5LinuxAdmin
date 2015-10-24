import sys
#all needed information for sqlalchemy to work on app.
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

#Creates user database to store login credentials from google and facebook.
class User(Base):
	__tablename__ = 'bookuser'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250))

#Creates the Genre categories table.
class Genre(Base):
	__tablename__ = 'genre'
	
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('bookuser.id'))
	user = relationship(User)

#Creates the table that stores all the book information.
class BookItem(Base):
	__tablename__ = 'book_item'

	name = Column(String(250), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	price = Column(String(8))
	author = Column(String(250))
	genre_id = Column(Integer, ForeignKey('genre.id', ondelete='CASCADE'))
	genre = relationship(Genre)
	user_id = Column(Integer, ForeignKey('bookuser.id'))
	user = relationship(User)


	


#Sets up the information for JSON
	@property
	def serialize(self):
		#Returns object data in an easily serialized format
		return {
			'name' : self.name,
			'description' : self.description,
			'price' : self.price,
			'author' : self.author,
			'id' : self.id,
			'genre' : self.genre.name,
		}


#Shows what and where the database is.
engine = create_engine(
'postgresql://postgres:postgres@localhost/catalog')

Base.metadata.create_all(engine)