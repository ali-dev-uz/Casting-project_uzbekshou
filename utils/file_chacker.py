import os


async def is_image(filename):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    file_extension = os.path.splitext(filename)[-1].lower()
    return file_extension in image_extensions


async def is_video(filename):
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
    file_extension = os.path.splitext(filename)[-1].lower()
    return file_extension in video_extensions



