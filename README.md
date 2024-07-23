# DiscordDispenser
> Self-hostable Discord bot to help with Hacking

D2 is a Discord bot that lets you do enumeration on target web domains from the comfort of your Discord server. Build up the Docker container, give it a bot token & a webhook, and enjoy! 

## Description:
`DiscordDispenser` -- D2 for short -- is meant to be used as a tool to help with Bug Bounty Hunting & Penetration testing. Users can issue commands via Discord, and the bot returns the output logs directly within the chat of your choosing. This setup provides a remote way to control and monitor a security testing process.

> ⚠️ Remember that the tools are being run on your server! You, and you only are responsible for any misuse of this software.

## Usage:

You need to create a bot token, and a webhook. You can find tutorials for both online, such as the following:
- [Bot token](https://discordgsm.com/guide/how-to-get-a-discord-bot-token)
- [Webhook](https://docs.gitlab.com/ee/user/project/integrations/discord_notifications.html)

To get the docker container running, you should be able to just docker compose it:
```
docker compose up --build
```

Alternatively, you can also run this:
```
docker build -t d2 .
docker run d2
```

> ❗ Remember to add a Discord Bot token, and a Webhook url to the `.env` before running!

Without the TOKEN and the WEBHOOK, d2 **will not work**.

Once the Bot is online, you can invite to the server. Add a new domain to be scanned with the following command:
```
!add example.domain
```

The bot will send a message with reactions. Select the tools you want to use by reacting, and select the checkmark once you're ready to go.

Enjoy!

## Modifications

If you wish to modify the tools or commands that are being ran, you can find the commands from `./worker/modules/tools/ ` and their respective files. You can modify the commands to adjust the ratelimiting, for example.

Adding more tools is a bit difficult at the moment, but in theory the software could be modified in future to run from a .toml or .yaml file for easier addition of tools. As it stands, this software is written more as a PoC. 

## Notes
Important: This project is intended for educational and lawful purposes only. The author and contributors are not responsible for any misuse or illegal activities that may arise from using this software. By using this software, you agree to comply with all applicable laws and regulations. If you are uncertain about the legality of your actions, please seek legal advice before proceeding. The author and contributors disclaim any and all liability for any direct, indirect, or consequential loss or damage arising from your use of the software. Use this software at your own risk.

Thank you for your understanding and cooperation.