# P5: Udacity Full Stack Nanodegree. Linux Server Setup.

###Description

This project consists installing a baseline Ubuntu Linux server and deploying a Flask application with PostgreSQL database while securing the server.

This application can be found at: [http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com/](http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com/) and [http://52.89.108.138/](http://52.89.108.138/)

+Also after suggestion from reviewer, setup DNS to this location:
+[http://anthrogeek.ddns.net/](http://anthrogeek.ddns.net/)
+
+$ ssh grader@52.89.108.138 -p2200

##Steps to run

##1 Download RSA key, ssh into instance

Source [Udacity](https://www.udacity.com/account#!/development_environment)

1. Launch your Virtual Machine with your Udacity account and log in. 
2. Download private keys to your computer
3. Move the key to your .ssh folder:
`-mv ~/Downloads/udacity_key.rsa ~/.ssh/`
4. Set permissions on key
`-chmod 600 ~/.ssh/udacity_key.rsa`
5. Log into virtual server using SSH
`-ssh -i ~/.ssh/udacity_key.rsa root@52.89.108.138`

##2 Create a new user grant this user sudo permissions.

1. Create new user grader
` adduser grader~
2. Give user permission to sudo: [askUbunto](http://askubuntu.com/questions/7477/how-can-i-add-a-new-user-as-sudoer-using-the-command-line) 
`sudo adduser grader sudo`

##3 Update all currently installed packages

1. Update all packages
- `apt-get update`
2. Install new versions of packages
- `sudo apt-get upgrade`
3. Automatically install updates
- `apt-get install unattended-upgrades`
4. Enable unattended updates package
- `sudo dpkg-reconfigure -plow unattended-upgrades`

##4 Configure the local timezone to UTC
`dpkg-reconfigure tzdata` 
Choose other>UTC


##5 & 6 Change the SSH port from 22 to 2200
Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

1. Change ssh config file and change port
`nano /etc/ssh/sshd_config`
Change to Port 2200
2. Restart SSH service
`/etc/init.d/ssh restart`
3. Check UFW status to make sure it's inactive
`ufw status`
4. Deny incoming traffic
`sudo ufw default deny incoming`
5. Allow outgoig traffic
`sudo ufw default allow outgoing`
6. Allow ssh
`sudo ufw allow ssh`
7. Allow port access 
`sudo ufw allow 2200/tcp`
8. Allow default web browser
`sudo ufw allow www`
9. Allow ntp
`sudo ufw allow ntp`
10. Enable UFW
`sudo ufw enable`

##7 Install and configure Apache to serve a Python mod_wsgi application
[DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

1. Install Apache
`sudo apt-get install apache2`
2. Visit http://52.89.108.138 to verify homepage shows Apache page.
3. Install mod-wsgi to help Apache and Python work together
`sudo apt-get install libapache2-mod-wsgi python-dev`
4. Enable mod-wsgi
`sudo a2enmod wsgi`
5. Create directory structure for app
`cd /var/www`
`sudo mkdir FlaskApp`
`cd FlaskApp`
`sudo mkdir FlaskApp`
`cd FlaskApp`
`sudo mkdir static templates`
6. Create simple app to make sure Flask is installed properly
`sudo nano __init__.py`
7. Add this code to __init__.py
```python
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, I love Linux Administration!"
if __name__ == "__main__":
    app.run()
```
8. Install python pip so we can install Flask and virtualenv
`sudo apt-get install python-pip`
`sudo pip install virtualenv`
`sudo virtualenv venv`
`source venv/bin/activate`
`sudo pip install Flask`
9. Create FlaskApp.conf to configure virtual host
`sudo nano /etc/apache2/sites-available/FlaskApp.conf`
10. Add code to FlaskApp.conf
```<VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
		<Directory /var/www/FlaskApp/FlaskApp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/FlaskApp/FlaskApp/static
		<Directory /var/www/FlaskApp/FlaskApp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>```
11. Enable virtual host
`sudo a2ensite FlaskApp`
12. Create a .wsgi file to serve the Flask app

```
cd /var/www/FlaskApp
sudo nano flaskapp.wsgi 
```

13. Add this code to the flaskapp.wsgi file [Flask Documentation](http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/#creating-a-wsgi-file)

```
#!/usr/bin/python
import sys, os
import logging

activate_this = '/var/www/FlaskApp/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")
os.chdir("/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'super_secret_key'
```

14. Restart Apache
`service apache2 restart`
15. 9. Visit http://52.89.108.138 to verify site is showing "Hello, I love Linux Administration!""

##8 Install and configure PostgreSQL
1. Install PostgreSQL [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
2. Ensure no remote connections are allowed
`nano /etc/postgresql/9.3/main/pq_hba.conf`

3. Create user catalog
```
sudo -u postgres psql postgres
createuser --interactive
sudo -u catalog psql catalog
\password catalog

```
##9 Install git, clone and set up your Catalog App project
1. Install needed packages for site
```
sudo pip install oauth2client
pip install Flask-SQLAlchemy
sudo apt-get install python-psycopg2
pip install psycopg2
apt-get install libpq-dev
apt-get install python-dev
apt-get install git
```
2. Clone catalog app project
`git clone https://github.com/anthrogeek/P5LinuxAdmin`
3. Remove access to git files
```
cd /var/www/FlaskApp
touch .htaccess |echo "$RedirectMatch 404 /\.git" >> .htaccess`
```
4. Rename application.py to __init__.py
`mv application.py __init__.py`
5. Update files to show postgresql engine instead of sqlite
```
nano __init__.py
nano database_setup.py
nano lotsofbooks.py
```
6. Run database_setup.py and lotsofbooks.py to generate data in the database
```
python database_setup.py
python lotsofbooks.py
```

7. Restart server
`service apache2 restart`

##9.1 Fix OAuths to work with application

1. Add ServerAlias to config file
`sudo nano /etc/apache2/sites-available/catalog.conf`
`ServerAlias http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com`
2. Restart server
`service apache2 restart`
3. Go to [https://console.developers.google.com/project](https://console.developers.google.com/project) and add 
http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com/oauth2callback to Authorized JavaScript origins and http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com/oauth2callback to Authorized Redirects.

*Facebook
4. Go to Facebook Developer site [https://developers.facebook.com/apps/](https://developers.facebook.com/apps/)
5. Add [http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com](http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com) to their site URL

Site should be availabe at:
[http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com](http://ec2-52-89-108-138.us-west-2.compute.amazonaws.com)

if issues are found use 
`sudo tail -50 /var/log/apache2/error.log`
to see the last 50 lines of the apache error log to troubleshoot.

##Add key to Grader and Disable Root login [Manually add key](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server)
1. on local machine `ssh-keygen`
2. Display the content of the key and copy the content `cat ~/.ssh/id_rsa.pub`
2. Switch to grader `su - grader`
3. If it's not there, make ~.ssh directory `mkdir -p ~/.ssh`
4. Add the content to the authorized_keys file
`echo public_key_string >> ~/.ssh/authorized_keys` 
where public_key_string is from step 2.
5. Edit ssh config file
`nano /etc/ssh/sshd_config`
6. Append `AllowUsers grader`
7. Change PermitRootLogin from `without-password` to `no`
8. sudo service ssh restart


##Ban abuse and Monitor [failban](https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04)
-`apt-get install fail2ban`
-`cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local`
-`nano /etc/fail2ban/jail.local`
  *set bantime = 900
  *destemail = grader@localhost
setup sendmail
`sudo apt-get install nginx sendmail iptables-persistent`
restart fail2ban
`sudo service fail2ban stop`
`sudo service fail2ban start`

*install [Glances](http://glances.readthedocs.org/en/latest/glances-doc.html#introduction)
*`sudo pip install Glances`

Installed [MondoMindi](https://help.ubuntu.com/community/MondoMindi) for server backups.



###Third party resources
[https://discussions.udacity.com/t/markedly-underwhelming-and-potentially-wrong-resource-list-for-p5/8587](https://discussions.udacity.com/t/markedly-underwhelming-and-potentially-wrong-resource-list-for-p5/8587)

[Deploy Flask App](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

[Project 5 Resources](https://discussions.udacity.com/t/project-5-resources/28343)

[Postgresql](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)

[List all users](http://askubuntu.com/questions/410244/a-command-to-list-all-users-and-how-to-add-delete-modify-users)

[Client-secret-json not found](https://discussions.udacity.com/t/client-secret-json-not-found-error/34070)

[Flask-working with virtual environments](http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/#working-with-virtual-environments)

