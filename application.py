from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, BookItem, User

from flask import session as login_session
import random
import string

# Oauth imports
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('postgresql://postgres:postgres@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# State token to prevent request forgery.
# Stores it in session for later validation.

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
                                  digits) for x in xrange(32))
    login_session['state'] = state
    # Renders login template
    return render_template('login.html')


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in our
    # token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Server side function to accept client token


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Diconnect--revoke user token and reset login session


@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps(
            'Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset user session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps(
            'Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason the fiven token was invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Making an API GET Endpoint (GET request)
@app.route('/genre/<int:genre_id>/JSON/')
def bookItemJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    items = session.query(BookItem).filter_by(genre_id=genre.id).all()
    return jsonify(BookItems=[i.serialize for i in items])


# Making an API GET Endpoint for one menu item (GET request)
@app.route('/genre/<int:genre_id>/book/<int:book_id>/JSON/')
def singleMenuJSON(genre_id, book_id):
    bookitem = session.query(BookItem).filter_by(id=book_id).one()
    return jsonify(BookItem=bookitem.serialize)


# Shows a list of all genres available
@app.route('/')
@app.route('/allgenres/')
def allGenreItems():
    genre = session.query(Genre).order_by(Genre.name)
    if 'username' not in login_session:
        return render_template('publicgenre.html', genre=genre)
    else:
        return render_template('allgenreitems.html', genre=genre)
         

# Shows all books in a particular genre category
@app.route('/genre/<int:genre_id>/')
def genrelist(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    items = session.query(BookItem).filter_by(genre_id=genre.id)
    return render_template('book.html', genre=genre, items=items)


# Lets you create a new genre category
@app.route('/genre/new/', methods=['GET', 'POST'])
def newGenre():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Genre(name=request.form['name'])
        session.add(newItem)
        session.commit()
        flash("New genre created!")
        return redirect(url_for('allGenreItems'))
    else:
        return render_template('newgenre.html')

# Allows you to edit the genre
@app.route('/genre/<int:genre_id>/edit',
           methods=['GET', 'POST'])
def editGenreItem(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']

        session.add(editedItem)
        session.commit()
        flash("Genre has been edited!")
        return redirect(url_for('allGenreItems', genre_id=genre_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITGENREITEM TEMPLATE
        return render_template(
            'editgenres.html', genre_id=genre_id, item=editedItem)

# Allows you to delete a genre
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Genre has been deleted!")
        return redirect(url_for('allGenreItems', genre_id=genre_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR DELETEGENRE TEMPLATE
        return render_template(
            'deletegenre.html', genre_id=genre_id, item=deletedItem)


# Lets you create a new book in a particular genre category
@app.route('/book/<int:genre_id>/new/', methods=['GET', 'POST'])
def newBookItem(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = BookItem(name=request.form['name'], description=request.form['description'],
                           author=request.form['author'], price=request.form[
                               'price'],  genre_id=genre_id,
                           user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New book created!")
        return redirect(url_for('genrelist', genre_id=genre_id))
    else:
        return render_template('newbookitem.html', genre_id=genre_id)

# Shows the details of individual book
@app.route('/book/<int:genre_id>/<int:book_id>/')
def singleBookItem(genre_id, book_id):
    singleBook = session.query(BookItem).filter_by(id=book_id).one()
    if 'username' not in login_session or singleBook.user_id != login_session['user_id']:
        return render_template('publicbookdetails.html', item=singleBook)
    else:
        return render_template('bookdetails.html', genre_id=genre_id, id=book_id, item=singleBook)

# Edit all information for a book
@app.route('/book/<int:genre_id>/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBookItem(genre_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(BookItem).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['author']:
            editedItem.author = request.form['author']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash("Book has been edited!")
        return redirect(url_for('singleBookItem', genre_id=genre_id, book_id=book_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITBOOKITEM TEMPLATE
        return render_template(
            'editbookitem.html', genre_id=genre_id, id=book_id, item=editedItem)

# Allows you to delete a book
@app.route('/book/<int:genre_id>/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBookItem(genre_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(BookItem).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Book has been deleted!")
        return redirect(url_for('genrelist', genre_id=genre_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITBOOKITEM TEMPLATE
        return render_template(
            'deletebook.html', genre_id=genre_id, id=book_id, item=deletedItem)

#Creates a user in the database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one()
    return user.id

#Gets user info for to authorize changes to genres and books
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user_id

#Finds user id
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('allGenreItems'))
    else:
        flash("You were not logged in")
        return redirect(url_for('allGenreItems'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
