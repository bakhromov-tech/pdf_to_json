import pdfplumber
import re
import json

# Mundarijadagi keraksiz belgilarni olib tashlash funksiyasi
def split_str(text):
    num = ''
    for char in text:
        if char.isalpha() or char == " " or char ==",":
            num+=char
    return num.rstrip()


# pdf faylni ochamiz va uni ishlash uchun qulay qilish uchun txt faylga o'zgartiramiz
with pdfplumber.open('1c.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        with open('text.txt', 'a', encoding='utf-8') as f:
            f.write(text + '\n')


# txt faylni ochib uning ustida amallar ketma-ketligini bajaramiz
with open('text.txt', 'r', encoding='utf-8') as file:
    text = file.read()
lines = text.split('\n')

structure = {}
current_chapter = None
current_title = None
current_section = None
i = 0
for line in lines:
    chapter_match = re.match(r"Глава\s?(\d+)\s+(\d+)", line)
    if chapter_match:
        chapter_number = chapter_match.group(1)
        chapter_title = chapter_match.group(2)
        structure[chapter_number] = {"title": split_str(lines[i+1]), "sections": {}}
        current_chapter = chapter_number
        current_section = None

    section_match = re.match(r"(\d+\.\d+) (.+)", line)
    if section_match and current_chapter:
        section_number = section_match.group(1)
        section_title = section_match.group(2)
        structure[current_chapter]["sections"][section_number] = {"title": split_str(section_title), "subsections": {}}
        current_section = section_number

    subsection_match = re.match(r"(\d+\.\d+\.\d+) (.+)", line)
    if subsection_match and current_section and current_chapter:
        subsection_number = subsection_match.group(1)
        subsection_title = subsection_match.group(2)
        structure[current_chapter]["sections"][current_section]["subsections"][subsection_number] = {
            "title": split_str(subsection_title)}
    if i==322:
        break
    i+=1


with open('structure.json', 'w', encoding='utf-8') as json_file:
    json.dump(structure, json_file, indent=4, ensure_ascii=False)