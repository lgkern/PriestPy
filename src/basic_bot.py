# -*- coding: utf-8 -*-

import discord
from discord import Forbidden
#from discord.ext import commands
import random
from dict import DictionaryReader
from botkey import Key
from subprocess import call
import sys
from priestLogger import PriestLogger
from perspectiveHandler import PerspectiveHandler
import logging
import time
import datetime
from discord import HTTPException
from discord import utils
from discord import DMChannel
from discord import Embed
from discord import Colour
from roleHandler import RoleHandler

logging.basicConfig(level=logging.INFO)

client = discord.Client()

prefix = Key().prefix()

logger = PriestLogger()

toxicity = PerspectiveHandler()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')    

@client.event
async def on_message(message):
    r = DictionaryReader()

    if message.channel.id == int(r.perspectiveLogChannelH2P()) and not message.author.bot:
        await toxicity.addReactions(r, message)

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
        
    if message.content.startswith(prefix):
        await messageHandler(message)
        
    if isinstance(message.channel, DMChannel) or message.channel.name in r.logChannels():
        logger.log(message)
        #await toxicity.measure(client, message)    
        
@client.event
async def on_message_edit(before, after):
    # bots edit messages to add embeds, we dont want to react to that
    if before.author.bot:
        return

    logger.logEdit(before, after)
    await logEdit(before, after)    

@client.event
async def on_message_delete(message):
    await logDelete(message)
    
@client.event
async def on_member_join(member):
    await sendWelcomeMessage(member)
    await logAction(member, member.guild, 'joined')

@client.event
async def on_raw_reaction_add(payload):

    if payload.user_id == client.user.id:
        return

    r = DictionaryReader()

    print(r.readEntry('subscriptionchannel',''))
    print(payload.emoji.name)
    #Only for reactions inside the report channel
    if payload.channel_id == int(r.perspectiveLogChannel()):
        await toxicity.feedback(payload.emoji, payload.user_id, r)

    elif payload.channel_id == int(r.readEntry('subscriptionchannel','')):
        await RoleHandler.newsSubscriptionAdd(client, payload.emoji, payload.user_id, payload.guild_id)

@client.event
async def on_raw_reaction_remove(payload):
    r = DictionaryReader()

    if payload.channel_id == int(r.readEntry('subscriptionchannel','')):
        await RoleHandler.newsSubscriptionRemove(client, payload.emoji, payload.user_id, payload.guild_id)

@client.event   
async def on_member_remove(member):
    print('member left')
    await logAction(member, member.guild, 'left')
    await RoleHandler.toggleUserState(client, member, None)
   
@client.event
async def on_member_ban(guild, user):
    await logBan(guild, user)
    await logAction(user, guild, 'banned')
    
@client.event
async def on_member_unban(member):
    await logAction(member, member.guild, 'unbanned')
    
@client.event
async def on_member_update(before, after):
    await RoleHandler.toggleUserState(client, before, after)
    
async def logAction(user, guild, action):
    r = DictionaryReader()
    channel = client.get_channel(int(r.actionLogChannel()))
    if guild and channel:
        await channel.send('['+time.strftime("%Y-%m-%d %H:%M:%S")+'] {1.name} - {0.name} {0.mention} ({0.id}) {2}'.format(user, guild, action))
    
    #print('error while writing {0} log'.format(action))
    
            
async def messageHandler(message):
    p = DictionaryReader()

    if message.guild:
        await client.get_channel(p.logReportChannel()).send('{0.guild.name} - {0.channel.name} - {0.author} invoked {0.content}'.format(message))
    else:
        await client.get_channel(p.logReportChannel()).send('PM - PM - {0.author} invoked {0.content}'.format(message))
    
    if message.content.startswith(prefix+'fullupdate') or message.content.startswith(prefix+'update') or message.content.startswith(prefix+'channel'):
        await maintenanceMessages(message)

    elif message.content.startswith(prefix+'send'):
        await forwardMessage(message)
        
    elif message.content.startswith(prefix+'item'):
        await itemMessage(message)
    
    elif message.content.startswith(prefix+'pin') or message.content.startswith(prefix+'pins'):
        await sendPinMessages(message)

    elif message.content.startswith(prefix+'sub'):
        await RoleHandler.newsSubscription(client, message)
        await message.delete()
        
    elif message.content.startswith(prefix+'ban') or message.content.startswith(prefix+'info'):
        await adminControl(message)
        
    elif message.content.startswith(prefix+'stream'):
        print('StreamCommand')
        await RoleHandler.toggleStream(client, message)
        await message.delete()
        
    else:
        await generalMessage(message)

async def maintenanceMessages(message):
    if message.content.startswith(prefix+'update'):
        call(["git","pull"])
    p = DictionaryReader()
    if message.content.startswith(prefix+'fullupdate'): 
        if str(message.author.id) not in p.admins():
            await message.channel.send('You\'re not my dad, {0.mention}!'.format(message.author))
            return
        call(["git","pull"])
        call(["start_bot.sh"])
        sys.exit()
    elif message.content.startswith(prefix+'channel'):
        await message.author.send(str(message.channel.id))

async def forwardMessage(message):
    p = DictionaryReader()
    roles = message.author.roles
    canSend = False
    for role in roles:
        canSend = canSend or (role.name in p.roles())
    if not canSend:
        print('{0.author.name} can\'t send whispers'.format(message))
        return
    entries = message.content.split(' ')
    target = message.mentions[0]
    if target != None:
        entry = ' '.join(entries[2::])
        msg = p.commandReader(entry)
        if msg != None:
            await target.send(msg)
            await message.delete()
            await message.author.send('Message sent to {0.mention}'.format(target))
        else:
            await message.channel.send('Invalid Message, {0.mention}'.format(message.author))

async def itemMessage(message):
    p = DictionaryReader()
    msg = p.itemReader(message.content[1::])
    await message.channel.send(msg)
    
async def sendWelcomeMessage(member):
    p = DictionaryReader()
    msg = p.commandReader('help')
    await member.send(msg)
    
async def sendPinMessages(message):
    pins = await message.channel.pins()
    size = 10
    count = 0
    command = message.content.split(' ')
    try:
        await message.delete()
    except (HTTPException, Forbidden):
        print('Error deleting message, probably from whisper')
    if len(command) > 1:
        size = int(command[1]) if isinstance(command[1], int) else 10
        
    for msg in pins:
        if count >= size:
            return
        if msg.content:
            await message.author.send('``` Pin '+ str(count+1) + ' ```')
            await message.author.send(msg.content)
        count += 1

async def logEdit(before, after):
    r = DictionaryReader()

    emb = Embed()
    emb.title = 'Message Edited in {0.channel.name}'.format(before)
    emb.type = 'rich'
    emb.url = after.jump_url
    emb.colour = Colour.blue()
    emb.set_footer(text='UserID: {0.author.id}'.format(before), icon_url=before.author.avatar_url)
    emb.set_author(name=before.author.name,icon_url=before.author.avatar_url)
    emb.add_field(name='Before', value=before.content)
    emb.add_field(name='After', value=after.content, inline=False)

    logChannel = client.get_channel(int(r.moderationLogChannel()))
    await logChannel.send(embed=emb)

async def logDelete(message):
    r = DictionaryReader()    
    logChannel = client.get_channel(int(r.moderationLogChannel()))

    if not message.guild:
        return

    deletedBy = message.author

    # Checks if the bot can see the audit log
    if message.guild.me.guild_permissions.view_audit_log:        
        auditLogs = message.guild.audit_logs(limit=100, action=discord.AuditLogAction.message_delete)
        logs = await auditLogs.flatten()
        deletionLog = None
        for log in logs:
            if log.target.id == message.author.id:
                deletionLog = log
                break
        
        deletedBy = deletionLog.user if deletionLog else deletedBy


    emb = Embed()
    emb.title = 'Message Deleted in {0.channel.name}'.format(message)
    emb.type = 'rich'
    emb.url = message.jump_url
    emb.colour = Colour.red()
    emb.set_footer(text='Timestamp: '+ time.strftime("%Y-%m-%d %H:%M:%S"))
    emb.set_author(name=message.author.name,icon_url=message.author.avatar_url)
    emb.add_field(name='Author', value=message.author.name)
    emb.add_field(name='Deleted by', value=deletedBy.name)
    if not message.guild.me.guild_permissions.view_audit_log:
        emb.add_field(name='Warning', value='Bot cant see AuditLog')    
    emb.add_field(name='Message', value=message.content, inline=False)
    
    await logChannel.send(embed=emb)

async def logBan(guild, user):
    r = DictionaryReader()    
    logChannel = client.get_channel(int(r.moderationLogChannel()))

    if not guild:
        return

    bannedBy = guild.me
    banReason = ''

    # Checks if the bot can see the audit log
    if guild.me.guild_permissions.view_audit_log:        
        auditLogs = guild.audit_logs(limit=100, action=discord.AuditLogAction.ban)
        logs = await auditLogs.flatten()
        banLog = None
        for log in logs:
            if log.target.id == user.id:
                banLog = log
                break
        
        bannedBy = banLog.user if banLog else bannedBy
        banReason = banLog.reason


    emb = Embed()
    emb.title = 'User {0.name} Banned'.format(user)
    emb.type = 'rich'
    emb.colour = Colour.dark_red()
    emb.set_footer(text='Timestamp: '+ time.strftime("%Y-%m-%d %H:%M:%S"))
    emb.set_author(name=user.name,icon_url=user.avatar_url)
    emb.add_field(name='Banned by', value=bannedBy.name)
    if not guild.me.guild_permissions.view_audit_log:
        emb.add_field(name='Warning', value='Bot cant see AuditLog')    
    emb.add_field(name='Reason', value=banReason, inline=False)
    
    await logChannel.send(embed=emb)

async def generalMessage(message):
    p = DictionaryReader()
    try:
        roles = len(message.author.roles)
    except Exception:
        roles = 10
    command = message.content[1::].split(' ')[0].lower()
    msg = ''
    if not isinstance(message.channel, DMChannel):
        msg = p.commandReader(message.content[1::],message.channel.name)
    else:
        msg = p.commandReader(message.content[1::],'PM')
        
    if msg != None:
        if command in p.whisperCommands():
            if command == 'pub' and roles > 1 and 'help' not in message.content:
                await message.channel.send(msg)
            else:
                await message.author.send(msg)
                try:
                    await message.delete()
                except (HTTPException, Forbidden):
                    print('Error deleting message, probably from whisper')
        else:
            await message.channel.send(msg)
    else:
        if not isinstance(message.channel, DMChannel):
            msg = p.commandReader(message.content[1::],message.channel.name)
        else:
            msg = p.commandReader(message.content[1::],'PM')
        print(message.content[1::])
        print(msg)
        await message.author.send(msg)        
        try:
            await message.delete()
        except (HTTPException, Forbidden):
            print('Error deleting message, probably from whisper')

async def adminControl(message):
    p = DictionaryReader()
    roles = message.author.roles
    canBan = False
    for role in roles:
        canBan = canBan or (role.name in p.roles())
    if not canBan:
        print('{0.author.name} can\'t manage members!'.format(message))
        await message.author.send('You can\'t manage members!')  
        return
    else:
        # Mass bans - Format: !banall id0 id1 id2
        if message.content.startswith(prefix+'banall'):
            if not message.guild.me.guild_permissions.ban_members:
                await message.author.send('The bot does not have permissions to manage members.')
                return
            ids = message.content.split(' ')[1::]
            reason = 'mass ban'
            bannedCount = 0
            for id in ids:
                try:
                    user = await client.fetch_user(id)
                    await message.guild.ban(user=user, reason=reason, delete_message_days=7)
                    if user != None:
                        await message.author.send('User {0.mention} banned successfully'.format(user))
                        bannedCount +=1
                    else:
                        await message.author.send('{0} is an invalid user ID'.format(str(id)))                            
                except discord.HTTPException:
                    continue
            await message.author.send('Successfully banned {0} users'.format(str(bannedCount)))
            await message.delete()

        # Bans - Format:  !ban 9999999999999
        elif message.content.startswith(prefix+'ban'):
            if not message.guild.me.guild_permissions.ban_members:
                await message.author.send('The bot does not have permissions to manage members.')
                return
            splitMessage = message.content.split(' ')
            id = splitMessage[1]        
            deleteDays = 0 
            reasonStart = 2
            if len(splitMessage) > 2:
                deleteDays = splitMessage[2] if splitMessage[2].isdigit() else 0
                reasonStart = 3 if splitMessage[2].isdigit() else 2

            reason = ' '.join(splitMessage[reasonStart::])
            print(reason)
            try:
                user = await client.fetch_user(id)
                if user != None:
                    await message.guild.ban(user=user, reason=reason, delete_message_days=deleteDays)
                    await message.author.send('User {0.mention} banned successfully'.format(user))
                else:
                    await message.author.send('Invalid user ID')                            
            except discord.HTTPException:
                pass
            finally:
                await message.delete()
        # Ban info - Format:  !info 9999999999999
        elif message.content.startswith(prefix+'info'):        
            if not message.guild.me.guild_permissions.view_audit_log:
                await message.author.send('The bot does not have permissions to view audit logs.')
                return
            id = message.content.split(' ')[1]
            isUserBanned = False
            
            try:
                await message.delete()
            except (HTTPException, Forbidden):
                print('Error deleting message, probably from whisper')
            
            user = await client.fetch_user(id)
            
            await message.author.send( 'User {0.mention}\n```Bans```'.format(user) )
            
            async for entry in message.guild.audit_logs(action=discord.AuditLogAction.ban):                
                if str(entry.target.id) == str(id):               
                    await message.author.send('-> User {0.target}({0.target.id}) was **banned** by {0.user}({0.user.id}) on {0.created_at} (UTC)\n\tReason: {0.reason}\n'.format(entry))
                    isUserBanned = True
            
            await message.author.send( '```Unbans```' )
            async for entry in message.guild.audit_logs(action=discord.AuditLogAction.unban):
                if entry.target.id == int(id):
                    await message.author.send('-> User {0.target} was **unbanned** by {0.user}({0.user.id}) on {0.created_at} (UTC)'.format(entry))                    
            if not isUserBanned:
                await message.author.send('User was never banned.')
client.run(Key().value())
