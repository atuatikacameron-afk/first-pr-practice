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

# ---- Hero image: section setting, else the product's main photo ----
hero = re.search(r'<img data-lr="hero" src="[^"]*" alt="([^"]*)" class="([^"]*)"[^>]*>', body)
assert hero
body = body.replace(hero.group(0), f"""{{%- assign hero = section.settings.image | default: product.featured_image -%}}
        {{%- if hero != blank -%}}
        {{%- assign hero_alt = hero.alt | default: '{hero.group(1)}' -%}}
        {{{{ hero | image_url: width: 1400 | image_tag: widths: '400, 600, 800, 1000, 1200, 1400', sizes: '(min-width: 768px) 720px, 100vw', class: '{' '.join(twkit.prefix_token(t) for t in hero.group(2).split())}', loading: 'eager', fetchpriority: 'high', alt: hero_alt }}}}
        {{%- endif -%}}""")

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
    {"type": "image_picker", "id": "image", "label": "Top image", "info": "Leave empty to use the product's main photo."},
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
    "settings": {"product": "loftrest-neck-traction-device", "image": "shopify://shop_images/loftrest-hero.webp", "show_trial": False}}},
  "order": ["main"]
}
(ROOT / 'templates' / 'page.listicle.json').write_text(json.dumps(template, indent=2, ensure_ascii=False) + '\n')
print('Wrote listicle section and template.')
