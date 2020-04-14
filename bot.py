""" A simple telegram bot script to send new pictures from a folder to a user
by Alex Bogdanov 2018-04-04
cheers!
"""
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
import os, glob
import time
from os.path import getctime

# path to a folder with pictures
pic_path = r'/share/Public/cam_motion/Entrance/*'
pic_path2_root = r'/share/Public/cam_motion/enrty2/'
import os



import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# dictionary to store latest photo seen by user
# key = user_id
# TODO: implement using context.user_data
last_seen_pic_dic = {}

def callback_sendpic(context):
    """ send the latest photo to user, if he has not received it yet """
    
    last_seen_pics = last_seen_pic_dic.get(context.job.context,['',''])
    latest_files = get_latest_pic()
    for i, (latestSeenPic, latestPic) in enumerate(zip(last_seen_pics, latest_files)):
        if latestSeenPic != latestPic:
            context.bot.send_photo(chat_id=context.job.context, photo=open(latestPic, 'rb'))
            last_seen_pic_dic[context.job.context][i]  = latestPic
            # if 'LINE_CROSS' in latest_file: 
        #     context.bot.send_message(chat_id=context.job.context, text='Line crossing')
        # else:
        #     context.bot.send_message(chat_id=context.job.context, text='Intrusion')

def show_last_photo(update, context):
    """ Send the latest photo in the folder 
    usage: /last
    """
    pics = get_latest_pic()
    for pic in pics:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(pic, 'rb'))

def get_latest_pic():    
    """ Get the latest meaningful files from folders
    my camera makes 4 shots within 6 seconds
    I want to grab the first one in the series (i.e. no older than 7 seconds from the last file) 
    """   
    
    # Camera 1  
    list_of_files = glob.glob(pic_path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    list_of_files.sort(key = os.path.getctime)
    first_file_of_series1 = list(file for file in list_of_files[-10:] if getctime(list_of_files[-1]) - getctime(file)<7)[0] 
   
    # Camera 2

    # get the most recent folder
    # camera creates fodlers each month
    all_subdirs = [os.path.join(pic_path2_root,d) for d in os.listdir(pic_path2_root) if os.path.isdir(os.path.join(pic_path2_root,d))]
    latest_subdir = max(all_subdirs, key=os.path.getmtime)

    list_of_files = glob.glob(latest_subdir + r'/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    list_of_files.sort(key = os.path.getctime)
    first_file_of_series2 = list(file for file in list_of_files[-10:] if getctime(list_of_files[-1]) - getctime(file)<7)[0] 

    print (first_file_of_series1, first_file_of_series2)
    return [first_file_of_series1, first_file_of_series2]


def callback_start(update, context):
    """ entry point for each user, starts calling callback_sendpic every 10 second """
    last_seen_pic_dic[update.message.chat_id] = ['','']
    #context.user_data['last_seen_pic'] = ''
    context.bot.send_message(chat_id=update.message.chat_id, text='Welcome to Camera bot, I will start sending you new photos!')
    context.job_queue.run_repeating(callback_sendpic, interval=10, first=0, context=update.message.chat_id)
    

def pic(update, context):
    """ depricated """
    list_of_files = glob.glob(pic_path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(latest_file, 'rb'))

def main():
    updater = Updater(token='1186794145:AAHl7gK5fXGBa0LZqMBvZqs5yfsg0xjoYgg', use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', callback_start, pass_job_queue=True)
    dispatcher.add_handler(start_handler)

    last_photo__handler = CommandHandler('last', show_last_photo)
    dispatcher.add_handler(last_photo__handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
