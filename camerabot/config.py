# config.py: contains some definitions
#
# PATH_TO_IMAGES: path to folders, with images
# if CHECK_SUBFOLDER = True, finding the latest subfolder in the path
# you can add fodler, that does not exist, it will be ignored
# in my case each camera creates a folder every month
# so I need to point to the parent folder, and the script will find the latest folder automatically
#
# ├── Entrance
# │   ├── 2020_04_13-2020_05_12
# │   └── 2020_05_13-2020_06_11
# ├── alley
# └── enrty2
#     ├── 2020_04_04-2020_05_03
#     └── 2020_05_04-2020_06_02

PATH_TO_IMAGES = (
    r'/share/Public/cam_motion/Entrance/',
    r'/share/Public/cam_motion/enrty2/',
    r'/Users/sash/mnt/zavulon_pub/cam_motion/Entrance/',
    r'/Users/sash/mnt/zavulon_pub/cam_motion/enrty2/',
    )
# looks for the latest subfolder in the path fron PATH_TO_IMAGES if True
# otherwise uses the path from PATH_TO_IMAGES  itself
CHECK_SUBFOLDER = True





