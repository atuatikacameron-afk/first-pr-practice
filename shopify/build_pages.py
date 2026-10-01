"""Build the FAQ and Reviews page sections from src/.

    cd shopify && npm install && python3 build_pages.py

Writes:
  sections/loftrest-faq.liquid       + templates/page.faq.json      (questions pre-filled)
  sections/loftrest-reviews.liquid   + templates/page.reviews.json  (customer reviews from reviews_data.py)
"""
import json, pathlib, re

import reviews_data, twkit

ROOT = pathlib.Path(__file__).resolve().parent
PAGE_SRC = (ROOT.parent / 'index.html').read_text()   # brand colours / tailwind.config
PRODUCT = 'loftrest-neck-traction-device'


def build(name, schema, title):
    src = (ROOT / 'src' / f'{name}.liquid').read_text()
    body = re.sub(r'^\{%- comment -%\}.*?\{%- endcomment -%\}\n', '', src, count=1, flags=re.S)
    body, slots = twkit.expand_slots(body)
    for sid, label in slots:
        schema["settings"].append({"type": "image_picker", "id": sid, "label": label})
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
      reviews_data.STARS,
      {"type": "text", "id": "title", "label": "Title"},
      {"type": "textarea", "id": "review", "label": "Review"},
      {"type": "text", "id": "name", "label": "Customer name", "info": "e.g. Sarah, Melbourne"},
      {"type": "text", "id": "date", "label": "Date", "info": "e.g. October 2026"},
      {"type": "checkbox", "id": "verified", "label": "Verified buyer", "default": True, "info": "Only tick if you've matched the review to an order."},
      reviews_data.SOURCE_SETTING,
      {"type": "image_picker", "id": "photo", "label": "Customer photo (optional)"},
      {"type": "textarea", "id": "reply", "label": "Your reply (optional)"}]},
  ],
  "presets": [{"name": "LoftRest reviews page"}],
}
build('loftrest-reviews', reviews_schema, 'LoftRest reviews page')
(ROOT / 'templates' / 'page.reviews.json').write_text(json.dumps({"sections": {"main": {
    "type": "loftrest-reviews", "blocks": reviews_data.blocks(), "block_order": list(reviews_data.blocks()),
    "settings": {"product": PRODUCT}}}, "order": ["main"]}, indent=2, ensure_ascii=False) + '\n')

# ---------------- Footer ----------------
footer_schema = {
  "name": "LoftRest footer", "tag": "div", "class": "loftrest-section",
  "enabled_on": {"groups": ["footer"]},
  "settings": [
    {"type": "textarea", "id": "tagline", "label": "Tagline", "default": "Relax first, then sleep. The 3-in-1 cervical traction pillow with air traction, heat, massage and all-night memory foam support."},
    PRODUCT_SETTING,
    {"type": "header", "content": "Newsletter"},
    {"type": "checkbox", "id": "show_newsletter", "label": "Show email signup", "default": True},
    {"type": "text", "id": "newsletter_heading", "label": "Signup heading", "default": "Get tips for better wind-downs and first access to offers"},
    {"type": "header", "content": "Links"},
    {"type": "link_list", "id": "shop_menu", "label": "Shop menu (optional)", "info": "Leave empty to show Why LoftRest and Reviews."},
    {"type": "link_list", "id": "help_menu", "label": "Help menu (optional)", "info": "Leave empty to show FAQ, Shipping, Returns and Contact."},
    {"type": "header", "content": "Contact"},
    *CONTACT,
    {"type": "text", "id": "phone", "label": "Phone"},
    {"type": "text", "id": "location", "label": "Location", "info": "e.g. Melbourne, Australia. Leave empty to hide."},
    {"type": "text", "id": "abn", "label": "ABN", "info": "Shown next to the copyright. Leave empty to hide."},
    {"type": "header", "content": "Social"},
    {"type": "url", "id": "instagram", "label": "Instagram"},
    {"type": "url", "id": "tiktok", "label": "TikTok"},
    {"type": "url", "id": "facebook", "label": "Facebook"},
    {"type": "url", "id": "youtube", "label": "YouTube"},
  ],
  "presets": [{"name": "LoftRest footer"}],
}
build('loftrest-footer', footer_schema, 'LoftRest footer')
(ROOT / 'sections' / 'footer-group.json').write_text(json.dumps({
    "type": "footer", "name": "Footer",
    "sections": {"loftrest_footer": {"type": "loftrest-footer",
                 "settings": {"product": PRODUCT, "phone": "+61 450 213 111", "location": "Melbourne, Australia", "show_newsletter": True}}},
    "order": ["loftrest_footer"]}, indent=2, ensure_ascii=False) + '\n')

# ---------------- About ----------------
about_schema = {
  "name": "LoftRest about page", "tag": "div", "class": "loftrest-section",
  "settings": [
    {"type": "paragraph", "content": "Tell your real story. Keep it about comfort and relaxation, not medical results (see COMPLIANCE.md)."},
    {"type": "text", "id": "founder_name", "label": "Founder name", "info": "Shown under the quote. Leave empty to show 'Founder of LoftRest'."},
    {"type": "text", "id": "heading", "label": "Heading", "default": "Built for two people who needed rest"},
    {"type": "textarea", "id": "intro", "label": "Intro", "default": "LoftRest™ started at home. I was working 10+ hour days and finishing every one with a stiff, sore neck. My girlfriend was lying awake most nights, struggling to switch off. Between the two of us, nobody was getting the rest we needed."},
    {"type": "header", "content": "Your story"},
    {"type": "text", "id": "me_label", "label": "Label", "default": "Me"},
    {"type": "text", "id": "me_heading", "label": "Heading", "default": "10+ hour days, and a neck that never got a break"},
    {"type": "textarea", "id": "me_text", "label": "Story", "default": "Most days I work more than 10 hours. By the time I got home, my neck and shoulders were tight and sore, and no pillow I tried ever felt right. I'd lie down wanting to rest and just couldn't get comfortable."},
    {"type": "header", "content": "Her story"},
    {"type": "text", "id": "her_label", "label": "Label", "default": "Her"},
    {"type": "text", "id": "her_heading", "label": "Heading", "default": "Long nights, lying awake"},
    {"type": "textarea", "id": "her_text", "label": "Story", "default": "My girlfriend has struggled with sleep for as long as I've known her. She'd lie awake long after the lights went out, trying everything she could think of to wind down."},
    {"type": "header", "content": "Turning point"},
    {"type": "textarea", "id": "quote", "label": "Quote", "default": "One night, both of us lying awake, I'd had enough. I set out to make the most comfortable headrest we could, and then build the rest around it."},
    {"type": "header", "content": "Building LoftRest"},
    {"type": "text", "id": "build_heading", "label": "Heading", "default": "We started with the headrest. Then we built the rest."},
    {"type": "textarea", "id": "build_text", "label": "Text", "default": "The pillow came first: something that would support my neck after a long day and give her somewhere comfortable to settle. Then we added the wind-down, so our evenings could be a moment to relax together instead of one more thing to push through."},
    {"type": "header", "content": "Call to action"},
    {"type": "text", "id": "cta_heading", "label": "Heading", "default": "Now it's your turn to rest"},
    {"type": "text", "id": "cta_text", "label": "Text", "default": "Relax first, then sleep, supported. Try LoftRest™ with 30-day change-of-mind returns."},
    PRODUCT_SETTING,
    {"type": "header", "content": "Images"},
  ],
  "presets": [{"name": "LoftRest about page"}],
}
build('loftrest-about', about_schema, 'LoftRest about page')
(ROOT / 'templates' / 'page.about.json').write_text(json.dumps({"sections": {"main": {
    "type": "loftrest-about", "settings": {"product": PRODUCT, "hero_image": "shopify://shop_images/loftrest-hero.webp"}}},
    "order": ["main"]}, indent=2, ensure_ascii=False) + '\n')

print(f'Wrote FAQ page ({len(FAQ)} questions), reviews page, footer and about page.')
