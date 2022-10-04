# Book management system

## overview
The users in this website can be **writers**, and **readers** at the same time where the users can write their own books/stories [acting as writers], and the users can read other books/stories (that were written by other users) [acting as readers]
## getting start
1. run **python manage.py makemigrations**, and run **python manage.py migrate**
2. run **python manage.py runserver**

## Distinctiveness and Complexity
### According to the specification, my project must adhere to the following guidelines:
**Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.**

- I believe that my website is different (distinct) from the previous projects for the following reasons:
   1. it's not close to any previous project I have done before in this course, but it's close to a library website or book management website which I did not make before.
   2. the website contains users who can be readers or writers.
   3. The user can write story/book with multiple chapters(parts), the user can add new chapter/part to a book/story that he or she has created/written it, and the user can edit any chapter/part in a book/story that he or she has created/written it.
   4. The user can read or view other stories that were written by other users on the website.
   5. The user can create reading lists and add books or stories to these reading lists.
   , the user can add a story to his/her reading lists, or to his/her current reads if he/she is still not sure if he likes this story, and want to read it to make sure.
   6. The user can add a story that was already exist in the current reads to the archive.
   7. The user can view all the stories in his/her playlists, his/her current reads, or his/her archive, and also view or read any chapter from these stories.
   8. The user can chat with any other user on the website (there is a chat).
   9. The user can search for a chat, a story, or a user.
   10. The user can view his/her own profile, can view other users' profile, and can follow or unfollow other users.
   11. I built a simple notifications system, which notifies users of new stories, and who followed them.
         - when the user follows other user, the system notifies the other user. 
         - when the user writes new story, the system notifies his/her followers. when the user adds new chapter to a story or edit a chapter in a story, the system notifies his/her followers, and the users who add this story to their reading playlists, their current reads, or their archive.
         - the user is notified when there is new messages or chats.

- I believe that my website is complex also for these reasons:
   1. This website took me much time to finish it.
   2. I have learnt new concepts, and new skills.
   3. this website contains 12 models, and I have used JavaScript. 

**A project that appears to be a social network is a priori deemed by the staff to be indistinct from Project 4, and should not be submitted; it will be rejected.**
- I believe that my website is different from project 4 for these reasons:
   1. this website reads or write stories which is completely different from project 4  but in project 4 users create posts.
   2. the user can add the stories in read lists, current reads, and archive.

**A project that appears to be an e-commerce site is strongly suspected to be indistinct from Project 2, and your README.md file should be very clear as to why it’s not. Failing that, it should not be submitted; it will be rejected.**
- I believe that my website is different from project 2 for these reasons:
   1. this website reads or write stories which is completely different from project 2 but in project 2 users create listsings.
   2. the user in project 2 interact with each others using bids, but here the users interact through chats.

**Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.**
   - My application was built using Django, including 12 models on the back-end and uses JavaScript to make dynamic updates on the front-end. All generated information is saved in a database.

**Your web application must be mobile-responsive**
   - Every page and feature of the web application is mobile-responsive using bootstrap, and CSS
## Models:
There are 12 models in database:
1.	User - An extension of Django's AbstractUser model. 
2.	Story – contains the stories’ writer, title, description, category, and cover .
3.	Chapter – contains the chapters in each story
4.	Readlist – contains read lists for each user (by default there is a read list that is created for the user by the system as the user signs up)
5.	Contain- Stores stories that are saved at each read list.
6.	CurrentRead – contains all current reads (by default there is a current reads library that is created for the user by the system as the user signs up)
7.	CurrentContain - Stores all the stories that are saved by the user in his/her current read.
8.	Archive – contains the archived stories for each user.
9.	Chat– contains different chats.
10.	Message– contains messages for each chat.
11.	Follow– stores the followers.
12.	Notification– stores all the notifications.
## Routes
### index default route
This page shows all the stories, and if the user is logged in it shows his/her stories as well.
### Login /login
The user can log into the website using a valid username and password.
### Logout /logout
The user can logout.
### Register /register
The user enters their username, email address, and password. The page has the following validation:
1.	There is no existing user with the username provided
If the details are valid, a new user is created in the User model. 

### Write /write
The user can write new story where the user enters the title, description, cover image, and the category of this story
### write/<int:sid>/<int:cid>
The user can add a new chapter (of cid as id) to his/her story (of sid as id).
### story/<int:sid>
The user can view a story.
### editChapter/<int:cid>
-	The user can edit a chapter in his/her own story or view other users’ chapters in their stories but can’t edit them.
-	If the story is written by the current user then the user can edit the chapter whose id is cid using this route, otherwise the user can only view this chapter.
### addToReadlist/<int:sid>
The user can add a story (that has id = sid) to one or more his/her reading lists by checking the read lists that he/she wants to add this story to. 
### checklist/<int:sid>
Returns which reading lists are checked by the user.
### showReadingLists
Shows all the reading lists of the current user.
### addReadList/<str:name>
The user can create new read list with name as a title.
### showReadList/<int:rid>
The user can view the stories which are stored inside certain Read list (has rid as id).
### showCurrentReads
The user can view the stories which are stored inside his/her current read (each user has his/her own current read)
### showArchives
The user can view the stories which are stored inside his/her archive.
### archive/<int:cid>
The user can archive a story which is stored inside his/her current reads.
### unarchive/<int:cid>
The user can unarchive a story which is stored inside his/her archive.
### /chats
The user can view his/her chats
### chat/<int:uid>
The user can view certain chat
### send_message
The user can send certain message in a certain chat by using JavaScript fetch that send the chat id, and the message to send_message route.
By default, the sender is always the current user [if the user is logged in]
### Notifications
When the user logs in, he/she can see a notification icon in the navigation bar. This number displays the number of **new** notifications he/she has, and comes from the look field on the Notification model. When the user clicks on the notification icon, the look field is set to 1 using showNotifications route and In the notifications display, unread notifications are marked in gray. The user can carry out the following actions:
-	If the user clicks on a notification, we make a request to /markread using JavaScript fetch to mark the individual notification as read in the database (set read field in Notification model to 1) and then we take the user to the page associated with the notification.
### search
#### search for story
The user can search for story by typing the name of the story then this name is sent using JavaScript fetch to searchForStory route, this route returns a set of results that will be displayed to the user.
#### search for user
The user can search for certain user or chat using JavaScript fetch to search route.

### profile
The user can view other users’ profile using profile/<int:uid> route, and follows or unfollow these users using follow/<int:uid>, and unfollow/<int:uid> respectively.
## Files and directories
The summary:
- library - project directory
   * __init__.py - generated by Django.
   * __pycahce__ -  generated by Django.
   * asgi.py - generated by Django
   * settings.py - generated by Django, also contains logic for media.
   * urls.py - contains project URLs.
   * wsgi.py - generated by Django.
- minds - main application directory.
   * __pycahce__ -  generated by Django.
   *  static contains all static content.
      - images contains the default cover image for the story if the user did not specify one.
      - minds contains
         - styles.css file – contains all CSS styles in the project.
         - minds.js -contains all JavaScript in the project.
   * templates/minds contains all application templates.
      - chat.html - template for showing certain chat content.
      - chats.html – template for showing all the user’s chats.
      - editChapter.html – template shows form to edit certain chapter.
      - index.html – template for home page which show all the stories, and if the user is logged in, it shows the stories created by this user.
      - layout.html - parent template. All other templates extend it.
      - login.html - template for login page.
      - profile.html – template to show certain user’s profile.
      - register – template for register page.
      - searchForStory.html – template to shows the results of searching for certain story.
      - showArchives.html – template to shows the stories inside the archive for logged-in user.
      - showCurrentReads.html – template to shows the stories inside the current reads for logged-in user.
      - showNotifications.html – template to shows the notifications for logged-in user.
      - showReadinglists.html – template to shows all the read lists owned by the logged-in user.
      - showReadlist.html – template to shows the stories that are stored inside a certain read list owned by the logged-in user.
      - story.html – template to shows all the information about certain story including the chapters inside this story.
      - view chapter.html – template that shows certain chapter.
      - write.html – template that contains form to specify the new story’s information (used when the user want to write a new story)
      - writeChapter.html – template that contains form to specify the title, and content of a new chapter in certain story.
   * __init__.py - generated by Django.
   * admin.py - used to determine models which will be used in the Django Admin Interface.
   * apps.py - generated by Django.
   * models.py defines the models in the database.
   * tests.py – generated by Django.
   * urls.py - defines all application’s URLs.
   * views.py - contains all application’s views.
   - manage.py - generated by Django. 
## How to run the application
1. run **python manage.py makemigrations**, and run **python manage.py migrate**
2. run **python manage.py runserver**

