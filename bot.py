from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio, time

app = Client(
    "DONATE_ARMY_APPROVE",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [
    "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.mp4",
    "https://media.giphy.com/media/l1J9EdzfOSgfyueLm/giphy.mp4",
    "https://media.giphy.com/media/xUPGGDNsLvqsBOhuU0/giphy.mp4",
    "https://media.giphy.com/media/xT39CXg70nNS0MFNLy/giphy.mp4",
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.mp4",
    "https://media.giphy.com/media/1xkUkkkg3pQnfp1yvm/giphy.mp4",
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.mp4",
    "https://media.giphy.com/media/3ohhwF34cGDoFFhRfy/giphy.mp4",
    "https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.mp4",
    "https://tenor.com/view/welcome-gif-19366855",
    "https://tenor.com/view/hello-welcome-neon-lights-gif-20482452",
    "https://tenor.com/view/hi-hello-welcome-gif-16952349",
    "https://tenor.com/view/hi-there-welcome-animated-text-gif-23001649",
    "https://tenor.com/view/galaxy-glow-welcome-gif-19366859",
    "https://tenor.com/view/abstract-welcome-lights-gif-20598340",
    "https://tenor.com/view/hello-hi-welcome-colorful-gif-16980934",
    "https://tenor.com/view/neon-particles-gif-22875045",
    "https://tenor.com/view/fancy-welcome-gif-21379121",
    "https://tenor.com/view/welcome-neon-flash-gif-21157980",
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
            await client.get_chat_member(channel["id"], user_id)
        except UserNotParticipant:
            return False, channel
        except Exception as e:
            print(f"Error checking channel {channel['link']}: {e}")
            return False, channel
    return True, None

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    try:
        is_member, missing_channel = await check_all_channels(app, m.from_user.id)
        if not is_member:
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🍀 Join Here 🍀", url=missing_channel["link"])],
                    [InlineKeyboardButton("✅ Check Again ✅", "chk")]
                ]
            )
            await m.reply_text(
                f"**⚠️ Access Denied! ⚠️**\n\n"
                f"**You must join {missing_channel['link']} to use me. If you've joined, click 'Check Again'.**",
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
                f"**You must join {missing_channel['link']} to use me. If you've joined, click 'Check Again'.**"
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

@app.on_message(filters.command("help"))
async def help(_, m: Message):
    help_text = (
        "**🦊 Bot Help Guide 🦊**\n\n"
        "**1. Start the bot**: Click on the /start button to begin using the bot.\n\n"
        "**2. Check Channel Membership**: The bot checks if you are a member of the required channels. If not, you will receive an inline button to join the missing channel.\n\n"
        "**3. Add me to Your Group**: You can add this bot to your group and promote it as an admin to automatically approve join requests.\n\n"
        "**4. Broadcast**: Sudo users can broadcast messages to all users who have started the bot using the `/bcast` command.\n\n"
        "**5. Stats**: The `/stats` command gives you a summary of users and groups using the bot, along with uptime and ping.\n\n"
        "**6. Support**: For assistance, join our support channel at @DONATE_ARMY_BOTS_SUPPORT_CHAT.\n\n"
        "**7. Channel**: Stay updated by joining our channel @DONATE_ARMY_BOTS.\n\n"
        "__Powered by: @DONATE_ARMY_BOTS__"
    )
    await m.reply_text(help_text)

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
