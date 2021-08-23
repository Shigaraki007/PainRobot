import html
import json
import os
from typing import Optional

from BoaHancockBOT import (STRAWHATS, PIRATE_KING_ID, YONKO, SUPPORT_CHAT, ADMIRALS,
                          WARLORDS, VICE_ADMIRALS, dispatcher)
from BoaHancockBOT.modules.helper_funcs.chat_status import (dev_plus, sudo_plus,
                                                           whitelist_plus)
from BoaHancockBOT.modules.helper_funcs.extraction import extract_user
from BoaHancockBOT.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(),
                                   'BoaHancockBOT/elevated_users.json')


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! "

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
#disasters =
# """ Text here """

# do not async, not a handler
#def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@run_async
@dev_plus
@gloggable
def addyonko(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in YONKO:
        message.reply_text("This member is already One of the Yonkō")
        return ""

    if user_id in ADMIRALS:
        rt += "Requested Strawhats to promote an Admiral to One of the Yonkō."
        data['admirals'].remove(user_id)
        ADMIRALS.remove(user_id)

    if user_id in WOLVES:
        rt += "Requested Strawhats to promote a Vice Admiral to One of the Yonkō."
        data['vice_admirals'].remove(user_id)
        VICE_ADMIRALS.remove(user_id)

    data['yonko'].append(user_id)
    YONKO.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfully set Power lvl of {} to One of the Yonkō!".format(
            user_member.first_name))

    log_message = (
        f"#YONKO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addadmiral(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in YONKO:
        rt += "Requested Strawhats to deomote this Yonko to an Admiral"
        data['yonko'].remove(user_id)
        YONKO.remove(user_id)

    if user_id in ADMIRALS:
        message.reply_text("This user is already an Admiral.")
        return ""

    if user_id in VICE_ADMIRALS:
        rt += "Requested Strawhats to promote this Vice Admiral to an Admiral."
        data['vice_admiral'].remove(user_id)
        VICE_ADMIRALS.remove(user_id)

    data['admirals'].append(user_id)
    ADMIRALS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as an Navy Admiral!")

    log_message = (
        f"#ADMIRAL\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addviceadmiral(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in YONKO:
        rt += "This member is One of the Yonkō, Demoting to an Vice Admiral."
        data['yonko'].remove(user_id)
        YONKO.remove(user_id)

    if user_id in ADMIRALS:
        rt += "This user is an Admiral, Demoting to an Vice Admiral."
        data['Admirals'].remove(user_id)
        ADMIRALS.remove(user_id)

    if user_id in VICE_ADMIRALS:
        message.reply_text("This user is already an Vice Admiral.")
        return ""

    data['vice_admirals'].append(user_id)
    VICE_ADMIRALS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to an Vice Admiral!")

    log_message = (
        f"#VICE_ADMIRALT\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwarlord(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in YONKO:
        rt += "This member is One of the Yonko, Demoting to a Warlord."
        data['yonko'].remove(user_id)
        YONKO.remove(user_id)

    if user_id in ADMIRALS:
        rt += "This user is an Admiral, Demoting to a Warlord."
        data['admirals'].remove(user_id)
        ADMIRALS.remove(user_id)

    if user_id in VICE_ADMIRALS:
        rt += "This user is an Vice Admiral, Promoting to a Warlord."
        data['vice_admirals'].remove(user_id)
        VICE_ADMIRALS.remove(user_id)

    if user_id in WARLORDS:
        message.reply_text("This user is already a Warlord.")
        return ""

    data['warlords'].append(user_id)
    WARLORDS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a Warlord!"
    )

    log_message = (
        f"#WARLORD\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@gloggable
def removeyonko(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in YONKO:
        message.reply_text("Requested Strawhats to demote this user to a no name Pirate ")
        YONKO.remove(user_id)
        data['yonko'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DEMOTED_YONKO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not One of the Yonkō anymore!")
        return ""


@run_async
@sudo_plus
@gloggable
def removeadmiral(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in ADMIRALS:
        message.reply_text("Requested Strawhats to demote this user to a no name Pirate")
        ADMIRALS.remove(user_id)
        data['admiral'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DEMOTED_ADMIRAL\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not an Admiral anymore!")
        return ""


@run_async
@sudo_plus
@gloggable
def removeviceadmiral(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in VICE_ADMIRALS:
        message.reply_text("Demoting to a no name Pirate")
        VICE_ADMIRALS.remove(user_id)
        data['vice_admiral'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DEMOTED_VICEADMIRAL\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not an Vice Admiral anymore!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewarlord(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WARLORDS:
        message.reply_text("Demoting to a no name Pirate")
        WARLORDS.remove(user_id)
        data['warlords'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#DEMOTED_WARLORD\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Warlord anymore!")
        return ""


@run_async
@whitelist_plus
def viceadmirals(update: Update, context: CallbackContext):
    reply = "<b>Known Vice Admirals:</b>\n"
    bot = context.bot
    for each_user in VICE_ADMIRALS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def warlords(update: Update, context: CallbackContext):
    reply = "<b>Known Warlords:</b>\n"
    bot = context.bot
    for each_user in WARLORDS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def admirals(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Navy Admirals:</b>\n"
    for each_user in ADMIRALS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def yonko(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(YONKO) - set(STRAWHATS))
    reply = "<b>Known Yonkō:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def strawhats(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(STRAWHATS) - {PIRATE_KING_ID})
    reply = "<b>Strawhat Pirates:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = f"""
*⚠️ Notice:*
Commands listed here only work for users with special access are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands. 

 ╔ *List all special users:*
 ╠ `/yonko`*:* Lists all Yonko (also know as SUDO)
 ╠ `/admirals`*:* Lists all Navy Admirals (also known as Support Users)
 ╠ `/warlords`*:* Lists all Warlords
 ╠ `/viceadmirals`*:* Lists all Vice Admirals (also known as Whitelisted Users)
 ╚ `/strawhats`*:* Lists all Strawhat Pirates (also known as Dev Users)

 ╔ *Ping:*
 ╠ `/ping`*:* gets ping time of bot to telegram server
 ╚ `/pingall`*:* gets all listed ping times

 ╔ *Broadcast: (Bot owner only)*
 ╠  *Note:* This supports basic markdown
 ╠ `/broadcastall`*:* Broadcasts everywhere
 ╠ `/broadcastusers`*:* Broadcasts too all users
 ╚ `/broadcastgroups`*:* Broadcasts too all groups

 ╔ *Groups Info:*
 ╠ `/groups`*:* List the groups with Name, ID, members count as a txt
 ╚ `/getchats`*:* Gets a list of group names the user has been seen in. Bot owner only

 ╔ *Blacklist:* 
 ╠ `/ignore`*:* Blacklists a user from 
 ╠  using the bot entirely
 ╚ `/notice`*:* Whitelists the user to allow bot usage

 ╔ *Speedtest:*
 ╚ `/speedtest`*:* Runs a speedtest and gives you 2 options to choose from, text or image output

 ╔ *Global Bans:*
 ╠ `/gban user reason`*:* Globally bans a user
 ╚ `/ungban user reason`*:* Unbans the user from the global bans list

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Lists names of all modules
 ╠ `/load modulename`*:* Loads the said module to 
 ╠   memory without restarting.
 ╠ `/unload modulename`*:* Loads the said module from
 ╚   memory without restarting.memory without restarting the bot 

 ╔ *Remote commands:*
 ╠ `/rban user group`*:* Remote ban
 ╠ `/runban user group`*:* Remote un-ban
 ╠ `/rpunch user group`*:* Remote punch
 ╠ `/rmute user group`*:* Remote mute
 ╠ `/runmute user group`*:* Remote un-mute
 ╚ `/ginfo username/link/ID`*:* Pulls info panel for entire group

 ╔ *Windows self hosted only:*
 ╠ `/reboot`*:* Restarts the bots service
 ╚ `/gitpull`*:* Pulls the repo and then restarts the bots service

 ╔ *Chatbot:* 
 ╚ `/listaichats`*:* Lists the chats the chatmode is enabled in
 
 ╔ *Debugging and Shell:* 
 ╠ `/debug <on/off>`*:* Logs commands to updates.txt
 ╠ `/logs`*:* Run this in support group to get logs in pm
 ╠ `/eval`*:* Self explanatory
 ╠ `/sh`*:* Self explanator
 ╚ `/py`*:* Self explanatory

Visit @{SUPPORT_CHAT} for more information.
"""

SUDO_HANDLER = CommandHandler(("addsudo", "addyonko"), addyonko)
SUPPORT_HANDLER = CommandHandler(("addsupport", "addadmiral"), addadmiral)
WARLORD_HANDLER = CommandHandler(("addwarlord"), addwarlord)
WHITELIST_HANDLER = CommandHandler(("addwhitelist", "addviceadmiral"), addviceadmiral)
UNSUDO_HANDLER = CommandHandler(("removesudo", "removeyonko"), removeyonko)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "removeadmiral"),
                                   removeadmiral)
UNWARLORD_HANDLER = CommandHandler(("removewarlord"), removewarlord)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "removeviceadmiral"),
                                     removeviceadmiral)

WHITELISTLIST_HANDLER = CommandHandler(["whitelistlist", "viceadmirals"],
                                       viceadmirals)
WARLORDLIST_HANDLER = CommandHandler(["warlords"], warlords)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "admirals"], admirals)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "yonko"], yonko)
DEVLIST_HANDLER = CommandHandler(["devlist", "strawhats"], strawhats)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(WARLORD_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNWARLORD_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(WARLORDLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Power lvl"
__handlers__ = [
    SUDO_HANDLER, SUPPORT_HANDLER, WARLORD_HANDLER, WHITELIST_HANDLER,
    UNSUDO_HANDLER, UNSUPPORT_HANDLER, UNWARLORD_HANDLER, UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER, WARLORDLIST_HANDLER, SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER, DEVLIST_HANDLER
]
