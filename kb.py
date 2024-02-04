from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,)


menu = [
    [InlineKeyboardButton(text="📝 Генерировать текст",
                          callback_data="generate_text"),
     InlineKeyboardButton(text="🖼 Генерировать изображение",
                          callback_data="generate_image")],
    [InlineKeyboardButton(text="💳 Купить токены", callback_data="buy_tokens"),
     InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
    [InlineKeyboardButton(text="⚙️ Выбор модели", callback_data="model"),
     InlineKeyboardButton(text="🎁 Бесплатные токены",
                          callback_data="free_tokens")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню",
                                           callback_data="menu")]])
