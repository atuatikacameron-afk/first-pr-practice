"""Build the FAQ and Reviews page sections from src/.

    cd shopify && npm install && python3 build_pages.py

Writes:
  sections/loftrest-faq.liquid       + templates/page.faq.json      (questions pre-filled)
  sections/loftrest-reviews.liquid   + templates/page.reviews.json  (no reviews until you add real ones)
"""
import json, pathlib, re

import twkit

ROOT = pathlib.Path(__file__).resolve().parent
PAGE_SRC = (ROOT.parent / 'index.html').read_text()   # brand colours / tailwind.config
PRODUCT = 'loftrest-neck-traction-device'


def build(name, schema, title):
    src = (ROOT / 'src' / f'{name}.liquid').read_text()
    body = re.sub(r'^\{%- comment -%\}.*?\{%- endcomment -%\}\n', '', src, count=1, flags=re.S)
    body = twkit.prefix_classes(twkit.inline_icons(body))
    css = twkit.compile_css(body, PAGE_SRC)
    liquid = f'''{{%- comment -%}}
  {title}. Generated from src/{name}.liquid by shopify/build_pages.py.
  Edit it in Online Store > Themes > Customize.
{{%- endcomment -%}}
{twkit.FONT_LINKS}
{twkit.style_block(css)}

<div class="loftrest" id="loftrest-{{{{ section.id }}}}">
{body.strip()}
</div>

{{% schema %}}
{json.dumps(schema, indent=2, ensure_ascii=False)}
{{% endschema %}}
'''
    (ROOT / 'sections' / f'{name}.liquid').write_text(liquid)


CONTACT = [
  {"type": "text", "id": "support_email", "label": "Support email", "info": "Leave empty to use your store email."},
]
PRODUCT_SETTING = {"type": "product", "id": "product", "label": "Product for the Shop button"}

# ---------------- FAQ ----------------
FAQ = [
  ("About LoftRest™", "What is LoftRest™?",
   "LoftRest™ is a 3-in-1 cervical traction pillow. It combines gentle air traction, constant-temperature heat and micro-kinetic massage for a 15–30 minute relaxation session, then works as a contoured memory foam pillow you sleep on all night."),
  ("About LoftRest™", "What does it feel like?",
   "Most people describe it as a gentle, lengthening stretch combined with soothing warmth and a light massage. You choose which modes to use and can start on the gentlest setting."),
  ("About LoftRest™", "Can I use the modes separately?",
   "Yes. Use air traction, heat and massage together or one at a time, whichever you find most relaxing."),
  ("About LoftRest™", "What size is it, and what is it made of?",
   "LoftRest™ measures 42.5 × 27 cm (16.7 × 10.6 in). It's made from high-density contoured memory foam with a soft, breathable flannel cover."),
  ("About LoftRest™", "Who is LoftRest™ for?",
   "It's popular with people who spend long days at a desk, people who do physical work, and anyone who finds it hard to get comfortable on their pillow at night."),
  ("Using LoftRest™", "How do I use it?",
   "1. Connect LoftRest™ to a 5V USB power source.\n2. Lie back and rest your neck on the contoured foam.\n3. Turn on the modes you want for a 15–30 minute session.\n4. When the timer switches the modes off, stay put and sleep on the memory foam."),
  ("Using LoftRest™", "How long and how often should I use it?",
   "Each session runs for 15–30 minutes. Most people use it once a day, often in the evening before sleep. Start on the gentlest setting, build up gradually, and stop if anything feels uncomfortable."),
  ("Using LoftRest™", "Can I sleep on it all night?",
   "Yes. That's what it's designed for. After your session, LoftRest™ works as a contoured memory foam pillow until morning."),
  ("Using LoftRest™", "What happens if I fall asleep during a session?",
   "LoftRest™ has a built-in automatic shut-off timer, so the heat, stretch and massage switch off on their own and you can keep sleeping on the pillow."),
  ("Using LoftRest™", "How is it powered?",
   "It runs on a 5V USB connection, so you can plug it into a USB wall adapter, a laptop or a power bank. That also makes it easy to use on the sofa or when you travel."),
  ("Using LoftRest™", "How do I clean it?",
   "Always unplug LoftRest™ before cleaning, never put it in water, and follow the care instructions supplied in the box."),
  ("Safety", "Is LoftRest™ safe to use?",
   "LoftRest™ runs on low-voltage 5V USB power and has an automatic shut-off timer. Start on the gentlest setting and stop if you feel sharp pain, numbness, tingling or dizziness."),
  ("Safety", "Who should not use LoftRest™?",
   "Talk to your doctor before using LoftRest™ if you are pregnant, have had neck or spine surgery, or have osteoporosis, a recent neck injury, rheumatoid arthritis, a known spinal condition, or a circulation disorder."),
  ("Safety", "Is LoftRest™ a medical device?",
   "No. LoftRest™ is a comfort and relaxation product. It is not a medical device and is not designed to diagnose, treat or relieve any medical condition. If you have neck pain or another health concern, see a health professional."),
  ("Orders & shipping", "How much is shipping, and how long does it take?",
   "Standard shipping is free within Australia on orders of A$100 or more and usually takes 7–14 business days. International shipping is A$20 and usually takes 10–25 business days. Shipping costs are always shown at checkout before you pay."),
  ("Orders & shipping", "Which countries do you ship to?",
   "Australia, New Zealand, Canada, the United States, the United Kingdom, Norway, Switzerland, Ireland and 13 other European Union countries, Singapore, Hong Kong, Japan, South Korea, Malaysia, Israel and the United Arab Emirates. You'll see if we ship to you at checkout."),
  ("Orders & shipping", "Will I get tracking?",
   "Yes. Once your order ships, we'll email you tracking details where available."),
  ("Orders & shipping", "Is there a discount for buying two?",
   "Yes. Buy 2 or more LoftRest™ pillows and get 10% off with the code LOFTREST2PACK. If you choose the 2 × LoftRest™ option on the product page, the code is applied for you at checkout."),
  ("Orders & shipping", "Is checkout secure?",
   "Yes. Payments are processed securely by Shopify, and we never see or store your full card details."),
  ("Returns & refunds", "Can I return LoftRest™ if I change my mind?",
   "Yes. You can return it within 30 days of delivery if it's in its original condition and packaging. For change-of-mind returns, you pay the return shipping."),
  ("Returns & refunds", "What if my LoftRest™ is faulty or damaged?",
   "Contact us and we'll arrange a repair, replacement or refund, and cover the return shipping. Your rights under the Australian Consumer Law always apply."),
  ("Returns & refunds", "How do I start a return?",
   "Email us with your order number and the reason for the return, and we'll send you instructions. Please contact us before sending anything back."),
]
faq_schema = {
  "name": "LoftRest FAQ page", "tag": "div", "class": "loftrest-section",
  "settings": [
    {"type": "text", "id": "heading", "label": "Heading", "default": "Frequently asked questions"},
    {"type": "textarea", "id": "intro", "label": "Intro", "default": "Everything you need to know about LoftRest™, shipping and returns."},
    *CONTACT,
    {"type": "text", "id": "phone", "label": "Phone (optional)"},
    PRODUCT_SETTING,
  ],
  "blocks": [{"type": "faq", "name": "Question", "settings": [
    {"type": "text", "id": "category", "label": "Topic", "info": "Questions with the same topic are grouped together, e.g. Shipping"},
    {"type": "text", "id": "question", "label": "Question"},
    {"type": "textarea", "id": "answer", "label": "Answer"}]}],
  "presets": [{"name": "LoftRest FAQ page"}],
}
build('loftrest-faq', faq_schema, 'LoftRest FAQ page')
blocks = {f"faq_{i+1}": {"type": "faq", "settings": {"category": c, "question": q, "answer": a}} for i, (c, q, a) in enumerate(FAQ)}
(ROOT / 'templates' / 'page.faq.json').write_text(json.dumps({"sections": {"main": {
    "type": "loftrest-faq", "blocks": blocks, "block_order": list(blocks),
    "settings": {"product": PRODUCT, "phone": "+61 450 213 111"}}}, "order": ["main"]}, indent=2, ensure_ascii=False) + '\n')

# ---------------- Reviews ----------------
reviews_schema = {
  "name": "LoftRest reviews page", "tag": "div", "class": "loftrest-section",
  "settings": [
    {"type": "text", "id": "heading", "label": "Heading", "default": "What customers say about LoftRest™"},
    {"type": "textarea", "id": "intro", "label": "Intro (shown until you have reviews)", "default": "Honest reviews from real LoftRest™ customers."},
    *CONTACT,
    PRODUCT_SETTING,
  ],
  "blocks": [
    {"type": "@app"},
    {"type": "review", "name": "Customer review", "settings": [
      {"type": "paragraph", "content": "Only add genuine reviews from real customers, with their permission. Don't edit them to change their meaning, and don't leave out negative ones."},
      {"type": "range", "id": "stars", "label": "Stars", "min": 1, "max": 5, "step": 1, "default": 5},
      {"type": "text", "id": "title", "label": "Title"},
      {"type": "textarea", "id": "review", "label": "Review"},
      {"type": "text", "id": "name", "label": "Customer name", "info": "e.g. Sarah, Melbourne"},
      {"type": "text", "id": "date", "label": "Date", "info": "e.g. October 2026"},
      {"type": "checkbox", "id": "verified", "label": "Verified buyer", "default": True, "info": "Only tick if you've matched the review to an order."},
      {"type": "image_picker", "id": "photo", "label": "Customer photo (optional)"},
      {"type": "textarea", "id": "reply", "label": "Your reply (optional)"}]},
  ],
  "presets": [{"name": "LoftRest reviews page"}],
}
build('loftrest-reviews', reviews_schema, 'LoftRest reviews page')
(ROOT / 'templates' / 'page.reviews.json').write_text(json.dumps({"sections": {"main": {
    "type": "loftrest-reviews", "settings": {"product": PRODUCT}}}, "order": ["main"]}, indent=2, ensure_ascii=False) + '\n')

print(f'Wrote FAQ page ({len(FAQ)} questions) and reviews page.')
