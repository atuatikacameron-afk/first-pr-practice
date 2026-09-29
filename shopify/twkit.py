"""Shared helpers for turning a Tailwind page into a self-contained Shopify section.

Used by build.py (homepage/landing page) and build_listicle.py (listicle).
"""
import json, pathlib, re, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent
ICONS = ROOT / 'node_modules' / 'lucide-static' / 'icons'
PREFIX = 'lr-'

FONT_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">"""

RESET_CSS = """  /* Minimal reset scoped to this page so the rest of your theme is untouched */
  .loftrest { font-family: 'Inter', -apple-system, sans-serif; color: #1e293b; background: #F8FAFC; -webkit-font-smoothing: antialiased; line-height: 1.5; }
  .loftrest *, .loftrest *::before, .loftrest *::after { box-sizing: border-box; border-width: 0; border-style: solid; border-color: #e5e7eb; }
  .loftrest h1, .loftrest h2, .loftrest h3, .loftrest p, .loftrest figure, .loftrest blockquote, .loftrest ol, .loftrest ul { margin: 0; padding: 0; }
  .loftrest h1, .loftrest h2, .loftrest h3 { font-family: inherit; font-size: inherit; font-weight: inherit; letter-spacing: inherit; color: inherit; line-height: 1.2; }
  .loftrest ol, .loftrest ul { list-style: none; }
  .loftrest a { color: inherit; text-decoration: none; }
  .loftrest button, .loftrest input { font: inherit; color: inherit; margin: 0; background: transparent; }
  .loftrest button { cursor: pointer; }
  .loftrest svg { display: block; }
  .loftrest summary { padding: 0; }
  .loftrest summary::-webkit-details-marker { display: none; }"""


def require_tools():
    if not ICONS.is_dir():
        raise SystemExit('Run "npm install" in the shopify folder first.')


def inline_icons(body):
    """Replace <i data-lucide="name" class="..."></i> with the Lucide SVG."""
    require_tools()

    def icon_svg(m):
        name, cls = m.group(1), m.group(2)
        svg = (ICONS / f'{name}.svg').read_text()
        svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
        svg = re.sub(r'\s+', ' ', svg).replace('> <', '><').strip()
        return svg.replace(f'class="lucide lucide-{name}"', f'class="{cls}" aria-hidden="true" focusable="false"', 1)

    body = re.sub(r'<i data-lucide="([a-z0-9-]+)" class="([^"]*)"></i>', icon_svg, body)
    assert 'data-lucide' not in body
    return body


def prefix_token(tok):
    if '{' in tok or tok.startswith('loftrest'):
        return tok
    parts, depth, cur = [], 0, ''
    for ch in tok:
        depth += ch == '['
        depth -= ch == ']'
        if ch == ':' and depth == 0:
            parts.append(cur); cur = ''
        else:
            cur += ch
    util = cur
    if util.startswith('['):
        pass  # arbitrary properties like [appearance:textfield] can't take a prefix
    elif util.startswith('-'):
        util = '-' + PREFIX + util[1:]
    else:
        util = PREFIX + util
    return ':'.join(parts + [util])


def prefix_classes(body):
    """Prefix every Tailwind class with "lr-" so none can clash with the theme's own
    classes (Horizon, for example, has its own .flex and .grid)."""
    return re.sub(r'class="([^"]*)"', lambda m: 'class="' + ' '.join(prefix_token(t) for t in m.group(1).split()) + '"', body)


def compile_css(body, page_src):
    """Compile only the Tailwind CSS that body uses, with the tailwind.config from page_src."""
    require_tools()
    tw = re.search(r'    tailwind.config = (\{.*?\n    \})\n', page_src, re.S).group(1)
    tw = tw.replace('{\n      theme:', "{\n      prefix: 'lr-',\n      important: '.loftrest',\n      corePlugins: { preflight: false },\n      theme:", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / 'page.html').write_text(body)
        (tmp / 'in.css').write_text('@tailwind base;\n@tailwind utilities;\n')
        cfg = tw.rstrip()[:-1].rstrip() + f",\n      content: [{json.dumps(str(tmp / 'page.html'))}]\n    }}"
        (tmp / 'tailwind.config.js').write_text('module.exports = ' + cfg + ';\n')
        css = subprocess.run(
            [str(ROOT / 'node_modules' / '.bin' / 'tailwindcss'), '-c', str(tmp / 'tailwind.config.js'), '-i', str(tmp / 'in.css'), '--minify'],
            check=True, capture_output=True, text=True).stdout.strip()
    # With preflight off, "base" is only Tailwind's default --tw-* variables (needed for
    # shadows, rings and transforms). Scope them to this page instead of the whole store.
    css = css.replace('*,:after,:before{', '.loftrest,.loftrest *,.loftrest :after,.loftrest :before{', 1)
    css = css.replace('::backdrop{', '.loftrest ::backdrop{', 1)
    assert not re.search(r'(^|})(\*|::backdrop|html|body)[,{]', css), 'unscoped base rule left in CSS'
    return css


def style_block(compiled_css):
    return '<style>\n' + RESET_CSS + '\n  /* Page styles (Tailwind, compiled by build.py) */\n  ' + compiled_css + '\n</style>'


def expand_slots(body):
    """Turn <!--SLOT id="x" label="..." wrap="..." sizes="..." [eager]--> markers into an
    image picker slot: the chosen image, or an "Add image" box in the theme editor and a
    soft brand panel for shoppers. Returns (body, [(id, label), ...])."""
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
    assert '<!--SLOT' not in body
    return body, slots
