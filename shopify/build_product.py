"""Build the Shopify product page section from src/loftrest-product.liquid.

    cd shopify && npm install && python3 build_product.py

Writes:
  shopify/sections/loftrest-product.liquid   (the product page, as a theme section)
  shopify/templates/product.loftrest.json    (product template that uses it, FAQ and offers pre-filled)
"""
import json, pathlib, re

import reviews_data, twkit

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT / 'src' / 'loftrest-product.liquid').read_text()
page_src = (ROOT.parent / 'index.html').read_text()   # brand colours / tailwind.config

body = re.sub(r'^\{%- comment -%\}.*?\{%- endcomment -%\}\n', '', src, count=1, flags=re.S)
body = twkit.inline_icons(body)
body = twkit.prefix_classes(body)
compiled_css = twkit.compile_css(body, page_src)

faqs = [
  ("What does LoftRest™ feel like?",
   "Most people describe it as a gentle stretch combined with soothing warmth and a light massage. You choose which modes to use and can start on the gentlest setting. LoftRest™ is a comfort and relaxation product. It is not a medical device and is not designed to treat pain or any medical condition. If you have neck pain, see a health professional."),
  ("Is it safe to sleep on LoftRest™ all night?",
   "Yes. That's what it's designed for. The built-in automatic shut-off timer switches off the heat, stretch and massage at the end of a session, and LoftRest™ then works as a contoured memory foam pillow until morning."),
  ("How long should I use it each day?",
   "Each LoftRest™ session runs for 15–30 minutes. Most people use it once a day, often in the evening before sleep. Start on the gentlest setting, build up gradually, and stop if anything feels uncomfortable."),
  ("Will it help me get comfortable at night?",
   "A relaxing wind-down before bed and a pillow that supports your neck can make it easier to get comfortable. LoftRest™ gives you both: a 15–30 minute session to unwind, then contoured memory foam to sleep on."),
  ("Is it good after a long day at a desk?",
   "Many people use LoftRest™ to unwind after long days at a screen: lie back, let the warmth and gentle stretch relax you, then drift off on the memory foam. Regular screen breaks and a raised monitor are good habits too."),
  ("Who should not use LoftRest™?",
   "Talk to your doctor before using LoftRest™ if you are pregnant, have had neck or spine surgery, or have osteoporosis, a recent neck injury, rheumatoid arthritis, a known spinal condition, or a circulation disorder. LoftRest™ is a comfort and relaxation product, not a medical device."),
  ("How is LoftRest™ powered?",
   "It runs on a 5V USB connection, so you can plug it into a USB wall adapter, a laptop or a power bank."),
  ("What size is it?",
   "LoftRest™ measures 42.5 × 27 cm (16.7 × 10.6 in). It's made from high-density contoured memory foam with a soft, breathable flannel cover."),
  ("How long does shipping take, and can I return it?",
   "Standard shipping is free within Australia and usually takes 7–14 business days. International shipping is A$20 and usually takes 10–25 business days. If you change your mind, you can return LoftRest™ within 30 days, and faulty items are always covered. Full details are in our shipping and refund policies. Both are linked at the bottom of this page."),
]

schema = {
  "name": "LoftRest product page",
  "tag": "div",
  "class": "loftrest-section",
  "settings": [
    {"type": "text", "id": "subtitle", "label": "Short description", "default": "A 3-in-1 cervical traction pillow: a 15–30 minute relaxation session of gentle air traction, heat and massage, then all-night neck support."},
    {"type": "checkbox", "id": "go_to_checkout", "label": "Add to cart goes straight to checkout", "default": True},
    {"type": "header", "content": "Trust"},
    {"type": "text", "id": "shipping_note", "label": "Shipping promise", "default": "Free standard shipping in Australia", "info": "Only say what your shipping settings really offer. Leave empty to hide."},
    {"type": "text", "id": "returns_label", "label": "Returns link text", "default": "30-day returns", "info": "Shown when your store has a refund policy. Keep it in line with that policy."},
    {"type": "checkbox", "id": "show_trial", "label": "Show trial badge", "default": False, "info": "Only turn on if you really offer a trial with a full refund."},
    {"type": "range", "id": "trial_days", "label": "Trial length (nights)", "min": 7, "max": 100, "step": 1, "default": 30},
    {"type": "text", "id": "support_email", "label": "Support email", "info": "Shown to customers. Leave empty to use your store email."}
  ],
  "blocks": [
    {"type": "@app"},
    {"type": "offer", "name": "Offer", "settings": [
      {"type": "text", "id": "label", "label": "Label", "default": "Buy 1"},
      {"type": "text", "id": "note", "label": "Note"},
      {"type": "range", "id": "quantity", "label": "Quantity", "min": 1, "max": 5, "step": 1, "default": 1},
      {"type": "paragraph", "content": "To show a bundle discount, create a real discount code in Shopify (Discounts) first, then enter the same code and percentage here. Both must be filled in or no discount is shown."},
      {"type": "text", "id": "discount_code", "label": "Discount code"},
      {"type": "range", "id": "discount_percent", "label": "Discount %", "min": 0, "max": 50, "step": 1, "default": 0},
      {"type": "text", "id": "badge", "label": "Badge", "info": "e.g. Most popular"}]},
    {"type": "review", "name": "Customer review", "settings": [
      {"type": "paragraph", "content": "Only add genuine reviews from real customers, with their permission."},
      reviews_data.STARS,
      {"type": "text", "id": "title", "label": "Title"},
      {"type": "textarea", "id": "review", "label": "Review"},
      {"type": "text", "id": "name", "label": "Customer name", "info": "e.g. Sarah, Melbourne"},
      {"type": "checkbox", "id": "verified", "label": "Verified buyer", "default": True},
      reviews_data.SOURCE_SETTING]},
    {"type": "faq", "name": "FAQ question", "settings": [
      {"type": "text", "id": "question", "label": "Question"},
      {"type": "textarea", "id": "answer", "label": "Answer"}]}
  ]
}

liquid = f'''{{%- comment -%}}
  LoftRest product page. Generated from src/loftrest-product.liquid by shopify/build_product.py.
  Edit offers, reviews, FAQ and trust settings in Online Store > Themes > Customize (Products > LoftRest).
{{%- endcomment -%}}
{twkit.FONT_LINKS}
{twkit.style_block(compiled_css)}

<div class="loftrest" id="loftrest-{{{{ section.id }}}}">
{body.strip()}
</div>

{{% schema %}}
{json.dumps(schema, indent=2, ensure_ascii=False)}
{{% endschema %}}
'''
(ROOT / 'sections' / 'loftrest-product.liquid').write_text(liquid)

blocks = {
  "offer_1": {"type": "offer", "settings": {"label": "1 × LoftRest™", "note": "For you", "quantity": 1}},
  "offer_2": {"type": "offer", "settings": {"label": "2 × LoftRest™", "note": "One for you, one for someone you love", "quantity": 2,
                                            "discount_code": "LOFTREST2PACK", "discount_percent": 10, "badge": "Save 10%"}},
}
blocks.update(reviews_data.blocks())
blocks.update({f"faq_{i+1}": {"type": "faq", "settings": {"question": q, "answer": a}} for i, (q, a) in enumerate(faqs)})
template = {
  "sections": {"main": {"type": "loftrest-product", "blocks": blocks, "block_order": list(blocks),
                        "settings": {"go_to_checkout": True, "shipping_note": "Free standard shipping in Australia", "returns_label": "30-day returns", "show_trial": False}}},
  "order": ["main"]
}
(ROOT / 'templates' / 'product.loftrest.json').write_text(json.dumps(template, indent=2, ensure_ascii=False) + '\n')
print(f'Wrote product section and template ({len(faqs)} FAQ questions).')
