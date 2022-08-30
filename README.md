# Django-Based-Blog
This is my first full stack web development project

* A Python Django framework based multi-user blog system
* Everyone can read and “like” the articles in the blog, but only user who registered can post articles and make comment on the articles, article posing supports Markdown grammar, comment use ckeditor.
* User can see article's number of views, likes, comments and when the article was post; articles can be sorted by number of view or article posting time. 
*	User can use third party login like GitHub, registered users can modify their username, avatar, or delete their account
* User can edit their profile, which includes information of avatar, phone number and bio. 
* User can delete their article and delete their accounts, if an account is deleted, all article written by that account will also be deleted. 
*	Used HTML, CSS, JavaScript and Bootstrap4 to design the front-end 
* Use Python and django for backend design.
*	Used SQLite as database engine, but otehr databse engine like MySQL is also supported, see ```setting.py``` for emxaple how to set it up 
*	Blog was deployed on AWS, it used Gunicorn and Nginx to handle client requests, and used Supervisor to manger Gunicorn process so the blog system will automatically restart immediately if the system accidentally shut down 
---
# Demo
This project is no longer deploy on the public Internet as I don't have a server right now, but I made a video for demo if you are interested how it looks after after deployment



https://user-images.githubusercontent.com/70169080/187521268-a165695d-5ff4-4023-b6f4-5a1ecc88df33.mp4

* 0:00-0:12  **Unregistered user read article**
* 0:12-0:28  **Register account**
* 0:28-1:17  **Read and 'like' an article, make comment and reply comment**
* 1:17-1:41  **Update user profile**
* 1:41-2:36  **Write and post article**
* 2:36-3:21  **Look at comment/article reply notice**
* 3:21-4:03  **Edit article**
* 4:03-4:35  **Look up article using categories and tags**
* 4:35-4:50  **Delete account**


https://user-images.githubusercontent.com/70169080/187523488-0acf3309-ec9c-41ae-b148-688a323a0df3.mp4

**Article searching and sorting function**

