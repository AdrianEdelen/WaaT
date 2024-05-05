# WaaT

Local Dev Setup:
0.1. in the User setting for your discord account, under the Advanced tab, select developer mode, this is required, to get specific information about the guild/server
1. Create a personal Discord guild
2. Set Server to Community server to enable Forum channels
3. go to server settings and select Enable Community, follow the proceeding steps
4. Select "Create one for me" for the rules and updates channel
5. The personal discord guild for local development is now ready

6. Go to the Discord Developer Portal https://discord.com/developers/applications
7. select new application ![image](https://github.com/AdrianEdelen/WaaT/assets/6466981/f35daa76-c831-4299-b735-99a299a3a916)
8. name the application how you choose, but make it distinct enough to remember
9. once created, seect the bot tab, enable Presence Intent, Server Members Intent, and Message Content Intent, un-select Public bot
10. select the OAuth2 tab and select the scope as 'bot' ![image](https://github.com/AdrianEdelen/WaaT/assets/6466981/f9ce7747-099e-48e3-9aa8-e47db1f646c9)
11. select administrator as the bot permission ![image](https://github.com/AdrianEdelen/WaaT/assets/6466981/44ebbb33-0eda-4133-b10a-8f5bd861b939)
12. copy the link and paste it in your browser.
13. Follow the prompts to invite the bot to your guild created earlier.

14. The bot and guild are now ready.

15. If you haven't already, set up your IDE or coding environment, these steps assume you are using vs code / vs codium
16. clone the repo and open it in vs code.
17. create a .env file, with the following
`DISCORD_BOT_TOKEN=bottokenhere`
`GUILD_ID=guildidhere`
`TEST=True`
`WEBSERVER_PORT=8080`
18. return to the discord developer portal, select the bot tab for your application created earlier, select reset token and copy the provided token into the .env file
19. in the personal discord guild, right click the name of the guild and  select copy server ID, and paste it in the .env file ![image](https://github.com/AdrianEdelen/WaaT/assets/6466981/9ca101a3-7752-4616-ac3e-29a8d1f46d4b)

NOTE: There is a basic dev environment setup attached with the repo for vs code, this makes it easy to get up and going. more advanced development can be done with docker if desired. if making changes to the docker file, please test it locally with docker first.

20. start the program with the run module in vs code: ![image](https://github.com/AdrianEdelen/WaaT/assets/6466981/7a1151fe-f269-4934-b115-783bad572131)
21. in the future the bot should automatically create missing channels for you, but currently you may need to create the appropriate channel in the discord itself.

any env var changes must be reflected in the docker file at the minimum, but should also be reflected in the unraid template and the vs code launch configuration (if necessary)

 

