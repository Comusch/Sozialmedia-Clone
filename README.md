# Instagram-Clon
This project is to learn flask and how to programm a website with python
So i try to create my own network.

## Bot Support
You can create a new bot in your Profile. The bot can post and like posts.
The bot has an id, which you also see in your profile.
The bot can send the data to the server and the server will post it.\
Url for the bot: \
"/login_bot/<int:bot_id>" to login the bot \
"/logout_bot/<int:bot_id>" to logout the bot \
"/Create_Post_Bot/<int:bot_id>" to create a post\
"/like_post_bot/<int:bot_id>/<int:post_id>" to like a post
"/change_Description_Bot/<int:bot_id>" to change the description of the bot
