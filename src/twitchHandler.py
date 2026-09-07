class TwitchHandler:

    # The twitch package is discontinued and may stop installing. It is imported
    # inside each method so that importing this module never fails on its own.

    async def validateStream(url, twitch_id):
        from twitch import TwitchClient

        client = TwitchClient(client_id=twitch_id)
        channelName = url.split('/')[-1]
        channels = client.search.channels(channelName)
        
        if channels:
            for ch in channels:
                if ch.name.casefold() == channelName.casefold():
                    return 'World of Warcraft' in ch.game
        
        return False
        
    async def fetchStreamInfo(url, twitch_id):
        from twitch import TwitchClient

        client = TwitchClient(client_id=twitch_id)
        channelName = url.split('/')[-1]
        channels = client.search.channels(channelName)
        
        title = None
        description = None
        avatar = None
        views = None
        followers = None
                
        if channels:
            channel = channels[0]
            
            for ch in channels:
                if ch.name.casefold() == channelName.casefold():
                    channel = ch
                    break

            avatar = channel.logo
            title = channel.status
            description = channel.description
            views = channel.views
            followers = channel.followers
        
        return title, description, avatar, views, followers
