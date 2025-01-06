from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from PIL import Image
import imageio
import os

TOKEN = "Y7606766248:AAF7vMiguoJhAyrVp2JvIhOrxX68IVHe-Uo"  # Replace with your bot token
IMAGE_DIR = "images/"  # Folder to save images

os.makedirs(IMAGE_DIR, exist_ok=True)
user_images = {}  # Store user images temporarily

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send me two images, and I'll create a fading GIF for you! 📷✨")

async def handle_photo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]  # Get highest resolution photo
    file = await context.bot.get_file(photo.file_id)
    
    image_path = os.path.join(IMAGE_DIR, f"{user_id}_{len(user_images.get(user_id, []))}.jpg")
    await file.download_to_drive(image_path)

    user_images.setdefault(user_id, []).append(image_path)

    if len(user_images[user_id]) == 2:
        await update.message.reply_text("Creating GIF... ⏳")
        gif_path = os.path.join(IMAGE_DIR, f"{user_id}_output.gif")
        create_fade_gif(user_images[user_id][0], user_images[user_id][1], gif_path)
        
        await update.message.reply_document(document=open(gif_path, "rb"))
        user_images[user_id] = []  # Reset user images after processing
    else:
        await update.message.reply_text("Got the first image! Now send the second one.")

def create_fade_gif(image1_path, image2_path, output_gif, frames=20, duration=100, resize_factor=0.5, hold_first_image=10):
    img1 = Image.open(image1_path).convert("RGBA")
    img2 = Image.open(image2_path).convert("RGBA")

    new_size = (int(img1.width * resize_factor), int(img1.height * resize_factor))
    img1 = img1.resize(new_size, Image.LANCZOS)
    img2 = img2.resize(new_size, Image.LANCZOS)

    images = []
    for _ in range(hold_first_image):
        images.append(img1.copy())

    for i in range(frames + 1):
        alpha = i / frames
        blended = Image.blend(img1, img2, alpha)
        images.append(blended)

    for _ in range(hold_first_image // 2):
        images.append(img2.copy())

    images[0].save(output_gif, save_all=True, append_images=images[1:], duration=duration, loop=0, optimize=True)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # ✅ Fixed filters

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
