from typing import Optional
import time
import random
from datetime import datetime
import humanize

from telegram import Message, User
from telegram import MessageEntity, ParseMode
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler, run_async

from BoaHancockBOT import dispatcher
from BoaHancockBOT.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from BoaHancockBOT.modules.redis.afk_redis import start_afk, end_afk, is_user_afk, afk_reason
from BoaHancockBOT import REDIS
from BoaHancockBOT.modules.users import get_user_id

from BoaHancockBOT.modules.helper_funcs.alternate import send_message
from BoaHancockBOT.modules.helper_funcs.readable_time import get_readable_time

AFK_GROUP = 7
AFK_REPLY_GROUP = 8

@run_async
def afk(update, context):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user
    if not user:  # ignore channels
        return

    if user.id == 777000:
        return
    start_afk_time = time.time()
    if len(args) >= 2:
        reason = args[1]
    else:
        reason = "none"
    start_afk(update.effective_user.id, reason)
    REDIS.set(f'afk_time_{update.effective_user.id}', start_afk_time)
    fname = update.effective_user.first_name
    try:
        update.effective_message.reply_text(
            "{} is now Away!".format(fname))
    except BadRequest:
        pass

@run_async
def no_longer_afk(update, context):
    user = update.effective_user
    message = update.effective_message
    if not user:  # ignore channels
        return

    if not is_user_afk(user.id):  #Check if user is afk or not
        return
    end_afk_time = get_readable_time((time.time() - float(REDIS.get(f'afk_time_{user.id}'))))
    REDIS.delete(f'afk_time_{user.id}')
    res = end_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "{} Is wasting his time in the chat!",
                "The Dead {} Came Back From His Grave!",
                "We thought we lost you {}",
                "Welcome Back {} now pay $69 to Get freedom or get banned!",
                "{} Good job waking up now get ready for your classes!",
                "Hey {}! Why weren't you online for such a long time?",
                "{} why did you came back?",
                "{} Is now back online!",
                "OwO, Welcome back {}",
                "Welcome to hell again {}",
                "Mission failed successfully {}",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(
                chosen_option.format(firstname),
            )
        except Exception:
            return
            



@run_async
def reply_afk(update, context):
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION])

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            elif ent.type == MessageEntity.MENTION:
                user_id = get_user_id(message.text[ent.offset:ent.offset +
                                                   ent.length])
                if not user_id:
                    # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                    return

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = context.bot.get_chat(user_id)
                except BadRequest:
                    print("Error: Could not fetch userid {} for AFK module".
                          format(user_id))
                    return
                fst_name = chat.first_name

            else:
                return

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if is_user_afk(user_id):
        reason = afk_reason(user_id)
        since_afk = get_readable_time((time.time() - float(REDIS.get(f'afk_time_{user_id}'))))
        if reason == "none":
            if int(userc_id) == int(user_id):
                return
            res = "{} is Dead!\nLast Liveliness: {} ago".format(fst_name, since_afk)
            update.effective_message.reply_text(res)
        else:
            if int(userc_id) == int(user_id):
                return
            res = "{} is afk!\nReason: {}\nLast seen: {} ago".format(fst_name, reason, since_afk)
            update.effective_message.reply_text(res)


def __user_info__(user_id):
    is_afk = is_user_afk(user_id)
    text = ""
    if is_afk:
        since_afk = get_readable_time((time.time() - float(REDIS.get(f'afk_time_{user_id}'))))
        text = "<i>This user is currently afk.</i>"
        text += f"\n<i>Last Seen: {since_afk}</i>"
       
    else:
        text = "<i>This user currently isn't afk.</i>"
    return text


def __gdpr__(user_id):
    end_afk(user_id)

__help__ = """
 • `/afk <reason>`*:* mark yourself as AFK(away from keyboard).
 • `brb <reason>`*:* same as the afk command - but not a command.
When marked as AFK, any mentions will be replied to with a message to say you're not available!
"""
__mod_name__ = "AFK"

AFK_HANDLER = DisableAbleCommandHandler("afk", afk)
AFK_REGEX_HANDLER = MessageHandler(Filters.regex("(?i)brb"), afk)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.group, reply_afk)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)
