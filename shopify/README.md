# LoftRest page on Shopify

These two files add the LoftRest landing page to your Shopify store. Your store's own header, footer and menu stay the same.

| File | What it is |
| --- | --- |
| `sections/loftrest-landing.liquid` | The page itself, as a theme section |
| `templates/page.loftrest.json` | A page template that uses it, with the FAQ questions already filled in |
| `templates/index.json` | The same page as your store's **homepage** |

## Install (about 10 minutes)

**1. Create the product.** In Shopify admin go to **Products → Add product**:
- Title: `LoftRest™ 3-in-1 Cervical Therapy Device`
- Price: `119.00`
- Compare-at price: `169.00`. This turns on the "SAVE $50" badge and "Get 30% Off" button. Leave it blank for no sale.
- Add your product photos, then **Save**.

**2. Make a backup of your theme.** Go to **Online Store → Themes**. On your current theme, click **⋯ → Duplicate**. If anything goes wrong, you can switch back to the copy.

**3. Add the two files.** On your current theme click **⋯ → Edit code**, then:
- Under **Sections**, click **Add a new section**, name it `loftrest-landing`, delete everything in it, paste in the whole of `sections/loftrest-landing.liquid`, and **Save**.
- Under **Templates**, click **Add a new template**, choose **page**, choose **JSON**, name it `loftrest`, delete everything in it, paste in the whole of `templates/page.loftrest.json`, and **Save**.

**4. Create the page.** Go to **Online Store → Pages → Add page**:
- Title: `LoftRest`. This becomes the address, e.g. `yourstore.com/pages/loftrest`.
- Leave the content empty.
- On the right, under **Theme template**, choose `loftrest`.
- Set **Visibility** to **Hidden** while you finish it, then **Save**.

**5. Connect the product.** Go to **Online Store → Themes → Customize**. At the top, switch to **Pages → LoftRest**. Click **LoftRest landing page** on the left and pick your product under **Product**. **Save**.

**6. Check it, then go live.** Preview the page. Click **Buy Now** to test that checkout opens. When you're happy, go back to the page and set **Visibility** to **Visible**.

## Using it as the homepage

To make the LoftRest page your homepage, replace your theme's `templates/index.json` with the one here: **Edit code → Templates → index.json**, delete everything, paste in `templates/index.json`, **Save**. To edit the homepage version, go to **Customize** and pick **Home page** at the top. The homepage and the `/pages/loftrest` page have separate review and FAQ blocks, so if you use the homepage you can leave the page hidden.

## Editing on Shopify

Most changes can be made in **Online Store → Themes → Customize → Pages → LoftRest → LoftRest landing page**. You don't need to touch any code.

| To change | Do this |
| --- | --- |
| Price or sale | Edit the product's **Price** and **Compare-at price**. The page, badge, "% off" button and total all update. |
| End the sale | Clear the product's **Compare-at price**. All sale wording disappears. |
| Sale name | **Sale name** field in the section settings |
| Buy Now goes to cart or checkout | **Buy Now goes straight to checkout** checkbox |
| Add a review | **Add block → Customer review**. Only use genuine reviews from real customers, with their permission. The reviews section stays hidden until you add one. |
| Add, edit or reorder a question | Each **FAQ question** block is one question. Drag to reorder. Google's FAQ data updates automatically. |

Other wording, like headlines and benefits, is in the section file: **Edit code → Sections → loftrest-landing.liquid**. Find the text and type over it. Don't change the `class="..."` parts. The page only includes the styles it already uses, so new style classes won't work without a rebuild.

## If you edit `index.html` instead

`index.html` in this repo is the standalone version of the page. After changing it, rebuild the Shopify files (you need [Node.js](https://nodejs.org) and Python installed):

```
cd shopify
npm install        # first time only
python3 build.py
```

The build turns the page's styles and icons into plain CSS and SVG inside the section, so nothing loads from outside at runtime. It also adds an `lr-` prefix to every style class so none can clash with your theme's own classes.

Then paste the new `sections/loftrest-landing.liquid` into your theme again. Pasting the template again resets the FAQ to what's in `index.html`, so skip that step if you've edited questions in Shopify.
