"""Customer reviews used by the product page, homepage and Reviews page templates.

These customers bought LoftRest before the online store opened, so there is no order
to match them to: they are labelled with SOURCE, not shown as "Verified buyer", and
have no star rating (stars 0) because none was given. Text is exactly as written.
Don't add reviews that make health claims (pain relief, insomnia, disc problems):
on our site, a testimonial counts as our own advertising.
"""
SOURCE = "Purchased before our online store opened"

REVIEWS = [
  ("Lonzo R.", "I love this neck massager cervical pillow hot compress. The heat is excellent, massage is good but the best part is the stretch. It really relaxes the neck. I'm really happy with my purchase. I recommend this seller! Thank you for your speedy shipping! Lonzo R."),
  ("Nadia K.", "I work 10 hour shifts doing software sales and by the evening my trap muscles are literally rock hard. I used to make my partner rub my shoulders every night lol. bought this instead and the heat + air lift combo forces the muscles to actually relax. 10/10 worth every cent."),
  ("Jake M.", "I do framing and overhead work all day so my upper back and neck are usually shot by the time I get home. Most neck stretchers are those hard plastic foam blocks where you have to lay on a cold hardwood floor... yeah right. This one you can actually use in bed. The heat setting alone is worth it."),
  ("Tom W.", "Most medical gadgets end up sitting in a closet after 3 days because they're a hassle to set up. I just leave this on my bed, plug it in while I do my nighttime skincare, and lay on it for 15 mins while scrolling on my phone. Auto shuts off so you don't even have to think about it."),
  ("Chris A.", "My girlfriend used to get so annoyed because I'd flip my pillow 20 times a night trying to get comfortable. Got the 2-pack bundle so we both have one. She uses hers for her screen neck, I use mine so I actually stay still and sleep. Best purchase we've made this year."),
  ("David B.", "Man i absolutely love this thing, just used it for the first time for 30 mins and had be feeling super good. only thing i dont like about it is that you have to keep it plugged in for power for it to work. but still definitely worth it david B."),
  ("Rachel J.", "The massage is a bit weak, feels like lying on a cell phone, haha. However, the air blowing and heating functions are quite good. The product packaging and visuals are also satisfactory. Rachel J."),
  ("Anonymous", "I love it so much.. I hope it doesn't break down and lasts a long time... Even if you just use it as a pillow without vibrating it. It's comfortable to sleep on your side. I'll use it for about a week and see if there are any issues. I need to buy one more as a gift. The vibration isn't strong, but it makes a sound like a lullaby. Haha. It's good to use Aero to moisten the throat."),
]

STARS = {"type": "range", "id": "stars", "label": "Stars", "min": 0, "max": 5, "step": 1, "default": 5,
         "info": "0 = no star rating. Only use the rating the customer actually gave."}
SOURCE_SETTING = {"type": "text", "id": "source", "label": "Where they bought it (optional)",
                  "info": "Shown under the name, e.g. for customers who bought before the online store opened."}


def blocks(extra=None):
    """Template blocks for the reviews: {"review_1": {...}, ...}."""
    out = {}
    for i, (name, text) in enumerate(REVIEWS):
        s = {"stars": 0, "review": text, "name": name, "verified": False, "source": SOURCE}
        s.update(extra or {})
        out[f"review_{i+1}"] = {"type": "review", "settings": s}
    return out
