# CampusSwapZone
#### Video Demo:  https://www.youtube.com/watch?v=Ggob7ln8eBo
#### Description:
I have created a website using HTML, CSS, Javascript and Flask as my CS50 final project named CampusSwapZone.
CampusSwapZone is website that provides a plateform for students in a campus to buy and sell items. Students can list their goods that they want to sell and students those are in need of that product can contact them though this website. There are several instances where senior students have things that are for no use for them, but they don't want to throw that instead they can sell that to thier juniors who are in need and ready to buy from them, finding such juniors is a difficult task, but our website make this task very easy. In the same way, when a fresher student want to buy an item but doesn't want to invest full cost, so finding such seniors is very difficult who are offering to sell that item, but our website make this task very easy.Overall, it is solving a good problem.

First, student have to register in order to use this website. He/She can register by navigating through register option in navigation bar. Here, student can fill the form to register, student must provide college email id, password, confirmation password, hostel, course and semester and then click register.

Your email id will become your username and password is password. Using you credentials, login on the website and start using it. Your will see three options on nav bar that are Home, Sell and Chat.

In home, you will get to see all the listings listed by sellers, you can filter them by selecting desired item from * *Select item* * and choose any of the listing appears. You can chat with the seller of a perticular listing using chat button of the listing you are intrested in and delete the listing that you listed.

In * Sell option, student and list a perticular item by providing a suitable title, desired price and category of listing. Bellow, you can delete the listing that you listed.

In * Chat option, we can view all the chat that you are involed in, weathher you recieved a message or sent a message. It will list all the conversations.


I have used four database tables that are users, items, listing, request and messages:

The users table is used to store the information of the users like userid ,email id, password, hostel, course and semester. This table provides us the overall view a user and required information.
The listing table is used to store information regarding a listing(product listing) done by a user in order to sell it. It stores details like listingid, sellerid(userid of seller), title, price, categoryid(from items) and date and time of listing. It provides all the neccesary details about a listing when needed.
The items table is used to store the details related to the category of items such as item's id and item's name.
The request table is used to store the store records related to request done by a buyer reagarding a listing. It stores requestid, buyerid (userid from users) and listingid (listingid from listing).
The messages table is used to store the details related to a message such as messageid, senderid(userid from users), recieverid (userid from users), listingid(listingid from listing), content and date and time of the message.
All the tables are stored in finance.db database.

There are eight templates in templates folder that are apology.html, chat.html, chats.html, index.html, layout.html, login.html, register.html and sell.html.
The apology.html template is used to display an apology to the user under certain conditions like if user did't enter valid credentials.
The chat.html template is used to display the chat page of the website, where the list of all the conversations in which user is a part.
The chat.html template is used to display a message box to the user for a perticular recipient and a perticular listing.It displays all the previous conversation held between the two and provides an option to send messages to the recipient.
The index.html template is used to display the homepage of the website where all the listing from the students across the campus is shown and a section where user can select specific item category to filter among the listings.
The layout.html template contains the main layout of the website including navigation bar and background.
The login.html template is used to display the login page to the user. It provides a login form to user to enter the login credentials in order to login the website and use it.
The register.html template is used to display register page to the user. It provides a registration form to user to enter the details in order to register on the website.
The sell.html template is used to display the a page to user by which a user can add new listing to the website and delete existing listing posted by him/her.

The file app.py contains all the flask code for running the backend of the website.
The file helpers.py contains certain functions that are useful for app.py to run the website as it should.

The Static folder contains two files, one is the style.css that provides the styling of the website and second is the favicon1.ico which is the icon of the website, that will we displayed in the title bar and navigation bar.






