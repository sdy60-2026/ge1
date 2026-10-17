from pathlib import Path
from html import escape
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
MEMBERS = ROOT / "members"
OUTPUT = ROOT / "_site"

# Διαβάζουμε την κεντρική σελίδα
index_file = ROOT / "index.html"
html = index_file.read_text(encoding="utf-8")

# Βρίσκουμε τα βιογραφικά των μελών
cv_files = sorted(MEMBERS.glob("*.html"))

def prettify_name(filename_stem):
    # Χωρίζει CamelCase π.χ. CamelCase -> Camel Case
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", filename_stem)
    name = name.replace("_", " ").replace("-", " ")
    return name.strip()

def greek_initials(name):
    parts = name.split()
    if len(parts) >= 2:
        return parts[0][0].upper() + parts[1][0].upper()
    elif len(parts) == 1:
        return parts[0][:2].upper()
    return "CV"

cards = []

for cv in cv_files:
    name = prettify_name(cv.stem)
    initials = greek_initials(name)

    card_html = f"""
    <article class="card">
      <div class="avatar">{escape(initials)}</div>
      <h2>{escape(name)}</h2>
      <p>Μέλος της ομάδας</p>
      <a class="btn"
         href="members/{escape(cv.name, quote=True)}"
         target="_blank"
         rel="noopener noreferrer">
         Δες το βιογραφικό →
      </a>
    </article>
    """
    cards.append(card_html.strip())

cards_html = "\n".join(cards)

# Αντικατάσταση placeholder
if "<!-- CV_LINKS -->" not in html:
    raise ValueError("Δεν βρέθηκε το σημείο CV_LINKS στο index.html")

html = html.replace("<!-- CV_LINKS -->", cards_html)

# Δημιουργία καθαρού φακέλου _site
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)

OUTPUT.mkdir()

# Γράφουμε το νέο index.html
(OUTPUT / "index.html").write_text(html, encoding="utf-8")

# Αντιγραφή φακέλου members με όλα τα αρχεία (html, jpg, png κτλ)
output_members = OUTPUT / "members"
shutil.copytree(MEMBERS, output_members)

print(f"Η ιστοσελίδα δημιουργήθηκε με {len(cv_files)} βιογραφικά σε μορφή καρτών.")
