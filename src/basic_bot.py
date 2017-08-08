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
import logging
import time
from discord import HTTPException
from discord import utils

logging.basicConfig(level=logging.INFO)

client = discord.Client()

prefix = Key().prefix()

logger = PriestLogger()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    r = DictionaryReader()
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
        
    if message.content.startswith(prefix):
        await messageHandler(message)
        
    if message.channel.name != None and message.channel.name in r.logChannels():
        logger.log(message)    
                 
@client.event
async def on_member_join(member):
    await sendWelcomeMessage(member)
    await logAction(member, 'joined')

@client.event   
async def on_member_remove(member):
    print('member left')
    await logAction(member, 'left')
    
@client.event
async def on_member_ban(guild, user):
    await logAction(user, guild, 'banned')
    
@client.event
async def on_member_unban(member):
    await logAction(member, 'unbanned')
    
@client.event
async def on_member_update(before, after):
    return
    # Checks if the Game state changed
    if before.game != after.game:
        p = DictionaryReader()
        if after.game is None: 
            # Removes role if assigned
            role = utils.find(lambda r: r.name == p.streamingRole(), after.roles)
            if role is not None:
                await after.remove_roles(after, role)
                
        else:
            role = utils.find(lambda r: r.name == p.streamingRole(), after.guild.roles)
            if role not in after.roles and after.game.type == 1:
            # Adds the role if started streaming
                await after.add_roles(after, role)

async def logAction(member, action):
    await logAction(member, member.guild, action)

    
async def logAction(user, guild, action):
    r = DictionaryReader()
    if guild:
        await client.get_channel(int(r.actionLogChannel())).send('['+time.strftime("%Y-%m-%d %H:%M:%S")+'] {1.name} - {0.name} ({0.id}) {2}'.format(user, guild, action))
    else:
        await client.get_channel(int(r.actionLogChannel())).send('No Server - {0.name} ({0.id}) {1}'.format(user, action))
    #print('error while writing {0} log'.format(action))
    
            
async def messageHandler(message):
    if message.guild:
        await client.get_channel(220534135947526154).send('{0.guild.name} - {0.channel.name} - {0.author} invoked {0.content}'.format(message))
    else:
        await client.get_channel(220534135947526154).send('PM - PM - {0.author} invoked {0.content}'.format(message))
    
    if message.content.startswith(prefix+'fullupdate') or message.content.startswith(prefix+'update') or message.content.startswith(prefix+'channel'):
        await maintenanceMessages(message)

    elif message.content.startswith(prefix+'send'):
        await forwardMessage(message)
        
    elif message.content.startswith(prefix+'item'):
        await itemMessage(message)
    
    elif message.content.startswith(prefix+'pin') or message.content.startswith(prefix+'pins'):
        await sendPinMessages(message)
        
    elif message.content.startswith(prefix+'channel'):
        await message.channel.send(string(message.channel.id))
        
    elif message.content.startswith(prefix+'ban'):
        await adminControl(message)
        
    else:
        await generalMessage(message)

async def maintenanceMessages(message):
    if message.content.startswith(prefix+'update'):
        call(["git","pull"])
    p = DictionaryReader()
    if message.content.startswith(prefix+'fullupdate'): 
        if string(message.author.id) not in p.admins():
            await message.channel.send('You\'re not my dad, {0.mention}!'.format(message.author))
            return
        call(["git","pull"])
        call(["start_bot.sh"])
        sys.exit()

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

async def generalMessage(message):
    p = DictionaryReader()
    try:
        roles = len(message.author.roles)
    except Exception:
        roles = 10
    command = message.content[1::].split(' ')[0].lower()
    msg = p.commandReader(message.content[1::],message.channel.name)
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
        msg = p.commandReader('invalid',message.channel.name)
        await message.author.send(msg)        
        try:
            await message.delete()
        except (HTTPException, Forbidden):
            print('Error deleting message, probably from whisper')

async def adminControl(message):
    p = DictionaryReader()
    roles = message.author.roles
    canSend = False
    for role in roles:
        canSend = canSend or (role.name in p.roles())
    if not canSend:
        print('{0.author.name} can\'t ban members!'.format(message))
        return
    else:
        if message.content.startswith(prefix+'ban'):
            if not message.guild.me.guild_permissions.ban_members:
                await message.author.send('The bot does not have permissions to ban members.')
                return
            id = message.content.split(' ')[1]
            try:
                await client.http.ban(id, message.guild.id)
                user = await client.get_user_info(id)
                if user != None:
                    await message.author.send('User '+user.name+' banned successfully')                            
                else:
                    await message.author.send('Invalid user ID')                            
            except discord.HTTPException:
                pass
            finally:
                await message.delete()
    
client.run(Key().value())
