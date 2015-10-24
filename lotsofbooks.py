#!/usr/bin/python
# encoding=utf8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, BookItem, User

engine = create_engine('postgresql://postgres:postgres@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

bookuser1 = User(id =1, name="Udacity Grader", email="grader@udacity.com", picture = "none")
session.add(bookuser1)
session.commit()
# Books for Sci Fi
genre1 = Genre(name="Sci Fi")

session.add(genre1)
session.commit()

bookItem2 = BookItem(user_id=1, name="My Sister Keeper", description="The \
                     difficult choices a family must make when a child is \
                     diagnosed with a serious disease",
                     price="$7.50", author="Jody Picoult", genre=genre1)

session.add(bookItem2)
session.commit()


bookItem1 = BookItem(user_id=1, name="The E-Myth Revisited", description="How \
                     to win at business with systems",
                     price="$12.99", author="Michael E. Gerber", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(user_id=1, name="Leonardo's Notebooks", description="Notes \
                     from Leonardo DaVinci",
                     price="$5.50", author="Leonardo DaVinci", genre=genre1)

session.add(bookItem2)
session.commit()

bookItem3 = BookItem(user_id=1, name="Mindless Eating: Why We Eat More \
                     Than We Think", description="how to stop mindlessly eat",
                     price="$3.99", author="Brian Wansink", genre=genre1)

session.add(bookItem3)
session.commit()

bookItem4 = BookItem(user_id=1, name="Acres of Diamonds: Our Every-Day \
                     Opportunities", description="This is a pre-1923 \
                     historical reproduction that was curated for quality",
                     price="$7.99", author="Russell Conwell  ", genre=genre1)

session.add(bookItem4)
session.commit()

bookItem5 = BookItem(user_id=1, name="The Referral Engine: Teaching Your \
                     Business to Market Itself", description="The small \
                     business guru behind Duct Tape Marketing shares his \
                     most valuable lesson",
                     price="$1.99", author="John Jantsch", genre=genre1)

session.add(bookItem5)
session.commit()

bookItem6 = BookItem(user_id=1, name="Excuses Begone! How to Change Lifelong, \
                     Self-Defeating Thinking Habits", description="Traditional \
                     Chinese edition of EXCUSES BEGONE!How to Change Lifelong",
                     price="$.99", author="Wayne W. Dyer", genre=genre1)

session.add(bookItem6)
session.commit()

bookItem7 = BookItem(user_id=1, name="The New Small", description="A small \
                     seafood restaurant attracts new customers with virtually \
                     no marketing budget.",
                     price="$3.49", author="Phil Simon", genre=genre1)

session.add(bookItem7)
session.commit()

bookItem8 = BookItem(user_id=1, name="Stop Saying You're Fine: Discover a \
                     More Powerful You", description="Right now, over 100 \
                     million Americans secretly feel frustrated and bored \
                     with their lives.",
                     price="$5.99", author="Mel Robbins", genre=genre1)

session.add(bookItem8)
session.commit()


# Books for Romance
genre2 = Genre(name="Romance")

session.add(genre2)
session.commit()


bookItem1 = BookItem(user_id=1, name="Today We Are Rich: Harnessing The Power \
                     Of Total Confidence", description="The long awaited \
                     prequel to global best seller Love Is the Killer App",
                     price="$7.99", author="Tim Sanders", genre=genre2)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(user_id=1, name="The Flinch", description="A book so \
                     important we refuse to charge for it. Julien Smith has ",
                     price="$0", author="Julien Smith", genre=genre2)

session.add(bookItem2)
session.commit()


# Books for Thriller
genre1 = Genre(name="Thriller")

session.add(genre1)
session.commit()


bookItem1 = BookItem(user_id=1, name="The $100 Startup", description="Reinvent \
                     the Way You Make a Living, Do What You Love, and \
                     Create a New Future.",
                     price="$8.99", author="Chris Guillebeau", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(user_id=1, name="The 4-Hour Chef: ", description="The \
                     Simple Path to Cooking Like a Pro, Learning Anything, \
                     and Living the Good Life.",
                     price="$6.99", author="Tim Ferris", genre=genre1)

session.add(bookItem2)
session.commit()


# Books for Business
genre1 = Genre(name="Business ")

session.add(genre1)
session.commit()


bookItem1 = BookItem(user_id=1, name="Refuse to Choose!:", description=" Use \
                     All of Your Interests, Passions, and Hobbies to Create \
                     the Life and Career of Your Dreams",
                     price="$2.99", author="Barbara Sher", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(user_id=1, name="Let Go", description="Let Go is \
                     Pat Flynn's touching memoir about overcoming adversity \
                     through a commitment to pursuing your own path.",
                     price="$5.99", author="Pat Flynn", genre=genre1)

session.add(bookItem2)
session.commit()


# Children's Books
genre1 = Genre(name="Childres\'s Books ")

session.add(genre1)
session.commit()


bookItem1 = BookItem(user_id=1, name="The Good Energy Book:", description=" \
                     Creating Harmony and Balance for Yourself and Your Home",
                     price="$13.95", author="Tess Whitehurst", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(user_id=1, name="Walden", description="Henry David \
                     Thoreau's classic, first published in 1854 and reporting \
                     on his experiences at the eponymous site ",
                     price="$4.95", author="Henry David Thoreau", genre=genre1)

session.add(bookItem2)
session.commit()


# Books for Arts and Crafts
genre1 = Genre(name="Arts and Crafts")

session.add(genre1)
session.commit()


bookItem1 = BookItem(user_id=1, name="Foodist: ", description="Using Real \
                     Food and Real Science to Lose Weight Without Dieting.",
                     price="$9.95", author="Darya Pino Rose", genre=genre1)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(user_id=1, name="Choose Yourself", description="The world \
                     is changing. Market have crashed. Jobs have disappeared.",
                     price="$7.95", author="James Altucher", genre=genre1)

session.add(bookItem2)
session.commit()

# Books for Meditation
genre1 = Genre(name="Meditation ")

session.add(genre1)
session.commit()

bookItem9 = BookItem(user_id=1, name="E-Squared: ", description="Nine Do-It- \
                     Yourself Energy Experiments That Prove Your Thoughts \
                     Create Your Reality",
                     price="$8.99", author="Pam Grout", genre=genre1)

session.add(bookItem9)
session.commit()


print "added menu items!"
