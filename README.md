# P3: Udacity Full Stack Nanodegree. Item catalog.

###Description

This is a project submission for the Udacity full stack web developer nanodegree. 
Project 3: Item Catalog using python's flask framework and sqlalchemy (with sqlite as the database platform).



##Steps to run
-Install all necessary files and Vagrant according to this document:
[Udacity UD 330 class](https://www.udacity.com/wiki/ud330/setup)
-git clone https://github.com/udacity/OAuth2.0 oauth contains flask application, a vagrantfile, and a pg_config.sh file for installing all of the necessary tools.
-run vagrant up from the vagrant subdirectory in the rep. This assumes you have vagrant installed already.
-SSH into the virtual machine using Vagrant SSH
-From the vagrant/oauth subfolder, run "python database.py". 
-Then run "python lotsofbooks.py" This will populate the database with some books
-Finally run "python application.py" to start the application
-Open a browser to http://localhost:5000/login
-Login with your Google or Facebook account
-Once logged in, you'll be able to view the books and genres already on the site.
-You'll also be able to create new Genres and books and edit or delete your own genres and books
-You can logout from the top right at any time


### Dependancies
- [Python](https://www.python.org/downloads/) 
- [Vagrant](http://vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)
- [fullstack-nanodegree-vm repository](http://github.com/udacity/fullstack-nanodegree-vm)
- [flask framework](http://flask.pocoo.org/)


