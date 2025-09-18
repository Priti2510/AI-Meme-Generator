# 🎭 AI Meme Generator

An **AI-powered meme generator** that creates relevant memes from text prompts using **image generation, text overlay, and AI-based context understanding**.

---

## **Features**

### Core Features

* Text-to-meme generation from prompts
* Template selection (AI-based context matching)
* Caption generation with humor detection
* Top and bottom text overlay
* Batch meme generation
* Watermarking

### Bonus Features

* Custom template upload
* Trending meme tracking (Imgflip)
* Style transfer: `grayscale` or `cartoon`
* GIF support (text overlay frame-by-frame)
* Multiple formats: JPG, PNG, GIF

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/<username>/AI-Meme-Generator.git
cd AI-Meme-Generator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## **Usage**

Run the meme generator:

```bash
python meme_generator.py
```

You will see options:

```
🎭 AI Meme Generator 🎭
1. Single Prompt
2. Multiple Prompts (comma separated)
3. From file (prompts.txt)
4. Custom Template Upload
5. Batch Generate from prompts.txt
```

### **Option Details**

* **1. Single Prompt** – Enter one meme idea at a time.
* **2. Multiple Prompts** – Enter multiple ideas separated by commas.
* **3. From file** – Generate memes from `prompts.txt`.
* **4. Custom Template Upload** – Provide your own image or GIF template.
* **5. Batch Generate** – Automatically generate all 50+ memes from `prompts.txt`.

---

## **Generating 50+ Memes**

1. Ensure `prompts.txt` has all your meme ideas (one per line).
2. Run the generator and choose **option 3 or 5**.
3. Memes are saved in:

```
generated_memes/
```

* Each prompt produces **3 variations** by default.
* Optional styles: `grayscale` or `cartoon`.
* Watermark: `"AI MemeGen"` (can be customized in code).

---

## **Adding Custom Templates**

* Place your image/GIF templates in the `templates/` folder or use **option 4** during runtime.
* The AI will use them instead of default templates.

---

## **Folder Structure**

```
MemeGenerator/
├── meme_generator.py
├── requirements.txt
├── README.md
├── prompts.txt
├── templates/         # meme templates
├── generated_memes/   # generated memes (ignored in GitHub)
├── .gitignore         # ignores generated memes and cache files
```

---

## **Tips**

* Keep `generated_memes/` ignored in GitHub to avoid large files.
* You can edit `prompts.txt` to add new meme ideas anytime.
* Optional styles and watermark can be
