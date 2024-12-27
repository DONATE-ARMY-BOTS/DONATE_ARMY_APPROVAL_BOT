from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio, time

app = Client(
    "DONATE_ARMY_APPROVE",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN

gif = [
    # Giphy Links
    "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.mp4",  # Abstract Lights
    "https://media.giphy.com/media/l1J9EdzfOSgfyueLm/giphy.mp4",  # Vibrant Welcome
    "https://media.giphy.com/media/xUPGGDNsLvqsBOhuU0/giphy.mp4",  # Glowing Digital Effect
    "https://media.giphy.com/media/xT39CXg70nNS0MFNLy/giphy.mp4",  # Neon Lights Animation
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.mp4",  # Abstract Futuristic Animation
    "https://media.giphy.com/media/1xkUkkkg3pQnfp1yvm/giphy.mp4",  # Modern Neon Text
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.mp4",  # Colorful Particles
    "https://media.giphy.com/media/3ohhwF34cGDoFFhRfy/giphy.mp4",  # Elegant Animation
    "https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.mp4",  # Shimmering Stars
    # Tenor Links
    "https://tenor.com/view/welcome-gif-19366855",  # Animated Welcome
    "https://tenor.com/view/hello-welcome-neon-lights-gif-20482452",  # Neon Welcome
    "https://tenor.com/view/hi-hello-welcome-gif-16952349",  # Casual Greeting
    "https://tenor.com/view/hi-there-welcome-animated-text-gif-23001649",  # Bold Welcome Animation
    "https://tenor.com/view/galaxy-glow-welcome-gif-19366859",  # Galaxy Glow
    "https://tenor.com/view/abstract-welcome-lights-gif-20598340",  # Abstract Welcome Animation
    "https://tenor.com/view/hello-hi-welcome-colorful-gif-16980934",  # Colorful Text Animation
    "https://tenor.com/view/neon-particles-gif-22875045",  # Futuristic Particles
    "https://tenor.com/view/fancy-welcome-gif-21379121",  # Fancy Greeting
    "https://tenor.com/view/welcome-neon-flash-gif-21157980",  # Flashy Neon Effect
]

START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {seconds}s"

async def check_all_channels(client, user_id):
    for channel in cfg.REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return False, channel
        except Exception as e:
            print(f"Error checking channel {channel}: {e}")
            return False, channel
    return True, None

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    try:
        is_member, missing_channel = await check_all_channels(app, m.from_user.id)
        if not is_member:
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🍀 Join Here 🍀", url=f"https://t.me/{missing_channel.lstrip('@')}")],
                    [InlineKeyboardButton("✅ Check Again ✅", "chk")]
                ]
            )
            await m.reply_text(
                f"**⚠️ Access Denied! ⚠️**\n\n"
                f"**You must join {missing_channel} to use me. If you've joined, click 'Check Again'.**",
                reply_markup=keyboard
            )
            return

        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/DONATE_ARMY_BOTS"),
                        InlineKeyboardButton("💬 Support", url="https://t.me/DONATE_ARMY_BOTS_SUPPORT_CHAT")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/DONATE_ARMY_APPR0VAL_BOT?startgroup")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo(
                "https://graph.org/file/1b49977f76dd6ea731cc5.jpg",
                caption=(
                    f"**🦊 Hello {m.from_user.mention}!**\n"
                    f"**🌟 I'm an Auto-Approval Bot for Admin Join Requests.**\n"
                    f"**✨ Add me to your chat and promote me to admin with 'Add Members' permission.**\n\n"
                    f"__Powered by: @DONATE_ARMY_BOTS__"
                ),
                reply_markup=keyboard
            )
        elif m.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP}:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me privately 💁‍♂️", url="https://t.me/DONATE_ARMY_APPR0VAL_BOT?startgroup")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text(
                f"**🦊 Hello {m.from_user.first_name}!**\n"
                f"**✨ Write to me privately for more details.**",
                reply_markup=keyboard
            )
        print(f"{m.from_user.first_name} started your bot!")
    except Exception as e:
        print(f"Error in start command: {e}")

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        is_member, missing_channel = await check_all_channels(app, cb.from_user.id)
        if not is_member:
            await cb.message.edit_text(
                f"**⚠️ Access Denied! ⚠️**\n\n"
                f"**You must join {missing_channel} to use me. If you've joined, click 'Check Again'.**"
            )
            return

        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/DONATE_ARMY_BOTS"),
                        InlineKeyboardButton("💬 Support", url="https://t.me/DONATE_ARMY_BOTS_SUPPORT_CHAT")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/DONATE_ARMY_APPR0VAL_BOT?startgroup")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit_text(
                f"**🦊 Hello {cb.from_user.mention}!**\n"
                f"**🌟 I'm an Auto-Approval Bot for Admin Join Requests.**\n"
                f"**✨ Add me to your chat and promote me to admin with 'Add Members' permission.**\n\n"
                f"__Powered by: @DONATE_ARMY_BOTS__",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        print(f"{cb.from_user.first_name} started your bot!")
    except Exception as e:
        print(f"Error in check callback: {e}")

@app.on_message(filters.command("stats") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    total = int(xx + x)
    uptime = get_readable_time(int(time.time() - START_TIME))
    start_time = time.perf_counter()
    await asyncio.sleep(0.1)
    end_time = time.perf_counter()
    ping = round((end_time - start_time) * 1000, 2)
    await m.reply_text(
        f"""
**🍀 Chat Statistics 🍀**

**🙋‍♂️ Users:** `{xx}`
**👥 Groups:** `{x}`
**🚧 Total Users & Groups:** `{total}`

**⏳ Uptime:** `{uptime}`
**📶 Ping:** `{ping}ms`
"""
    )

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    msg = await m.reply_text("`⚡️ Processing Broadcast...`")
    success, failed, deactivated, blocked = 0, 0, 0, 0

    for usr in allusers.find():
        try:
            userid = usr["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception:
            failed += 1

    await msg.edit(
        f"**✅ Successfully sent to:** `{success}`\n"
        f"**❌ Failed to send to:** `{failed}`\n"
        f"**👾 Blocked users:** `{blocked}`\n"
        f"**👻 Deactivated users:** `{deactivated}`"
    )

print("Bot is now running!")
app.run()
        await m.reply_text(
            f"**⚠️ Access Denied! ⚠️**\n\n"
            f"**Please join @{cfg.FSUB} to use me. If you've joined, click the 'Check Again' button.**",
            reply_markup=keyboard
        )

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/DONATE_ARMY_BOTS"),
                        InlineKeyboardButton("💬 Support", url="https://t.me/DONATE_ARMY_BOTS_SUPPORT_CHAT")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/DONATE_ARMY_APPR0VAL_BOT?startgroup")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit(
                f"**🦊 Hello {cb.from_user.mention}!**\n"
                f"**🌟 I'm an Auto-Approval Bot for Admin Join Requests.**\n"
                f"**✨ Add me to your chat and promote me to admin with 'Add Members' permission.**\n\n"
                f"__Powered by: @DONATE_ARMY_BOTS__",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        print(f"{cb.from_user.first_name} started your bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to the channel. Join and try again. 🙅‍♂️")

@app.on_message(filters.command("stats") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    total = int(xx + x)
    uptime = get_readable_time(int(time.time() - START_TIME))
    start_time = time.perf_counter()
    await asyncio.sleep(0.1)
    end_time = time.perf_counter()
    ping = round((end_time - start_time) * 1000, 2)
    await m.reply_text(
        f"""
**🍀 Chat Statistics 🍀**

**🙋‍♂️ Users:** `{xx}`
**👥 Groups:** `{x}`
**🚧 Total Users & Groups:** `{total}`

**⏳ Uptime:** `{uptime}`
**📶 Ping:** `{ping}ms`
"""
    )

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    msg = await m.reply_text("`⚡️ Processing Broadcast...`")
    success, failed, deactivated, blocked = 0, 0, 0, 0
    for usr in allusers.find():
        try:
            userid = usr["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception:
            failed += 1
    await msg.edit(
        f"**✅ Successfully sent to:** `{success}`\n"
        f"**❌ Failed to send to:** `{failed}`\n"
        f"**👾 Blocked users:** `{blocked}`\n"
        f"**👻 Deactivated users:** `{deactivated}`"
    )

print("I'm Alive Now!")
app.run()
