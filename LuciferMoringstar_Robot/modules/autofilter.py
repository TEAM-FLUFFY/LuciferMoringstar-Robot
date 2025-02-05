import re, asyncio, random
# from pyrogram import Client as LuciferMoringstar_Robot, filters as Worker
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from LuciferMoringstar_Robot.database._utils import get_size, split_list
from LuciferMoringstar_Robot.database.autofilter_db import get_filter_results, get_poster
from config import BUTTONS, bot_info, SPELL_MODE, SET_SPEL_M, SUPPORT, BOT_PICS
from translation import LuciferMoringstar


#@LuciferMoringstar_Robot.on_message(Worker.text & Worker.group & Worker.incoming & Worker.chat(AUTH_GROUPS) if AUTH_GROUPS else Worker.text & Worker.group & Worker.incoming)
async def group_filters(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{get_size(file.file_size)} {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", callback_data=f"lucifermoringstar_robot#{file_id}")]
                )
        else:
            if SPELL_MODE:
                reply = search.replace(" ", '+')
                reply_markup = InlineKeyboardMarkup([[
                 InlineKeyboardButton("🎗️ 𝚂𝙴𝙰𝚁𝙲𝙷 𝙾𝙽 𝙶𝙾𝙾𝙶𝙻𝙴 🎗️", url=f"https://www.google.com/search?q={reply}"),
                 ],[
                 InlineKeyboardButton("🔍𝙸𝙼𝙳𝙱", url=f"https://www.imdb.com/find?q={reply}"),
                 InlineKeyboardButton("𝚆𝙸𝙺𝙸𝙿𝙴𝙳𝙸𝙰🔎", url=f"https://en.m.wikipedia.org/w/index.php?search={reply}"),
                 ],[
                 InlineKeyboardButton("👻𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝙰 𝙶𝚁𝙾𝚄𝙿👻", url=f"http://t.me/AH_v3autofilterbot?startgroup=true")
                 ]]  
                )    
                LuciferMoringstar_delete=await message.reply_text(
                    text=SET_SPEL_M.format(query=search, mention=message.from_user.mention),
                    reply_markup=reply_markup                 
                )
                await asyncio.sleep(60) 
                await LuciferMoringstar_delete.delete()
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🎭 𝙿𝙰𝙶𝙴𝚂 1/1",callback_data="pages"),
                 InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴", callback_data="close")]
            )
            buttons.append(
                [InlineKeyboardButton(text="🎗️ 𝙵𝙸𝙻𝙴 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙿𝙼 𝙲𝙷𝙴𝙲𝙺🎗️", url=f"https://telegram.dog/{bot_info.BOT_USERNAME}")]
            )

            imdb=await get_poster(search)
            if imdb and imdb.get('poster'):
                dell=await message.reply_photo(photo=imdb.get('poster'), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(1000)
                await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
            elif imdb:
                dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(1000)
                await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
            else:
                dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_2.format(query=search, mention=message.from_user.mention, chat=message.chat.title), reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(1000)
                await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝙽𝙴𝚇𝚃 𝙿𝙰𝙶𝙴",callback_data=f"nextgroup_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🎭 𝙿𝙰𝙶𝙴𝚂 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴", callback_data="close")]
        )
        buttons.append(
            [InlineKeyboardButton(text="🎗️ 𝙵𝙸𝙻𝙴 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙿𝙼 𝙲𝙷𝙴𝙲𝙺 🎗️", url=f"https://telegram.dog/{bot_info.BOT_USERNAME}")]
        )

        imdb=await get_poster(search)
        if imdb and imdb.get('poster'):
            dell=await message.reply_photo(photo=imdb.get('poster'), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(1000)
            await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")         
        elif imdb:
            dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(1000)
            await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
        else:
            dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_2.format(query=search, mention=message.from_user.mention, chat=message.chat.title), reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(1000)
            await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")



# ---------- Bot PM ---------- #



#@LuciferMoringstar_Robot.on_message(Worker.text & Worker.private & Worker.incoming & Worker.chat(AUTH_GROUPS) if AUTH_GROUPS else Worker.text & Worker.group & Worker.incoming)
async def pm_autofilter(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{get_size(file.file_size)} {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", callback_data=f"pmfile#{file_id}")]
                )
        else:
            await message.reply_photo(
                photo=random.choice(BOT_PICS),
                caption=LuciferMoringstar.ADD_YOUR_GROUP,
                reply_markup=InlineKeyboardMarkup([[
                   InlineKeyboardButton("🔘 REQUEST HERE 🔘", url=f"{SUPPORT}")
                   ]]
                )
            )
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🎭 𝙿𝙰𝙶𝙴𝚂 1/1",callback_data="pages"),
                 InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴", callback_data="close")]
            )


            imdb=await get_poster(search)
            if imdb and imdb.get('poster'):
                dell=await message.reply_photo(photo=imdb.get('poster'), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(1000)
                await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
            elif imdb:
                dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(1000)
                await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
            else:
                dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_2.format(query=search, mention=message.from_user.mention, chat=bot_info.BOT_NAME), reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(1000)
                await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")

            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝙽𝙴𝚇𝚃 𝙿𝙰𝙶𝙴",callback_data=f"nextgroup_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🎭 𝙿𝙰𝙶𝙴𝚂 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴", callback_data="close")]
        )

        imdb=await get_poster(search)
        if imdb and imdb.get('poster'):
            dell=await message.reply_photo(photo=imdb.get('poster'), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(1000)
            await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")         
        elif imdb:
            dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_1.format(mention=message.from_user.mention, query=search, title=imdb.get('title'), genres=imdb.get('genres'), year=imdb.get('year'), rating=imdb.get('rating'), url=imdb['url']), reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(1000)
            await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
        else:
            dell=await message.reply_photo(photo=random.choice(BOT_PICS), caption=LuciferMoringstar.GET_MOVIE_2.format(query=search, mention=message.from_user.mention, chat=bot_info.BOT_NAME), reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(1000)
            await dell.edit(f"⚙️ Filter For {search} Closed 🗑️")
