""" A simple telegram bot script to send new pictures from a folder to a user
by Alex Bogdanov 2018-04-04
cheers!
"""
from typing import Dict, List, Tuple

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
import os, glob
import time
from os.path import getctime
import tempfile

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import camerabot.file_utils as file_utils
import camerabot.images_utils as images_utils
from config import PATH_TO_IMAGES, CHECK_SUBFOLDER

import os
TELEGRAM_CAMERA_BOT_TOKEN = os.environ.get('TELEGRAM_CAMERA_BOT_TOKEN')

# path to a folders with pictures
#pic_path = r'/share/Public/cam_motion/Entrance/*'
pic_path1_root = r'/share/Public/cam_motion/Entrance/'
pic_path2_root = r'/share/Public/cam_motion/enrty2/'

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# dictionary to store latest photo seen by user
# key = user_id
# TODO: implement using context.user_data
last_seen_pic_dic = {}

def callback_sendpic(context):
    """ 
    send the latest photos to user, if he has not received it yet 
    """
    
    last_seen_pics = last_seen_pic_dic.get(context.job.context, ['' for _ in range(len(PATH_TO_IMAGES))])
    
    logging.debug('Latest pics: %s'  % str(last_seen_pic_dic))
    
    
    latest_files = get_latest_pic()
    
    for i, (latestSeenPic, latestPic) in enumerate(zip(last_seen_pics, latest_files)):
        if latestSeenPic != latestPic:
            # generate images with boxes around movement
            latestPicWBoxes = get_latest_pic_w_boxes()
            context.bot.send_photo(chat_id=context.job.context, photo=open(latestPicWBoxes[i], 'rb'))
            last_seen_pic_dic[context.job.context][i]  = latestPic
            # if 'LINE_CROSS' in latest_file: 
        #     context.bot.send_message(chat_id=context.job.context, text='Line crossing')
        # else:
        #     context.bot.send_message(chat_id=context.job.context, text='Intrusion')

def show_last_photo(update, context):
    """ Send the latest photo in the folder 
    usage: /last
    """
    pics = get_latest_pic_w_boxes()
    for pic in pics:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(pic, 'rb'))

def get_latest_pic() -> List[str]:    
    """ Get the latest meaningful files from folders
    my camera makes 4 shots within 6 seconds
    I want to grab the first one in the series (i.e. no older than 7 seconds from the last file) 
    """   
    
    imageList = []

    for parentFolder in PATH_TO_IMAGES:
        logging.debug(f'Checking folder: {parentFolder}')
        if not os.path.exists(parentFolder):
            imageList.append('')
            continue
        # all directories in parentFolder:
        
        if CHECK_SUBFOLDER:
            all_subdirs = [os.path.join(parentFolder,d) for d in os.listdir(parentFolder) if os.path.isdir(os.path.join(parentFolder,d))]
        else:
            all_subdirs = [parentFolder,]

        
        if  all_subdirs:
            latest_subdir = max(all_subdirs, key=os.path.getmtime)
            logging.debug(f'Latest subfolder: {latest_subdir}')

            #list_of_files = glob.glob(pic_path) # * means all if need specific format then *.csv
            list_of_files = glob.glob(latest_subdir + r'/*') # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)

            list_of_files.sort(key = os.path.getctime)
            first_file_of_series = list(file for file in list_of_files[-10:] if getctime(list_of_files[-1]) - getctime(file)<7)[0] 
        else:
            first_file_of_series = ''
        
        imageList.append(first_file_of_series)    

    logging.debug(f'Found files: {imageList}')

    return imageList

def get_latest_pic_w_boxes() -> List[str]:    
    """ Get the latest meaningful files from folders with boxes around moving objects
    my camera makes 4 shots within 6 seconds
    I want to grab the first one in the series (i.e. no older than 7 seconds from the last file) 
    boxes are determined by comparing with the last image in series (typially by then the object is gone)
    """   
    
    imageList = []
    for parentFolder in PATH_TO_IMAGES:
        if not os.path.exists(parentFolder):
            imageList.append('')
            continue

        if CHECK_SUBFOLDER:
            all_subdirs = [os.path.join(parentFolder,d) for d in os.listdir(parentFolder) if os.path.isdir(os.path.join(parentFolder,d))]
        else:
            all_subdirs = [parentFolder,]
        if not all_subdirs:
            imageList.append('')
            continue
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        groupedFiles = file_utils.groupPicsByTime(latest_subdir)

        lastImage, firstImage = groupedFiles[-1][-1], groupedFiles[-1][0]
        tmpFile1Path = images_utils.compare_two_images_3(firstImage, lastImage, None)
        imageList.append(tmpFile1Path)

    return imageList


def callback_start(update, context):
    """ 
    entry point for each user, starts calling callback_sendpic every 10 second 
    """
    
    # initializing dictionary with user key
    last_seen_pic_dic[update.message.chat_id] = ['' for _ in range(len(PATH_TO_IMAGES))]

    context.bot.send_message(chat_id=update.message.chat_id, text='Welcome to Camera bot, I will start sending you new photos!')
    context.job_queue.run_repeating(callback_sendpic, interval=10, first=0, context=update.message.chat_id)
    

# def pic(update, context):
#     """ depricated """
#     list_of_files = glob.glob(pic_path) # * means all if need specific format then *.csv
#     latest_file = max(list_of_files, key=os.path.getctime)
#     context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(latest_file, 'rb'))

def main():
    print('Starting the camera bot')
    print(f'With the token: {TELEGRAM_CAMERA_BOT_TOKEN}')
    updater = Updater(token=TELEGRAM_CAMERA_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', callback_start, pass_job_queue=True)
    dispatcher.add_handler(start_handler)

    last_photo__handler = CommandHandler('last', show_last_photo)
    dispatcher.add_handler(last_photo__handler)

    updater.start_polling()

def test_images_utils():
    # test
    print('Testing image_utils...')
    images_utils.main()


if __name__ == '__main__':
    main()
    #test_images_utils()
    
