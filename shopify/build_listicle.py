"""Build the Shopify listicle section from ../listicle.html.

    cd shopify && npm install && python3 build_listicle.py

Writes:
  shopify/sections/loftrest-listicle.liquid   (the listicle, as a theme section)
  shopify/templates/page.listicle.json        (page template that uses it)
"""
import json, pathlib, re

import twkit

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT.parent / 'listicle.html').read_text()
body = src[src.index('<!-- LISTICLE START -->') + len('<!-- LISTICLE START -->'):src.index('<!-- LISTICLE END -->')]

# ---- Optional parts ----
body = body.replace('<!--IF_SALE-->', '{% if on_sale %}').replace('<!--END_IF_SALE-->', '{% endif %}')  # no whitespace trimming: keeps spaces in button text
body = body.replace('<!--IF_TRIAL-->', '{%- if section.settings.show_trial -%}').replace('<!--END_IF_TRIAL-->', '{%- endif -%}')

# ---- Prices come from the product ----
LIQUID = {
    'price': '{% if variant %}{{ variant.price | money }}{% endif %}',
    'compare': '{{ variant.compare_at_price | money }}',
    'percent': '{{ variant.compare_at_price | minus: variant.price | times: 100.0 | divided_by: variant.compare_at_price | round }}%',
}
body, n = re.subn(r'<span([^>]*) data-lr="(price|compare|percent)">[^<]*</span>',
                  lambda m: f'<span{m.group(1)}>{LIQUID[m.group(2)]}</span>', body)
assert n >= 6, n

# ---- Images: three slots, each set in the theme editor. A slot with no image is hidden
#      (the middle one falls back to the product's main photo). Captions are editable too.
def image_liquid(slot, alt, cls, eager, fallback=''):
    cls = ' '.join(twkit.prefix_token(t) for t in cls.split())
    default = f' | default: {fallback}' if fallback else ''
    loading = "loading: 'eager', fetchpriority: 'high'" if eager else "loading: 'lazy'"
    return (f"{{%- assign img = section.settings.{slot}{default} -%}}"
            f"{{%- assign img_alt = img.alt | default: '{alt}' -%}}"
            f"{{{{ img | image_url: width: 1400 | image_tag: widths: '400, 600, 800, 1000, 1200, 1400', "
            f"sizes: '(min-width: 768px) 720px, 100vw', class: '{cls}', {loading}, alt: img_alt }}}}")

def figure_slot(m):
    slot, alt, cls = m.group(2), m.group(3), m.group(4)
    fallback = 'product.featured_image' if slot == 'image_middle' else ''
    check = f"section.settings.{slot}" + (f" != blank or {fallback}" if fallback else "")
    return (f"{m.group(1)}{{%- if {check} != blank -%}}\n"
            f"{m.group(1)}<figure class=\"{m.group(5)}\">\n"
            f"{m.group(1)}  {image_liquid(slot, alt, cls, slot == 'image_top', fallback)}\n"
            f"{m.group(1)}  {{%- if section.settings.caption_{slot.split('_')[1]} != blank -%}}"
            f"<figcaption class=\"{m.group(6)}\">{{{{ section.settings.caption_{slot.split('_')[1]} | escape }}}}</figcaption>{{%- endif -%}}\n"
            f"{m.group(1)}</figure>\n{m.group(1)}{{%- endif -%}}")

FIG = re.compile(r'( *)<figure class="([^"]*)">\s*<img data-lr="(image_top|image_middle)" src="[^"]*" alt="([^"]*)" class="([^"]*)"[^>]*>\s*<figcaption class="([^"]*)">(.*?)</figcaption>\s*</figure>', re.S)
captions = {}
def fig(m):
    indent, fig_cls, slot, alt, img_cls, cap_cls, cap = m.groups()
    captions[slot] = cap
    class M:  # shape expected by figure_slot
        def group(self, i): return [None, indent, slot, alt, img_cls, fig_cls, cap_cls][i]
    return figure_slot(M())
body, n = FIG.subn(fig, body)
assert n == 2, n
# Bottom slot: same look as the middle one, empty by default
mid = re.search(r'<figure class="([^"]*)">\s*<img data-lr="image_middle"[^>]*class="([^"]*)"[^>]*>\s*<figcaption class="([^"]*)">', src, re.S)
class B:
    def group(self, i): return [None, '      ', 'image_bottom', 'LoftRest 3-in-1 cervical traction pillow', mid.group(2), 'mt-14', mid.group(3)][i]
body = body.replace('<!--SHOPIFY_IMAGE_BOTTOM-->', figure_slot(B()).lstrip())
assert 'SHOPIFY_IMAGE' not in body

import html as _html
cap_text = {k: _html.unescape(re.sub(r'<[^>]+>', '', v)).strip() for k, v in captions.items()}

# ---- Buy buttons add the product to the cart and go to checkout ----
def buy(m):
    cls, text = m.group(1), m.group(2)
    return ('{%- if variant -%}'
            '<form action="{{ routes.cart_add_url }}" method="post" class="contents">'
            '<input type="hidden" name="id" value="{{ variant.id }}">'
            '<input type="hidden" name="quantity" value="1">'
            '<input type="hidden" name="return_to" value="/checkout">'
            f'<button type="submit" class="{cls}">{text}</button>'
            '</form>'
            '{%- else -%}'
            f'<a href="{{{{ routes.all_products_collection_url }}}}" class="{cls}">{text}</a>'
            '{%- endif -%}')
body, n = re.subn(r'<a data-lr="buy" href="[^"]*" class="([^"]*)">(.*?)</a>', buy, body, flags=re.S)
assert n == 3, n
assert 'data-lr' not in body and '<!--IF' not in body

body = twkit.inline_icons(body)
body = twkit.prefix_classes(body)
compiled_css = twkit.compile_css(body, src)

schema = {
  "name": "LoftRest listicle",
  "tag": "div",
  "class": "loftrest-section",
  "settings": [
    {"type": "product", "id": "product", "label": "Product", "info": "Prices, the discount and the Buy buttons come from this product."},
    {"type": "header", "content": "Images"},
    {"type": "image_picker", "id": "image_top", "label": "Image 1 (top)", "info": "Shown under the headline. Leave empty to hide it."},
    {"type": "text", "id": "caption_top", "label": "Image 1 caption", "default": cap_text['image_top']},
    {"type": "image_picker", "id": "image_middle", "label": "Image 2 (middle)", "info": "Shown in reason 3. Leave empty to use the product's main photo."},
    {"type": "text", "id": "caption_middle", "label": "Image 2 caption", "default": cap_text['image_middle']},
    {"type": "image_picker", "id": "image_bottom", "label": "Image 3 (before the offer)", "info": "Leave empty to hide it."},
    {"type": "text", "id": "caption_bottom", "label": "Image 3 caption"},
    {"type": "header", "content": "Offer"},
    {"type": "checkbox", "id": "show_trial", "label": "Show 30-night trial", "default": False,
     "info": "Only turn this on if you really offer a 30-night trial with a full refund."}
  ],
  "presets": [{"name": "LoftRest listicle"}]
}

liquid = f'''{{%- comment -%}}
  LoftRest listicle. Generated from listicle.html by shopify/build_listicle.py.
  Edit the product, top image and trial box in Online Store > Themes > Customize.
{{%- endcomment -%}}
{{%- assign product = section.settings.product -%}}
{{%- assign variant = product.selected_or_first_available_variant -%}}
{{%- assign on_sale = false -%}}
{{%- if variant.compare_at_price > variant.price -%}}{{%- assign on_sale = true -%}}{{%- endif -%}}

{twkit.FONT_LINKS}
{twkit.style_block(compiled_css)}

<div class="loftrest" id="loftrest-{{{{ section.id }}}}">
{body.strip()}
</div>

{{% schema %}}
{json.dumps(schema, indent=2)}
{{% endschema %}}
'''
(ROOT / 'sections' / 'loftrest-listicle.liquid').write_text(liquid)

template = {
  "sections": {"main": {"type": "loftrest-listicle",
    "settings": {"product": "loftrest-neck-traction-device",
                 "image_top": "shopify://shop_images/neck-pain-hd.webp", "caption_top": cap_text['image_top'],
                 "image_middle": "shopify://shop_images/loftrest-hero.webp", "caption_middle": cap_text['image_middle'],
                 "image_bottom": "shopify://shop_images/waking-up.webp", "caption_bottom": "The goal: waking up ready for the day, not stiff and sore.",
                 "show_trial": False}}},
  "order": ["main"]
}
(ROOT / 'templates' / 'page.listicle.json').write_text(json.dumps(template, indent=2, ensure_ascii=False) + '\n')
print('Wrote listicle section and template.')
