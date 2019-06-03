## Personal-Blog
# By Charles Maina
## Description
This is a python based application that allows a user to view and comment on my blog posts. A writer can register and write new posts, comment on the post and delete the post they have created

## User Story
# User
As a user I would like to view the blog posts submitted
As a user I would like to comment on blog posts
As a user I would like to view the most recent posts
As a user I would like to alerted when a new post is made by joining a subscription.
# Writer
As a writer I would like to sign in to the blog.
As a writer I would also like to create blog from the application.
As a writer I would like to delete comments that I find insulting or degrading.
As a writer I would like to update or delete blogs i have created.
# Behaviour of the Application
On visiting the site you are redrected to a homepage where you can view the blog posts or sign in
If you do not have an account you can register to get an account
You can access the homepage again to view the blog posts and comments and be able to create new posts and comments
Setup
# Requirements
This project was created on a debian linux platform but should work on other unix based[not limited to] sytems.

# Python3.6

Creating a virtual environment
'''pip3 install virtualenv''' '''python3.6 -m venv virtual''' '''source virtual/bin/activate'''

Installing dependencies
'''pip3 install -r requirements.txt'''

Running Tests
'''python3.6 manage.py test'''

Running the Server
Development Mode
'''The following configuration should be enabled when in development mode'''

Production Mode
'''The following configuration should be enabled when in production mode'''

Run Server Starting server by defaut will run it in development mode '''| python3.6 manage.py server |''' or '''| python3 manage.py server |''' or '''| python2 manage.py server|'''

Deployment to Heroku
'''Set the configuration in production mode'''

''' heroku create ''' ''' heroku heroku addons:create heroku-postgresql ''' ''' git add . ''' ''' git push heroku master ''' ''' heroku run python3.6 manage.py db upgrade '''


# Technology Used
Python3.6
Flask
Bootstrap
HTML
Known Bugs
## License
MIT License Copyright (c) 2019 Charles Maina
