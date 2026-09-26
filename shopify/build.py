"""Build the Shopify theme files from ../index.html.

    python3 shopify/build.py

Writes:
  shopify/sections/loftrest-landing.liquid   (the page, as a theme section)
  shopify/templates/page.loftrest.json       (page template with the FAQ pre-filled)

Re-run this after changing index.html, then re-upload both files to your theme.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT.parent / 'index.html').read_text()

def between(start, end):
    i = src.index(start); j = src.index(end, i)
    return src[i:j]

# Page body from the hero to the footer. The store's own theme supplies the header,
# announcement bar and footer, so the page's versions are left out.
body = between('  <!-- HERO SECTION -->', '  <!-- FOOTER -->')

# ---- FAQ: pre-fill template blocks from the page, render from blocks ----
faq_html = between('  <!-- FAQ -->', '  <!-- FOOTER -->')
faqs = [(html.unescape(q.strip()), html.unescape(a.strip())) for q, a in
        re.findall(r'<h3>(.*?)</h3>.*?<p class="mt-3[^"]*">(.*?)</p>', faq_html, re.S)]
assert len(faqs) >= 5, faqs
faq_liquid = re.sub(r'      <div class="space-y-3">.*?\n      </div>\n    </div>\n  </section>',
lambda m: '''      <div class="space-y-3">
        {%- for block in section.blocks -%}
          {%- if block.type == 'faq' -%}
        <details class="group rounded-xl border border-slate-200 p-5" {{ block.shopify_attributes }}>
          <summary class="flex items-center justify-between gap-4 cursor-pointer font-bold text-brand-navy list-none">
            <h3>{{ block.settings.question | escape }}</h3>
            <i data-lucide="chevron-down" class="w-5 h-5 shrink-0 transition-transform group-open:rotate-180"></i>
          </summary>
          <p class="mt-3 text-slate-600 leading-relaxed">{{ block.settings.answer | escape }}</p>
        </details>
          {%- endif -%}
        {%- endfor -%}
      </div>
    </div>
  </section>
''', faq_html, count=1, flags=re.S)
body = body.replace(faq_html, faq_liquid)

# ---- Reviews: one card per review block; section hidden until a review is added ----
rev_html = between('  <!-- REVIEWS', '  <!-- CHECKOUT & ORDER SECTION -->')
rev_liquid = re.sub(r'      <div class="grid[^"]*">.*?\n      </div>\n    </div>\n  </section>',
lambda m: '''      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {%- for block in section.blocks -%}
          {%- if block.type == 'review' -%}
        <figure class="bg-white rounded-2xl border border-slate-200 p-6 flex flex-col" {{ block.shopify_attributes }}>
          {%- if block.settings.topic != blank -%}<p class="text-xs font-bold uppercase tracking-wide text-brand-blue">{{ block.settings.topic | escape }}</p>{%- endif -%}
          {%- if block.settings.question != blank -%}<h3 class="mt-1 font-bold text-brand-navy">{{ block.settings.question | escape }}</h3>{%- endif -%}
          <div class="mt-3 flex text-amber-400" aria-label="{{ block.settings.stars }} out of 5 stars">
            {%- for i in (1..block.settings.stars) -%}<i data-lucide="star" class="w-4 h-4 fill-current"></i>{%- endfor -%}
          </div>
          <blockquote class="mt-3 text-slate-600 flex-1">{{ block.settings.review | escape }}</blockquote>
          <figcaption class="mt-4 text-sm font-semibold text-slate-800">{{ block.settings.name | escape }}{%- if block.settings.verified -%} <span class="font-normal text-slate-500">· Verified buyer</span>{%- endif -%}</figcaption>
        </figure>
          {%- endif -%}
        {%- endfor -%}
      </div>
    </div>
  </section>
''', rev_html, count=1, flags=re.S)
rev_liquid = re.sub(r'  <!-- REVIEWS.*?-->\n', '', rev_liquid, count=1, flags=re.S)
rev_liquid = ("  {%- assign review_count = section.blocks | where: 'type', 'review' | size -%}\n"
              "  {%- if review_count > 0 -%}\n" + rev_liquid.rstrip() + "\n  {%- endif -%}\n\n")
body = body.replace(rev_html, rev_liquid)

# ---- Order box: real Shopify product, price and cart ----
order_html = between('  <!-- CHECKOUT & ORDER SECTION -->', '  <!-- FAQ -->')
order = order_html
for a, b in [
    ('<div class="mt-6 flex flex-wrap items-baseline gap-4">', '{%- if variant -%}\n          <div class="mt-6 flex flex-wrap items-baseline gap-4">'),
    ('SAVE <span data-savings>$50</span></span>\n          </div>', 'SAVE <span data-savings>$50</span></span>\n          </div>\n          {%- endif -%}'),
    ('<span class="text-4xl font-extrabold" data-price>$119.00</span>', '<span class="text-4xl font-extrabold">{{ variant.price | money }}</span>'),
    ('<span class="text-xl text-slate-500 line-through" data-old-price>$169.00</span>\n            <span class="text-xs font-bold bg-brand-heat text-white px-2 py-1 rounded" data-savings-badge>SAVE <span data-savings>$50</span></span>',
     '{%- if on_sale -%}\n            <span class="text-xl text-slate-500 line-through">{{ variant.compare_at_price | money }}</span>\n            <span class="text-xs font-bold bg-brand-heat text-white px-2 py-1 rounded">SAVE {{ variant.compare_at_price | minus: variant.price | money_without_trailing_zeros }}</span>\n            {%- endif -%}'),
    ('<li class="flex items-center gap-3"><i data-lucide="check-circle-2" class="w-5 h-5 text-brand-emerald"></i> <span data-sale-name>Spring Sleep Sale</span> price</li>',
     '{%- if on_sale and section.settings.sale_name != blank -%}<li class="flex items-center gap-3"><i data-lucide="check-circle-2" class="w-5 h-5 text-brand-emerald"></i> {{ section.settings.sale_name | escape }} price</li>{%- endif -%}'),
    ('<div class="bg-white/5 rounded-2xl border border-white/10 p-6 space-y-5">',
     '{%- if variant -%}\n        <form action="{{ routes.cart_add_url }}" method="post" class="bg-white/5 rounded-2xl border border-white/10 p-6 space-y-5">\n          <input type="hidden" name="id" value="{{ variant.id }}">\n          <input type="hidden" name="return_to" value="{% if section.settings.go_to_checkout %}/checkout{% else %}{{ routes.cart_url }}{% endif %}">'),
    ('<input id="qty" type="number"', '<input id="qty" name="quantity" type="number"'),
    ('<span id="total" class="font-extrabold">$119.00</span>', '<span id="total" class="font-extrabold">{{ variant.price | money }}</span>'),
    ('          <!-- The checkout link is set in EASY SETTINGS at the top of this file (checkoutUrl). -->\n          <a href="#" id="buy" class="block w-full', '          <button type="submit" id="buy" {% unless variant.available %}disabled{% endunless %} class="block w-full disabled:opacity-50'),
    ('            Buy Now\n          </a>', '            {% if variant.available %}Buy Now{% else %}Sold out{% endif %}\n          </button>'),
    ('            <i data-lucide="lock" class="w-3.5 h-3.5"></i> Secure checkout\n          </p>\n        </div>',
     '            <i data-lucide="lock" class="w-3.5 h-3.5"></i> Secure checkout\n          </p>\n        </form>\n        {%- else -%}\n        <div class="bg-white/5 rounded-2xl border border-white/10 p-6 text-slate-300">Choose your LoftRest product in the theme editor: <strong>Customize</strong> &rsaquo; this page &rsaquo; <strong>LoftRest landing page</strong> &rsaquo; <strong>Product</strong>.</div>\n        {%- endif -%}'),
]:
    assert order.count(a) == 1, a
    order = order.replace(a, b)
body = body.replace(order_html, order)

# ---- Hero sale wording follows the product's compare-at price ----
for a, b in [
    ('<span data-no-sale-text="Order LoftRest Today">Get <span data-percent-off>30%</span> Off LoftRest Today</span>',
     '{%- if on_sale -%}Get {{ variant.compare_at_price | minus: variant.price | times: 100.0 | divided_by: variant.compare_at_price | round }}% Off LoftRest Today{%- else -%}Order LoftRest Today{%- endif -%}'),
]:
    assert body.count(a) == 1, a
    body = body.replace(a, b)

# ---- Scripts: icons, quantity total, FAQ schema (Shopify outputs its own product data) ----
script = '''<script>
  (function () {
    var root = document.getElementById('loftrest-{{ section.id }}');
    function icons() { if (window.lucide) lucide.createIcons(); }
    if (window.lucide) icons(); else document.addEventListener('DOMContentLoaded', icons);

    var qty = root.querySelector('#qty');
    if (qty) {
      var price = {{ variant.price | default: 0 | json }};
      var format = {{ shop.money_format | strip_html | json }};
      var total = root.querySelector('#total');
      var money = function (cents) {
        var amount = (cents / 100).toFixed(2);
        return format.replace(/\\{\\{\\s*(\\w+)\\s*\\}\\}/, function (m, key) {
          if (key.indexOf('no_decimals') > -1) amount = Math.round(cents / 100).toString();
          if (key.indexOf('comma') > -1) amount = amount.replace('.', ',');
          return amount;
        });
      };
      var clamp = function (n) { return Math.min(10, Math.max(1, isFinite(n) ? n : 1)); };
      var render = function () { qty.value = clamp(parseInt(qty.value, 10)); total.textContent = money(price * qty.value); };
      root.querySelector('#qty-minus').addEventListener('click', function () { qty.value = parseInt(qty.value, 10) - 1; render(); });
      root.querySelector('#qty-plus').addEventListener('click', function () { qty.value = parseInt(qty.value, 10) + 1; render(); });
      qty.addEventListener('change', render);
    }
  })();
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {%- assign faq_blocks = section.blocks | where: 'type', 'faq' -%}
    {%- for block in faq_blocks -%}
    { "@type": "Question", "name": {{ block.settings.question | json }}, "acceptedAnswer": { "@type": "Answer", "text": {{ block.settings.answer | json }} } }{% unless forloop.last %},{% endunless %}
    {%- endfor -%}
  ]
}
</script>'''

tw = re.search(r'    tailwind.config = (\{.*?\n    \})\n', src, re.S).group(1)
tw = tw.replace('{\n      theme:', "{\n      important: '.loftrest',\n      corePlugins: { preflight: false },\n      theme:", 1)

schema = {
  "name": "LoftRest landing page",
  "tag": "div",
  "class": "loftrest-section",
  "settings": [
    {"type": "product", "id": "product", "label": "Product", "info": "Price, sale price and the Buy Now button come from this product. Set a 'Compare-at price' on the product to show the sale."},
    {"type": "text", "id": "sale_name", "label": "Sale name", "default": "Spring Sleep Sale"},
    {"type": "checkbox", "id": "go_to_checkout", "label": "Buy Now goes straight to checkout", "default": True, "info": "Turn off to send buyers to the cart instead."}
  ],
  "blocks": [
    {"type": "faq", "name": "FAQ question", "settings": [
      {"type": "text", "id": "question", "label": "Question"},
      {"type": "textarea", "id": "answer", "label": "Answer"}]},
    {"type": "review", "name": "Customer review", "settings": [
      {"type": "paragraph", "content": "Only add genuine reviews from real customers, with their permission."},
      {"type": "text", "id": "topic", "label": "Topic", "info": "e.g. Sleep, Neck pain, Tech neck"},
      {"type": "text", "id": "question", "label": "Heading", "info": "e.g. Did it help you sleep better?"},
      {"type": "range", "id": "stars", "label": "Stars", "min": 1, "max": 5, "step": 1, "default": 5},
      {"type": "textarea", "id": "review", "label": "Review"},
      {"type": "text", "id": "name", "label": "Customer name", "info": "e.g. Sarah, Denver"},
      {"type": "checkbox", "id": "verified", "label": "Verified buyer", "default": True}]}
  ],
  "presets": [{"name": "LoftRest landing page"}]
}

liquid = f'''{{%- comment -%}}
  LoftRest landing page. Generated from index.html by shopify/build.py.
  Edit reviews, FAQ, product and sale name in Online Store > Themes > Customize.
{{%- endcomment -%}}
{{%- assign product = section.settings.product -%}}
{{%- assign variant = product.selected_or_first_available_variant -%}}
{{%- assign on_sale = false -%}}
{{%- if variant.compare_at_price > variant.price -%}}{{%- assign on_sale = true -%}}{{%- endif -%}}

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<script>
  tailwind.config = {tw};
</script>
<style>
  /* Minimal reset scoped to this page so the rest of your theme is untouched */
  .loftrest {{ font-family: 'Inter', -apple-system, sans-serif; color: #1e293b; background: #F8FAFC; -webkit-font-smoothing: antialiased; line-height: 1.5; }}
  .loftrest *, .loftrest *::before, .loftrest *::after {{ box-sizing: border-box; border-width: 0; border-style: solid; border-color: #e5e7eb; }}
  .loftrest h1, .loftrest h2, .loftrest h3, .loftrest p, .loftrest figure, .loftrest blockquote, .loftrest ol, .loftrest ul {{ margin: 0; padding: 0; }}
  .loftrest h1, .loftrest h2, .loftrest h3 {{ font-family: inherit; font-size: inherit; font-weight: inherit; letter-spacing: inherit; color: inherit; line-height: 1.2; }}
  .loftrest ol, .loftrest ul {{ list-style: none; }}
  .loftrest a {{ color: inherit; text-decoration: none; }}
  .loftrest button, .loftrest input {{ font: inherit; color: inherit; margin: 0; background: transparent; }}
  .loftrest button {{ cursor: pointer; }}
  .loftrest svg {{ display: block; }}
  .loftrest summary::-webkit-details-marker {{ display: none; }}
</style>

<div class="loftrest" id="loftrest-{{{{ section.id }}}}">
{body.rstrip()}
</div>

{script}

{{% schema %}}
{json.dumps(schema, indent=2)}
{{% endschema %}}
'''
(ROOT / 'sections' / 'loftrest-landing.liquid').write_text(liquid)

template = {
  "sections": {"main": {"type": "loftrest-landing",
    "blocks": {f"faq_{i+1}": {"type": "faq", "settings": {"question": q, "answer": a}} for i, (q, a) in enumerate(faqs)},
    "block_order": [f"faq_{i+1}" for i in range(len(faqs))],
    "settings": {"product": "loftrest-neck-traction-device", "sale_name": "Spring Sleep Sale", "go_to_checkout": True}}},
  "order": ["main"]
}
(ROOT / 'templates' / 'page.loftrest.json').write_text(json.dumps(template, indent=2, ensure_ascii=False) + '\n')
print(f'Wrote section and template ({len(faqs)} FAQ questions).')
