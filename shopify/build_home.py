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
PRODUCT = 'products-loftrest-3in1-massaging-orthopedic-cervical-pillowhttps-yourdomain-com-products-loftrest-3in1-massaging-orthopedic-cervical-pillow'

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
    {"type": "textarea", "id": "hero_text", "label": "Text", "default": "Gentle air traction, soothing warmth and massage to help you unwind, then a contoured pillow with a soft flannel cover to drift off on."},
    {"type": "header", "content": "2-pack offer"},
    {"type": "paragraph", "content": "Enter a real discount code from Shopify Discounts and its %. Both must be filled in or no discount is shown."},
    {"type": "text", "id": "bundle_code", "label": "Discount code"},
    {"type": "range", "id": "bundle_percent", "label": "Discount %", "min": 0, "max": 50, "step": 1, "default": 0},
    {"type": "text", "id": "bundle_badge", "label": "2-pack badge", "info": "Leave empty to show \"Save X%\". Only promise what's true (international shipping isn't free)."},
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
# Quiz app sections the owner added in Customize (RevenueHunt). Kept so a rebuild doesn't remove them.
def _quiz(block_id, block_type, settings, disabled=False):
    b = {"type": f"shopify://apps/rh-product-quiz-builder/blocks/{block_type}/672f3d48-fd3b-4227-8778-c6e58c4f8a98", "settings": settings}
    if disabled: b["disabled"] = True
    return {"type": "_blocks", "blocks": {block_id: b}, "block_order": [block_id], "settings": {
        "content_direction": "column", "vertical_on_mobile": True, "horizontal_alignment": "flex-start", "vertical_alignment": "center",
        "align_baseline": False, "horizontal_alignment_flex_direction_column": "flex-start", "vertical_alignment_flex_direction_column": "center",
        "gap": 12, "section_width": "page-width", "section_height": "", "section_height_custom": 50, "background_media": "none",
        "background_color": "", "video_position": "cover", "background_image_position": "cover", "toggle_overlay": False,
        "overlay_color": "#00000026", "overlay_style": "solid", "gradient_direction": "to top", "border": "none", "border_width": 1,
        "border_opacity": 100, "border_color": "", "border_radius": 0, "padding-block-start": 0, "padding-block-end": 0}}
_inline = {"quiz_height": 500, "quiz_height_unit": "px", "quiz_fixed_height": False, "quiz_full_width": False,
           "quiz_retake_autoscroll": "disabled", "quiz_question_autoscroll": "disabled", "quiz_id": ""}
QUIZ_SECTIONS = {
  "1791865482cb1476cb": _quiz("revenuehunt_product_quiz_maker_v2_inline_quiz_dYwTRp", "v2-inline-quiz", _inline),
  "179186557683b020a2": _quiz("revenuehunt_product_quiz_maker_v2_automatic_popup_block_ne66a4", "v2-automatic-popup-block",
      {"popup_timeout": 20, "quiz_width": "100", "quiz_height": "100", "quiz_z_index": 100, "popup_close_color": "#777777", "quiz_exit_intent": False, "quiz_id": ""}),
  "1791865646e2665dbe": _quiz("revenuehunt_product_quiz_maker_v2_inline_quiz_9fQ73U", "v2-inline-quiz", _inline, disabled=True),
  "1791865728cf917bc4": _quiz("revenuehunt_product_quiz_maker_v2_inline_quiz_b7xPJx", "v2-inline-quiz", _inline, disabled=True),
}
(ROOT / 'templates' / 'index.json').write_text(json.dumps({"sections": {"main": {
    "type": "loftrest-home", "blocks": blocks, "block_order": list(blocks),
    "settings": {"product": PRODUCT, "hero_badge": "3-in-1 traction pillow",
                 "hero_heading": "Your evening wind-down starts here",
                 "hero_text": "Gentle air traction, soothing warmth and massage to help you unwind, then a contoured pillow with a soft flannel cover to drift off on.",
                 "bundle_code": "LOFTREST2PACK", "bundle_percent": 10, "bundle_badge": "Save 10% + Free AU shipping",
                 "hero_image": "shopify://shop_images/loftrest-hero.webp",
                 "product_image": "shopify://shop_images/Title_ad188c19-967a-4386-bb65-74cf28fb6639.png",
                 "offer1_image": "shopify://shop_images/u8512767942_edit_tis_kee_it_clean_and_studio_vibes_just_keep__1052460e-07fa-4269-8423-eaafffc4b717_3.png",
                 "offer2_image": "shopify://shop_images/u8512767942_edit_tis_kee_it_clean_and_studio_vibes_just_keep__4380a481-880e-476c-8e3f-df624be1e107_3.png",
                 "lifestyle_image": "shopify://shop_images/waking-up.webp",
                 "features_image": "shopify://shop_images/IMG_5504.jpg"}},
    **QUIZ_SECTIONS}, "order": ["main", *QUIZ_SECTIONS]}, indent=2, ensure_ascii=False) + '\n')
print(f'Wrote homepage section ({len(slots)} image slots, {len(blocks)} blocks).')
