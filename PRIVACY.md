# PriestBot Privacy Policy

**Last updated:** September 7, 2026

PriestBot ("the bot") is a moderation and utility Discord application operated by the
staff of the Warcraft Priests Discord server. This policy explains what data the bot
collects, why it collects it, how long it is kept, and who can see it.

The bot's source code is public and available at
<https://github.com/lgkern/PriestPy> under the MIT license.

By participating in a Discord server where PriestBot is present, you are subject to
this policy.

---

## 1. Who operates the bot

PriestBot is operated by the administrators of the Warcraft Priests Discord server.
It is a private, non-commercial bot. It is not offered for public invite, it is not
monetized, and it is not operated by or affiliated with Discord Inc. or
Blizzard Entertainment.

Contact for privacy questions: **a direct message to any member of the Warcraft
Priests server holding the Admin role.**

---

## 2. What the bot collects

### 2.1 Message content in moderated channels

In a specific set of channels configured by server staff, the bot records:

- the message content
- the author's username and Discord user ID
- the message ID and channel name
- the timestamp

### 2.2 Message edits and deletions

When a message in a monitored channel is edited or deleted, the bot records:

- the content before the edit and the content after the edit
- for deletions, the content of the deleted message
- the author's username and Discord user ID
- the channel name and a timestamp
- where available from Discord's guild audit log, the moderator who performed the
  deletion

This is the bot's core moderation function. Discord does not retain the content of
deleted messages, so without this record a member can post rule-breaking content and
remove it before staff can act on it.

### 2.3 Direct messages sent to the bot

Messages that you send directly to PriestBot in a DM are recorded in the same way as
messages in monitored channels. The bot cannot see direct messages between you and
any other user.

### 2.4 Command usage

When you invoke a bot command (a message beginning with the command prefix), the bot
posts the guild name, channel name, your username and the full text of the command to
a private staff channel. This applies to commands used in a server and in DMs to the
bot.

### 2.5 Member events

The bot records the following to a private staff audit channel:

- joins and leaves, with username, Discord user ID and timestamp
- bans and unbans, with the responsible moderator and the stated reason where
  available from Discord's guild audit log

### 2.6 Presence and activity data

The bot reads the Discord presence (online status and current activity) of members who
hold the opt-in "Streaming Partner" role, in order to announce when they go live on
Twitch playing World of Warcraft and to grant a temporary "Currently Streaming" role.

Presence data is evaluated in memory and is **not** stored or written to any log. The
presence of members who do not hold the Streaming Partner role is ignored entirely.

> **Status note:** this feature is currently inactive pending replacement of a
> discontinued third-party library. The bot does not request the Discord Presence
> intent and the code path is disabled, so no presence data is being processed at
> this time.

---

## 3. What the bot does not collect

The bot does not collect or have access to:

- your email address, phone number, IP address or payment information
- your voice, video or screen share content
- direct messages between you and any other user
- message content in channels that server staff have not configured for logging
- any data from servers the bot has not been invited to

The bot does not build advertising profiles, does not perform automated content
scanning against any external service, and does not process biometric or special
category data.

---

## 4. Why the bot collects this data

| Data | Purpose |
|------|---------|
| Message content, edits and deletions | Moderation evidence, rule enforcement, and review of ban appeals |
| Command usage | Detecting abuse and troubleshooting bot behaviour |
| Member events | Maintaining a moderation history and identifying ban evasion or raid patterns |
| Presence of Streaming Partner role holders | Announcing community members who are live on Twitch |

No data is collected for any purpose other than operating and moderating the server.

---

## 5. Where data is stored and who can access it

- **Log files** are written to disk on a private server controlled by the bot
  maintainer. They are not exposed to the public internet.
- **Staff log channels** inside Discord are restricted to members holding an
  administrator or moderator role.

Access is limited to the server's administrators. No other member, and no person
outside the server's staff, has access.

---

## 6. Retention

| Data | Retention period |
|------|------------------|
| Message content, edits and deletions | 365 days (one year) |
| Command usage records | 365 days (one year) |
| Member join, leave, ban and unban records | 365 days (one year) |
| Presence data | Not retained |

Log files older than the retention period are deleted automatically by log rotation.

---

## 7. Sharing

Data collected by PriestBot has never been and will never be:

- sold, rented or licensed to any party
- shared with advertisers, data brokers or analytics providers
- used to train machine learning or artificial intelligence models
- disclosed to anyone outside the server's administrator team

The only exception is disclosure required by law, or a report submitted to Discord
Trust and Safety in relation to a violation of Discord's Terms of Service or Community
Guidelines.

---

## 8. Your rights

You may contact the server administrators, **by direct message to any member holding
the Admin role**, to:

- ask what data the bot holds about you
- request a copy of that data
- request deletion of your data

Requests are normally answered within 30 days. Note that data forming part of an
active moderation record, an ongoing investigation, or an existing ban may be retained
where deletion would defeat the purpose of the moderation system. If a deletion request
is refused on that basis, you will be told why.

Leaving the server does not automatically delete records already collected. Submit a
deletion request if you want them removed.

---

## 9. Children

Discord's Terms of Service require users to be at least 13 years old, or older where
local law sets a higher minimum age. PriestBot is not directed at children and does not
knowingly collect data from anyone below Discord's minimum age. If you believe a
record concerns such a user, contact the administrators and the record will be removed.

---

## 10. Changes to this policy

This policy may be updated as the bot changes. The "last updated" date at the top will
reflect any change, and material changes will be announced in the server's
announcements channel. The revision history for this document is public in the
repository linked above.

---

## 11. Discord's own policies

PriestBot operates within Discord and is subject to Discord's
[Terms of Service](https://discord.com/terms), [Privacy Policy](https://discord.com/privacy),
[Developer Terms of Service](https://discord.com/developers/docs/policies-and-agreements/developer-terms-of-service)
and [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy).
Data you provide to Discord itself is governed by Discord's privacy policy, not this one.
