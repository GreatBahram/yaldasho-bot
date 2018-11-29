import configparser
import logging
from telegram.ext import Updater, CommandHandler
from telegram import UserProfilePhotos, File, ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from functools import wraps
from time import sleep
from PIL import Image
from shutil import copyfile
import os
welcome_message = '''
🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉 \n 
🌹 سلام \n \n \n✳️این ربات با همکاری امیرحسین گودرزی به عنوان برنامه نویس و امین خلیقی به عنوان گرافیست و به منظور احیای شب یلدا و بهتر شدن حال هممون برای یه مدت زمانی طراحی شده.

✳️ فقط کافیه که منتظر بمونین تا عکس پروفایل یلدایی خودتون توسط ربات آماده بشه و از اون توی شبکه‌های اجتماعی مختلف استفاده کنین.

✳️ همچنین این ربات متن باز بوده و سورس کد اون از طریق 🖥 [این لینک](https://github.com/numb95/yaldasho-bot) 🖥 در اختیار همه قرار داره.

✳️ ما رو به دوستاتون معرفی کنید: [یلدایی شو](https://t.me/yaldasho_bot)

'''

wait_message = '''
⭐️تصویر نمایه شما آماده شده است. ربات در حال ارسال آن به شماست.⭐️
'''

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)
        return command_func
    
    return decorator


def image_merge(profile_picture,banner_number):
    im = Image.open(profile_picture, 'r')
    size = 640, 640
    thumbnail = im.resize(size)
    yalda = Image.open('assets/{}.png'.format(banner_number), 'r')
    thumbnail.paste(yalda, (0,0), yalda)
    thumbnail.save(profile_picture, "JPEG")

@send_action(ChatAction.TYPING)
def start(bot , update):
    user_id = update.message.chat_id
    user_name = update.message.chat.username
    done_date = update.message.date
    bot.send_message(chat_id=user_id, text= welcome_message,  parse_mode=ParseMode.MARKDOWN)
    profile_picture_id = bot.getUserProfilePhotos(update.message.chat_id, 0).photos[0][-1].file_id
    profile_picture_file = bot.get_file(profile_picture_id)
    profile_picture_file.download('images/original/{}_@{}_original.jpg'.format(user_id,user_name))
    copyfile('images/original/{}_@{}_original.jpg'.format(user_id,user_name), 'images/edited/{}_@{}_edited.jpg'.format(user_id,user_name))
    bot.send_message(chat_id=user_id, text="دوتا طرح برات ارسال میشه. هرکدوم رو دوست داشتی انتخاب کن تا بر اساس اون تصویر نمایه‌ت ساخته بشه")
    bot.send_photo(chat_id= update.message.chat_id, photo=open('assets/yalda1.jpg', 'rb',), caption='\n\n\n\n\n\n\n /design1 طرح اول')
    bot.send_photo(chat_id= update.message.chat_id, photo=open('assets/yalda2.jpg', 'rb',), caption='\n\n\n\n\n\n\n /design2 طرح دوم')
 
   
def design1(bot, update):
    user_id = update.message.chat_id
    user_name = update.message.chat.username
    done_date = update.message.date
    image_merge('images/edited/{}_@{}_edited.jpg'.format(user_id,user_name),'yalda1')
    bot.send_message(chat_id=update.message.chat_id, text=wait_message)
    bot.send_photo(chat_id= update.message.chat_id, photo=open('images/edited/{}_@{}_edited.jpg'.format(user_id,user_name), 'rb'))
    bot.send_message(chat_id=user_id, text="با تشکر. اگه مجدداً بخواین از ربات استفاده کنین دستور /start رو بزنین. این مورد رو بعداً باید به کد اضافه کنیم و باگ رو برطرف کنیم تا مشکلش برطرف بشه :)")
    os.remove('images/edited/{}_@{}_edited.jpg'.format(user_id,user_name))
    os.remove('images/original/{}_@{}_original.jpg'.format(user_id,user_name))
def design2(bot, update):
    user_id = update.message.chat_id
    user_name = update.message.chat.username
    done_date = update.message.date
    image_merge('images/edited/{}_@{}_edited.jpg'.format(user_id,user_name),'yalda2')
    bot.send_message(chat_id=update.message.chat_id, text=wait_message)
    bot.send_photo(chat_id= update.message.chat_id, photo=open('images/edited/{}_@{}_edited.jpg'.format(user_id,user_name), 'rb'))
    bot.send_message(chat_id=user_id, text="با تشکر. اگه مجدداً بخواین از ربات استفاده کنین دستور /start رو بزنین. این مورد رو بعداً باید به کد اضافه کنیم و باگ رو برطرف کنیم تا مشکلش برطرف بشه :)")
    os.remove('images/edited/{}_@{}_edited.jpg'.format(user_id,user_name))
    os.remove('images/original/{}_@{}_original.jpg'.format(user_id,user_name))

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(name)s - %(message)s', level=logging.INFO)
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['app-conf']['token']
    updater = Updater(token=token)
    start_handler = CommandHandler ('start',start)
    updater.dispatcher.add_handler(start_handler)
    design1_handler = CommandHandler ('design1', design1)
    updater.dispatcher.add_handler(design1_handler)
    design2_handler = CommandHandler ('design2', design2)
    updater.dispatcher.add_handler(design2_handler)

    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()


