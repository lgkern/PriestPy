from dict import DictionaryReader
from discord import utils

class RoleHandler:
    
    async def toggleStream(client, message):
        p = DictionaryReader()
        
        target = message.mentions[0] if message.mentions else message.author
        
        role  = utils.find(lambda r: r.name == p.streamingRole(), target.roles)
        staff = utils.find(lambda r: r.name == p.roles(), message.author.roles)
        donor = utils.find(lambda r: r.name == p.donor(), message.author.roles)
        streamingRole = utils.find(lambda r: r.name == p.streamingRole(), message.author.guild.roles)
        
        
                
        # Target doesn't have the Streaming Role
        if role is None:
                    
            # If user has the Staff role
            if staff is not None:
                await target.add_roles(streamingRole, reason='Role added by {0.name}'.format(message.author))
                
            else:
            # Donors can add the role to themselves
                if donor is not None:
                    await message.author.add_roles(streamingRole, reason='Donor adding role to themselves')
        
        #User already has the Streaming Role, so remove it
        else:
            # If user has the Staff role or is the author
            if staff is not None or target == message.author:
                await target.remove_roles(role, reason='Role removed by {0.name}'.format(message.author))               