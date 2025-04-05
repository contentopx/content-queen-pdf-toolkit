import fitz  # PyMuPDF
import os
import re

# ----------- SETTINGS -----------
PDF_FOLDER = "OriginalPDFs"
OUTPUT_FOLDER = "pdf SA version"
FONT_PATH = "NotoSans-Regular.ttf"
# --------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

pattern = re.compile(r"Openstax\s+CC\s+BY[-\u2013]\s*NC", re.IGNORECASE)
replacement_text = "Openstax CC BY NC SA"

edited_files = []
no_match_files = []
mismatch_files = []

for filename in os.listdir(PDF_FOLDER):
    if filename.endswith(".pdf"):
        file_path = os.path.join(PDF_FOLDER, filename)
        doc = fitz.open(file_path)
        total_pages = len(doc)
        updated = False
        match_count = 0

        print(f"\n🔍 Checking: {filename} ({total_pages} pages)")

        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("blocks")
            for block in blocks:
                text = block[4]
                match = pattern.search(text)
                if match:
                    match_count += 1
                    updated = True
                    print(f"  🟢 Match #{match_count} on page {page_num}")
                    bbox = block[:4]
                    page.add_redact_annot(fitz.Rect(bbox), fill=(1, 1, 1))
                    page.apply_redactions()
                    page.insert_text(
                        (bbox[0], bbox[1]),
                        replacement_text,
                        fontsize=11.0,
                        fontfile=FONT_PATH,
                        fill=(0, 0, 0)
                    )

        if updated:
            new_filename = filename.replace(".pdf", "_SA.pdf")
            new_path = os.path.join(OUTPUT_FOLDER, new_filename)
            doc.save(new_path)
            edited_files.append((filename, match_count, total_pages))
            if match_count != total_pages:
                mismatch_files.append(filename)
            print(f"✅ Saved: {new_filename} 🎉 (Matches: {match_count} / Pages: {total_pages})")
        else:
            no_match_files.append((filename, total_pages))
            print("⚠️ No match found. Original left untouched.")

        doc.close()

# 👑📋 FINAL ROYAL DECREE 📋👑
border = "🌟👑" * 10
print("\n\n" + border)
print("       👑✨ FINAL ROYAL DECREE ✨👑")
print(border + "\n")

if edited_files:
    print("👸🏼 Royal Scrolls of Triumph — PDFs Transformed with Magic and Majesty:")
    for name, matches, pages in edited_files:
        emoji = "👑" if matches == pages else ""
        print(f"  👑 {name} → {matches} enchanted page(s) out of {pages} {emoji}")
    print()

if mismatch_files:
    print("🔮 Files with Partial Magic (pages ≠ matches):")
    for name in mismatch_files:
        print(f"  ⚠️ {name} — please review these suspicious scrolls again, royal one 🧐")
    print()

if no_match_files:
    print("❄️ Scrolls That Resisted All Spells (No Matches Found):")
    for name, pages in no_match_files:
        print(f"  ❌ {name} ({pages} royal pages) — untouched by charm ✋✨")
else:
    print("🎉 All scrolls were blessed with sparkle and style! Rejoice, Queen of the Digital Realm! 👑")

print("\n❤️ Go get a snack, content queen — you’ve earned it. 🧁✨ 👑")
print(border + "\n")
