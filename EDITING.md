# Editing the LoftRest page

The whole page is one file, `index.html`. There's no build step or special software. Change the file, save it, and the page updates.

## How to edit

- **On GitHub (easiest):** open `index.html` on GitHub, click the pencil icon, make your change, then click **Commit changes**.
- **On your computer:** open `index.html` in any text editor (VS Code, Notepad, TextEdit in plain-text mode). Double-click the file to preview it in your browser.
- **Ask Claude:** describe the change you want, e.g. "change the price to $99" or "add a question about returns".

## Price, sale and checkout link

These live in one place near the top of `index.html`, in the block marked **EASY SETTINGS**:

```js
window.LOFTREST = {
  price: 119.00,            // current price
  oldPrice: 169.00,         // crossed-out price (set to 0 to hide it)
  currencySymbol: '$',
  currencyCode: 'USD',
  saleName: 'Spring Sleep Sale',
  checkoutUrl: '',          // paste your Shopify/Stripe checkout link between the quotes
  maxQuantity: 10
};
```

When you change a setting here, the page updates everywhere it's used:

| Setting | What it updates |
| --- | --- |
| `price` | Order box price, the running total, and the price Google sees |
| `oldPrice` | Crossed-out price, "SAVE $50" badge, "Save $50" in the top bar, "Get 30% Off" button. Set to `0` to end the sale and hide all of these. |
| `saleName` | The top bar, the order box and the shipping answer in the FAQ |
| `checkoutUrl` | Where the **Buy Now** button goes |

## Where everything else is

Each section in `index.html` starts with a label in capitals, like `<!-- FAQ -->`. Search the file for these:

| Label | What's in it |
| --- | --- |
| `ANNOUNCEMENT BAR` | The dark strip at the very top |
| `NAVIGATION` | Logo and menu links |
| `HERO SECTION` | Headline, intro text, main button, product image area |
| `HOW IT WORKS` | The three therapy cards |
| `NECK PAIN & SLEEP` | How neck pain and sleep affect each other |
| `BENEFITS` | The six benefit cards |
| `15-MINUTE ROUTINE` | The three steps |
| `REVIEWS` | Customer review cards |
| `CHECKOUT & ORDER SECTION` | Price box and Buy Now button |
| `FAQ` | Questions and answers |
| `FOOTER` | Bottom of the page |

To change any wording, find it in the file and type over it. Leave the parts inside `< >` alone.

## Common changes

**Add a real review.** In the `REVIEWS` section, replace `[Paste a real customer review here]` and `[Customer first name, city]`. Delete any review card you don't have a real review for: each card runs from `<figure` to `</figure>`. Use only genuine reviews from real customers, with their permission. Fake reviews are illegal in the US, UK and EU.

**Add or change a question.** In the `FAQ` section, copy one whole block from `<details` to `</details>`, paste it below, and change the question (inside `<h3>`) and the answer (inside `<p>`). Google reads the questions straight from the page, so there's nothing else to update.

**Add a product photo.** Upload the image next to `index.html`, e.g. `loftrest.jpg`. Then in the `HERO SECTION`, replace the placeholder box (the `<div class="relative aspect-square ...">` block) with:

```html
<img src="loftrest.jpg" alt="LoftRest neck traction device" class="w-full rounded-3xl shadow-2xl">
```

**Change the colors.** Near the top of the file, `tailwind.config` lists the brand colors (`navy`, `blue`, `heat` and so on). Change a color code, e.g. `'#0284C7'`, and every place that uses it updates.

**Change the page title Google shows.** Edit the `<title>` and `<meta name="description">` lines near the top.

## Shopify version

The page is also packaged for Shopify in the `shopify/` folder. There, price and sale come from your Shopify product, and reviews and questions can be edited in Shopify's theme editor. See [shopify/README.md](shopify/README.md) for how to install and edit it.
