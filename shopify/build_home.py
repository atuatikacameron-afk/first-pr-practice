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

import twkit

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT / 'src' / 'loftrest-home.liquid').read_text()
page_src = (ROOT.parent / 'index.html').read_text()   # brand colours / tailwind.config
PRODUCT = 'loftrest-neck-traction-device'

body = re.sub(r'^\{%- comment -%\}.*?\{%- endcomment -%\}\n', '', src, count=1, flags=re.S)

slots = []
def slot(m):
    attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    eager = ' eager' in m.group(1)
    sid, label = attrs['id'], attrs['label']
    slots.append((sid, label))
    loading = "loading: 'eager', fetchpriority: 'high'" if eager else "loading: 'lazy'"
    return (f'<div class="{attrs.get("wrap", "")}">'
            f"{{%- if section.settings.{sid} != blank -%}}"
            f"{{%- assign img_alt = section.settings.{sid}.alt | default: 'LoftRest cervical traction pillow' -%}}"
            f"{{{{ section.settings.{sid} | image_url: width: 1600 | image_tag: widths: '400, 600, 800, 1000, 1200, 1600', "
            f"sizes: '{attrs.get('sizes', '100vw')}', class: 'lr-w-full lr-h-full lr-object-cover', {loading}, alt: img_alt }}}}"
            f"{{%- else -%}}"
            f'<div class="w-full h-full flex flex-col items-center justify-center gap-2 p-4 text-center bg-gradient-to-br from-brand-lightBlue to-sky-100 text-brand-royal">'
            f"{{%- if request.design_mode -%}}"
            f'<div class="absolute inset-3 rounded-2xl border-2 border-dashed border-sky-300"></div>'
            f'<i data-lucide="image-plus" class="w-8 h-8"></i><span class="text-xs font-bold uppercase tracking-wide">Add image: {label}</span>'
            f"{{%- else -%}}<i data-lucide=\"waves\" class=\"w-10 h-10 opacity-40\"></i>{{%- endif -%}}"
            f"</div>{{%- endif -%}}</div>")

body = re.sub(r'<!--SLOT (.*?)-->', slot, body)
assert slots and '<!--SLOT' not in body
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
      {"type": "range", "id": "stars", "label": "Stars", "min": 1, "max": 5, "step": 1, "default": 5},
      {"type": "textarea", "id": "review", "label": "Review"},
      {"type": "text", "id": "name", "label": "Customer name"},
      {"type": "checkbox", "id": "verified", "label": "Verified buyer", "default": True},
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
blocks = {f"faq_{i+1}": {"type": "faq", "settings": {"question": q, "answer": by_q[q]}} for i, q in enumerate(want)}
(ROOT / 'templates' / 'index.json').write_text(json.dumps({"sections": {"main": {
    "type": "loftrest-home", "blocks": blocks, "block_order": list(blocks),
    "settings": {"product": PRODUCT, "bundle_code": "LOFTREST2PACK", "bundle_percent": 10,
                 "hero_image": "shopify://shop_images/loftrest-hero.webp",
                 "lifestyle_image": "shopify://shop_images/waking-up.webp"}}},
    "order": ["main"]}, indent=2, ensure_ascii=False) + '\n')
print(f'Wrote homepage section ({len(slots)} image slots, {len(blocks)} FAQ questions).')
