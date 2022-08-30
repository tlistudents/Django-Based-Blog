# Django-Based-Blog
This is my first full stack web developer project

* A Python Django framework based multi-user blog system
* Everyone can read and “like” the articles in the blog, but only user who registered can post articles and make comment on the articles, editor supports Markdown grammar. 
*	User can use third party login like GitHub, registered users can modify their username, avatar, or delete their account
*	Used HTML, CSS, JavaScript and Bootstrap4 to design the front-end 
*	Used SQLite as database engine, but MySQL is also supported 
*	Blog was deployed on AWS, it used Gunicorn and Nginx to handle client requests, and used Supervisor to manger Gunicorn process so the blog system will automatically restart immediately if the system accidentally shut down 
