from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio, time

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [
    'https://te.legra.ph/file/a1b3d4a7b5fce249902f7.mp4',
    'https://te.legra.ph/file/0c855143a4039108df602.mp4',
    'https://te.legra.ph/file/d7f3f18a92e6f7add8fcd.mp4',
    'https://te.legra.ph/file/9e334112ee3a4000c4164.mp4',
    'https://te.legra.ph/file/652fc39ae6295272699c6.mp4',
    'https://te.legra.ph/file/702ca8761c3fd9c1b91e8.mp4'
]

START_TIME = time.time()

# Helper function for uptime
def get_readable_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {seconds}s"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main Process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        await app.send_video(
            kk.id,
            img,
            f"**✨ Hello {m.from_user.mention}!**\n"
            f"**🌟 Welcome to {m.chat.title}!**\n\n"
            f"__Powered by: @DONATE_ARMY_BOTS__"
        )
        add_user(kk.id)
    except errors.PeerIdInvalid:
        print("User hasn't started the bot (group join request failed).")
    except Exception as err:
        print(str(err))

@app.on_message(filters.command("start"))
async def op(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/DONATE_ARMY_BOTS"),
                        InlineKeyboardButton("💬 Support", url="https://t.me/DONATE_ARMY_BOTS_SUPPORT_CHAT")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/DONATE_ARMY_APPROVAL_BOT?startgroup")
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
                        InlineKeyboardButton("💁‍♂️ Start me privately 💁‍♂️", url="https://t.me/DONATE_ARMY_APPROVAL_BOT?startgroup")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text(f"**🦊 Hello {m.from_user.first_name}!**\n**✨ Write to me privately for more details.**", reply_markup=keyboard)
        print(f"{m.from_user.first_name} started your bot!")
    except UserNotParticipant:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🍀 Check Again 🍀", "chk")
                ]
            ]
        )
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
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/DONATE_ARMY_APPROVAL_BOT?startgroup")
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
    tot = int(xx + x)
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
**🚧 Total Users & Groups:** `{tot}`

**⏳ Uptime:** `{uptime}`
**📶 Ping:** `{ping}ms`
"""
    )

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success, failed, deactivated, blocked = 0, 0, 0, 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception:
            failed += 1
    await lel.edit(
        f"✅ Successfully sent to `{success}` users.\n"
        f"❌ Failed to send to `{failed}` users.\n"
        f"👾 Found `{blocked}` blocked users.\n"
        f"👻 Found `{deactivated}` deactivated users."
    )

print("I'm Alive Now!")
app.run()
