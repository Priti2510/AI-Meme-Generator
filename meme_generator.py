import os
import requests
import textwrap
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageFilter
from transformers import pipeline

OUTPUT_DIR = "generated_memes"
TEMPLATE_DIR = "templates"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

try:
    DEFAULT_FONT = ImageFont.truetype("Impact.ttf", 40)
except OSError:
    DEFAULT_FONT = ImageFont.truetype("arial.ttf", 40)

sentiment_analyzer = pipeline("sentiment-analysis")
context_classifier = pipeline("zero-shot-classification")

def select_template_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Template Image or GIF",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")]
    )
    return file_path

def download_templates(limit=5):
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Could not fetch Imgflip templates")
        return []
    memes = response.json()["data"]["memes"][:limit]
    paths = []
    for meme in memes:
        filename = os.path.join(TEMPLATE_DIR, f"{meme['id']}.jpg")
        if not os.path.exists(filename):
            img_data = requests.get(meme["url"]).content
            with open(filename, "wb") as f:
                f.write(img_data)
        paths.append(filename)
    return paths

def choose_best_template(prompt, templates):
    candidate_labels = ["confusion", "happiness", "sadness", "anger", "teamwork", "failure", "success"]
    result = context_classifier(prompt, candidate_labels)
    print(f"📊 Context detected: {result['labels'][0]}")
    return random.choice(templates)

def generate_caption(prompt):
    sentiment = sentiment_analyzer(prompt)[0]["label"]
    if sentiment == "NEGATIVE":
        return f"When everything goes wrong :: {prompt}"
    elif sentiment == "POSITIVE":
        return f"{prompt} :: Best day ever!"
    else:
        return prompt

def add_text_to_image(img, caption, watermark=None):
    draw = ImageDraw.Draw(img)
    font_size = int(img.height * 0.08)
    try:
        font = ImageFont.truetype("Impact.ttf", size=font_size)
    except OSError:
        font = ImageFont.truetype("arial.ttf", size=font_size)

    if "::" in caption:
        top_text, bottom_text = caption.split("::", 1)
    else:
        top_text, bottom_text = caption, ""

    def draw_text(text, y_pos):
        lines = textwrap.wrap(text, width=25)
        y = y_pos
        for line in lines:
            w, h = draw.textbbox((0, 0), line, font=font)[2:]
            x = (img.width - w) / 2
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    draw.text((x+dx, y+dy), line, font=font, fill="black")
            draw.text((x, y), line, font=font, fill="white")
            y += h + 5

    if top_text.strip():
        draw_text(top_text.strip(), 10)
    if bottom_text.strip():
        draw_text(bottom_text.strip(), img.height - font_size*2)

    if watermark:
        wm_font = ImageFont.truetype("arial.ttf", size=int(img.height * 0.03))
        draw.text((10, img.height - 30), watermark, font=wm_font, fill="gray")

    return img

def process_gif(template_path, caption, output_path, watermark="AI MemeGen"):
    img = Image.open(template_path)
    frames = []
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("RGB")
        frame = add_text_to_image(frame, caption, watermark)
        frames.append(frame)
    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, duration=img.info.get("duration", 100))

def generate_memes(prompts, batch_size=3, watermark="AI MemeGen", style=None, custom_template=None):
    """
    Generates memes for a list of prompts.
    Displays the saved file paths after generation.
    """
    templates = [custom_template] if custom_template else download_templates(limit=batch_size)
    all_outputs = []

    for idx, prompt in enumerate(prompts):
        best_template = choose_best_template(prompt, templates)
        caption = generate_caption(prompt)
        variations = [caption, caption.upper(), f"{prompt}::Relatable!"]

        for var_idx, var in enumerate(variations):
            ext = os.path.splitext(best_template)[-1].lower()
            output_file = os.path.join(OUTPUT_DIR, f"meme_{idx}_{var_idx}{ext}")

            if ext == ".gif":
                process_gif(best_template, var, output_file, watermark)
            else:
                img = Image.open(best_template).convert("RGB")
                img = add_text_to_image(img, var, watermark)

                if style == "grayscale":
                    img = img.convert("L").convert("RGB")
                elif style == "cartoon":
                    img = img.filter(ImageFilter.BLUR).filter(ImageFilter.CONTOUR)

                img.save(output_file)

            all_outputs.append(output_file)

    print(f"\n✅ Generated {len(all_outputs)} memes:")
    for i, path in enumerate(all_outputs, start=1):
        print(f"{i}. {path}")

    return all_outputs


if __name__ == "__main__":
    while True:
        print("\n🎭 AI Meme Generator 🎭")
        print("1. Single Prompt")
        print("2. Multiple Prompts (comma separated)")
        print("3. From file (prompts.txt)")
        print("4. Custom Template Upload")
        print("5. Batch Generate from prompts.txt")
        print("6. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            prompt = input("Enter meme idea: ")
            generate_memes([prompt])
        elif choice == "2":
            prompts = input("Enter meme ideas (comma separated): ").split(",")
            generate_memes([p.strip() for p in prompts])
        elif choice == "3":
            if os.path.exists("prompts.txt"):
                with open("prompts.txt") as f:
                    prompts = [line.strip() for line in f if line.strip()]
                generate_memes(prompts, batch_size=5)
            else:
                print("❌ No prompts.txt file found")
        elif choice == "4":
            print("Select your custom template file:")
            template_path = select_template_file()
            if not template_path:
                print("❌ No file selected. Returning to menu.")
                continue
            prompt = input("Enter meme idea: ")
            style = input("Style? (none/grayscale/cartoon): ").strip().lower()
            generate_memes([prompt], custom_template=template_path, style=style)
        elif choice == "5":
            if os.path.exists("prompts.txt"):
                with open("prompts.txt") as f:
                    prompts = [line.strip() for line in f if line.strip()]
                print(f"📄 Generating memes for {len(prompts)} prompts...")
                generate_memes(prompts, batch_size=5)
            else:
                print("❌ No prompts.txt file found")
        elif choice == "6":
            print("👋 Exiting AI Meme Generator. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")

        # Ask if user wants to continue
        cont = input("\nDo you want to create another meme? (yes/no): ").strip().lower()
        if cont not in ["yes", "y"]:
            print("✅ Done! Exiting AI Meme Generator.")
            break
