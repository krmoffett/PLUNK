# PLUNK
### Dependencies
discord.py - https://github.com/Rapptz/discord.py

pubg-python - https://github.com/ramonsaraiva/pubg-python

### Setup
1. Set up bot user in discordapp.developers and obtain token
2. Remove .template from config.ini.template
3. Copy bot token into the token field and PUBG Developer API key into the api-key field
4. The prefix used by the bot may be changed here also
5. Run plunk.py

### Adding users
PLUNK uses a stored dictionary of Discord names with PUBG player names. In order to add yourself, use the `addme` command followed by your PUBG user name. 

Example: `!addme shroud`

To add another user use the 'add' command with the users discord name followed by their PUBG name.

Example: `!add shroudDiscord shroud`

Additional commands can be found in the commands directory
