"""Build the new LoftRest homepage section from src/loftrest-home.liquid.

    cd shopify && npm install && python3 build_home.py

Writes:
  sections/loftrest-home.liquid   (the homepage, as a theme section)
  templates/index.json            (uses it as the store homepage)

Image slots are written in the source as
  <!--SLOT id="hero_image" label="Hero photo" wrap="absolute inset-0" sizes="100vw" eager-->
and become an image picker in the theme editor. Until an image is chosen, the theme
editor shows a dashed "Add image" box; shoppers only see a soft brand-coloured panel.
"""
import json, pathlib, re

import reviews_data, twkit

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT / 'src' / 'loftrest-home.liquid').read_text()
page_src = (ROOT.parent / 'index.html').read_text()   # brand colours / tailwind.config
PRODUCT = 'loftrest-neck-traction-device'

body = re.sub(r'^\{%- comment -%\}.*?\{%- endcomment -%\}\n', '', src, count=1, flags=re.S)

body, slots = twkit.expand_slots(body)
assert slots
body = twkit.prefix_classes(twkit.inline_icons(body))
css = twkit.compile_css(body, page_src)

schema = {
  "name": "LoftRest homepage", "tag": "div", "class": "loftrest-section",
  "settings": [
    {"type": "product", "id": "product", "label": "Product", "info": "Prices and Buy buttons come from this product."},
    {"type": "header", "content": "Hero"},
    {"type": "text", "id": "hero_badge", "label": "Badge", "default": "3-in-1 traction pillow"},
    {"type": "text", "id": "hero_heading", "label": "Heading", "default": "Your evening wind-down starts here"},
    {"type": "textarea", "id": "hero_text", "label": "Text", "default": "Gentle air traction, soothing warmth and massage to help you unwind, then contoured memory foam that supports your neck all night."},
    {"type": "header", "content": "2-pack offer"},
    {"type": "paragraph", "content": "Enter a real discount code from Shopify Discounts and its %. Both must be filled in or no discount is shown."},
    {"type": "text", "id": "bundle_code", "label": "Discount code"},
    {"type": "range", "id": "bundle_percent", "label": "Discount %", "min": 0, "max": 50, "step": 1, "default": 0},
    {"type": "header", "content": "Images"},
    *[{"type": "image_picker", "id": sid, "label": label} for sid, label in slots],
  ],
  "blocks": [
    {"type": "moment", "name": "Customer photo", "settings": [
      {"type": "paragraph", "content": "Only use photos you own or have permission to use."},
      {"type": "image_picker", "id": "image", "label": "Photo"},
      {"type": "text", "id": "caption", "label": "Caption"}]},
    {"type": "review", "name": "Customer review", "settings": [
      {"type": "paragraph", "content": "Only add genuine reviews from real customers, with their permission."},
      reviews_data.STARS,
      {"type": "textarea", "id": "review", "label": "Review"},
      {"type": "text", "id": "name", "label": "Customer name"},
      {"type": "checkbox", "id": "verified", "label": "Verified buyer", "default": True},
      reviews_data.SOURCE_SETTING,
      {"type": "image_picker", "id": "photo", "label": "Photo (optional)"}]},
    {"type": "faq", "name": "FAQ question", "settings": [
      {"type": "text", "id": "question", "label": "Question"},
      {"type": "textarea", "id": "answer", "label": "Answer"}]},
  ],
  "presets": [{"name": "LoftRest homepage"}],
}

liquid = f'''{{%- comment -%}}
  LoftRest homepage. Generated from src/loftrest-home.liquid by shopify/build_home.py.
  Add images, reviews and questions in Online Store > Themes > Customize.
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
(ROOT / 'sections' / 'loftrest-home.liquid').write_text(liquid)

# Homepage template: FAQ picked from the full FAQ page, images we already have pre-set
faq_page = json.loads((ROOT / 'templates' / 'page.faq.json').read_text())['sections']['main']
want = ["What is LoftRest™?", "How long and how often should I use it?", "Can I sleep on it all night?",
        "Is LoftRest™ a medical device?", "How much is shipping, and how long does it take?",
        "Can I return LoftRest™ if I change my mind?"]
by_q = {b['settings']['question']: b['settings']['answer'] for b in faq_page['blocks'].values()}
blocks = reviews_data.blocks()
blocks.update({f"faq_{i+1}": {"type": "faq", "settings": {"question": q, "answer": by_q[q]}} for i, q in enumerate(want)})
(ROOT / 'templates' / 'index.json').write_text(json.dumps({"sections": {"main": {
    "type": "loftrest-home", "blocks": blocks, "block_order": list(blocks),
    "settings": {"product": PRODUCT, "hero_badge": "3-in-1 traction pillow",
                 "hero_heading": "Your evening wind-down starts here",
                 "hero_text": "Gentle air traction, soothing warmth and massage to help you unwind, then contoured memory foam that supports your neck all night.",
                 "bundle_code": "LOFTREST2PACK", "bundle_percent": 10,
                 "hero_image": "shopify://shop_images/loftrest-hero.webp",
                 "product_image": "shopify://shop_images/Title_ad188c19-967a-4386-bb65-74cf28fb6639.png",
                 "offer1_image": "shopify://shop_images/u8512767942_edit_tis_kee_it_clean_and_studio_vibes_just_keep__1052460e-07fa-4269-8423-eaafffc4b717_3.png",
                 "offer2_image": "shopify://shop_images/u8512767942_edit_tis_kee_it_clean_and_studio_vibes_just_keep__4380a481-880e-476c-8e3f-df624be1e107_3.png",
                 "lifestyle_image": "shopify://shop_images/waking-up.webp",
                 "features_image": "shopify://shop_images/IMG_5504.jpg"}}},
    "order": ["main"]}, indent=2, ensure_ascii=False) + '\n')
print(f'Wrote homepage section ({len(slots)} image slots, {len(blocks)} blocks).')
