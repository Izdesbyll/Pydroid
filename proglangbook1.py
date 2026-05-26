import os
import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from collections import Counter
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# --- YOUR REWRITE LOGIC (Slightly modified for the bot) ---
def process_epub_logic(input_path, output_path, threshold, target_lang):
    # 'auto' lets Google figure out if it's Russian, Norwegian, etc.
    translator = GoogleTranslator(source='auto', target=target_lang)
    global_word_counts = Counter()
    translation_cache = {}
    
    book = epub.read_epub(input_path)
    new_book = epub.EpubBook()
    new_book.metadata = book.metadata
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            for text_node in soup.find_all(string=True):
                if text_node.parent.name in ['script', 'style']: continue
                
                # IMPROVED REGEX: matches Unicode letters (Russian, Arabic, etc.)
                # This ensures Russian words are actually "seen" by the counter
                segments = re.findall(r"[\w]+|[^\w]+", text_node.string, re.UNICODE)
                
                new_segments = []
                for segment in segments:
                    # Check if segment is a word (including Russian letters)
                    if re.match(r"[\w]+", segment, re.UNICODE):
                        word_lower = segment.lower()
                        global_word_counts[word_lower] += 1
                        
                        if global_word_counts[word_lower] > threshold:
                            if word_lower not in translation_cache:
                                try:
                                    translated = translator.translate(word_lower)
                                    # Ensure we got a valid string back
                                    if translated and isinstance(translated, str):
                                        translation_cache[word_lower] = translated
                                        print(f"Translated: {word_lower} -> {translated}")
                                    else:
                                        translation_cache[word_lower] = segment
                                except: 
                                    translation_cache[word_lower] = segment
                            
                            target_word = translation_cache[word_lower]
                            
                            # Casing logic
                            if segment.isupper(): new_segments.append(target_word.upper())
                            elif segment[0].isupper(): new_segments.append(target_word.capitalize())
                            else: new_segments.append(target_word.lower())
                        else:
                            new_segments.append(segment)
                    else:
                        new_segments.append(segment)
                
                text_node.replace_with("".join(new_segments))
            
            item.set_content(str(soup).encode('utf-8'))
        new_book.add_item(item)
    
    new_book.spine = book.spine
    new_book.toc = book.toc
    epub.write_epub(output_path, new_book)

# --- BOT CONVERSATION STATES ---
GET_FILE, GET_LANG, GET_THRESH = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Welcome! Please upload the .epub file you want to translate.")
    return GET_FILE

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save the file locally in Pydroid
    file = await update.message.document.get_file()
    path = f"user_{update.message.chat_id}.epub"
    await file.download_to_drive(path)
    context.user_data['file_path'] = path
    
    await update.message.reply_text("✅ File received! Now, enter the target language code (e.g., 'no' for Bokmål, 'es' for Spanish).")
    return GET_LANG

async def handle_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['lang'] = update.message.text.lower().strip()
    await update.message.reply_text("🔢 After how many times should a word be translated? (Enter a number, e.g., 5)")
    return GET_THRESH

async def handle_thresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        threshold = int(update.message.text)
        chat_id = update.message.chat_id
        input_p = context.user_data['file_path']
        output_p = f"translated_{chat_id}.epub"
        
        await update.message.reply_text("⏳ Processing your book... This may take a moment depending on length.")
        
        # Run the processing logic
        process_epub_logic(input_p, output_p, threshold, context.user_data['lang'])
        
        # Send the file back
        await update.message.reply_document(document=open(output_p, 'rb'), filename="translated_study.epub")
        
        # Cleanup
        os.remove(input_p)
        os.remove(output_p)
        await update.message.reply_text("✨ Done! Enjoy your study.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    
    return ConversationHandler.END

# --- MAIN RUNNER ---
if __name__ == '__main__':
    # Paste your BotFather token here
    TOKEN = "8790707022:AAGdUladscrdLEV19C18o8VTPUMegIIQDn0"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_FILE: [MessageHandler(filters.Document.MimeType("application/epub+zip"), handle_file)],
            GET_LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_lang)],
            GET_THRESH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_thresh)],
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    app.add_handler(conv_handler)
    print("Bot is alive! Go to Telegram and press /start")
    app.run_polling()
