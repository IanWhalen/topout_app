Browser:
Spin up ec2 microinstance with AMI ami-cef405a7

Add value for key 'NAME'

Create a new key pair named 'TopOutAppServer', copy TopOutAppServer.pem to USB drive for safety
Copy key to ~/.ssh/TopOutAppServer.pem for use
chmod 600 ~/.ssh/TopOutAppServer.pem

Choose security group quick-start-1

Command Line:
ssh -i ./.ssh/TopOutAppServer.pem ubuntu@ec2-50-16-145-115.compute-1.amazonaws.com

sudo apt-get update
sudo apt-get install python-django
sudo apt-get install mysql-server
	enter password for root user
sudo apt-get install python-mysqldb
sudo apt-get install git

git clone git://github.com/IanWhalen/bkb_app.git

in settings.py, check MEDIA_ROOT

chmod 600 manage.py *It always comes down to permissions and sudo.*

sudo apt-get install python-pip

sudo pip install django-registration
sudo pip install south
sudo pip install django-socialregistration

mysql -uroot -p
CREATE USER 'topout'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'topout'@'localhost' WITH GRANT OPTION;
create database topout;

git clone git://github.com/facebook/python-sdk.git
cd python-sdk
sudo python setup.py install

sudo apt-get install python-openid

sudo pip install -e git+git://github.com/shelfworthy/minidetector.git#egg=minidetector

