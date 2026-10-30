"""Google Search responsive search ads for the four persona concepts (draft until Kelly approves).

Built from the Meta copy Mitchell approved on October 28, 2026, with no incentive (the November offer
lives on the landing pages). No build timeline is claimed, per the Four Buyers deck.
Run: python3 google_search_rsa.py   checks Google's limits and writes google_search_rsa.txt.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHARED_H = ["Mitchell Homes", "Family Owned Since 1992", "We Build in VA, NC, SC and MD"]
SHARED_D = "Family owned since 1992, with Design Centers across Virginia and North Carolina."

CONCEPTS = [
    {"name": "1 Value Unlocker (run first)", "url": "https://simplymitchellhomes.com/land", "paths": ("Land", "SimplyMitchell"),
     "headlines": SHARED_H + ["Build on Your Land", "Your Land Is Worth More", "Land Can Be Your Down Payment",
                              "See the Math on Your Land", "You Already Own the Hard Part", "Zero Down With SimplyMitchell",
                              "Closing Costs Paid", "No Construction Loan Needed", "More Than 40 Floor Plans",
                              "Over 40,000 Selections", "Talk to a New Home Consultant", "Custom Homes on Your Land"],
     "descriptions": ["Your land can be your down payment. You already own the hardest part. Here is the math.",
                      "Zero down, closing costs paid and no construction loan with SimplyMitchell. See the math.",
                      "More than 40 floor plans and 40,000 selections, built on land you own or are buying.",
                      SHARED_D]},
    {"name": "2 Planner", "url": "https://simplymitchellhomes.com/math", "paths": ("Math", "SimplyMitchell"),
     "headlines": SHARED_H + ["Custom Without the Unknowns", "Priced Before We Build", "Start With 40 Home Plans",
                              "You Hear From Us Every Week", "You Stay in Control", "We Make the Path Predictable",
                              "See the Plans", "Custom Homes on Your Land", "Zero Down With SimplyMitchell",
                              "No Construction Loan Needed", "Over 40,000 Selections", "Closing Costs Paid"],
     "descriptions": ["Custom does not have to mean unpredictable. Every choice is priced before we build.",
                      "Start with more than 40 home plans, not a blank page, and hear from us every week.",
                      "Zero down, closing costs paid and no construction loan with SimplyMitchell.",
                      SHARED_D]},
    {"name": "3 Transitioner (after legal approves the persona's bank line)", "url": "https://simplymitchellhomes.com/math", "paths": ("Math", "SimplyMitchell"),
     "headlines": SHARED_H + ["No Construction Loan Needed", "Skip the Construction Loan", "Ready to Build on Your Land?",
                              "A Finished Home on Your Land", "Land Can Be Your Down Payment", "Big Decisions, Small Steps",
                              "Zero Down With SimplyMitchell", "Closing Costs Paid", "See the Math",
                              "More Than 40 Floor Plans", "Talk to a New Home Consultant", "Custom Homes on Your Land"],
     "descriptions": ["If a construction loan stopped you from building on your land, SimplyMitchell removes it.",
                      "Zero down, closing costs paid and no construction loan. See the math on your land.",
                      "A finished home on the land you already own. Big decisions become small steps.",
                      SHARED_D]},
    {"name": "4 Grounded Dreamer", "url": "https://simplymitchellhomes.com/math", "paths": ("Math", "SimplyMitchell"),
     "headlines": SHARED_H + ["Give Your Dream Home a Date", "40 Plans, 40,000 Ways", "Make It Yours",
                              "It Starts With One Appointment", "Bring the Photos You Saved", "Built on the Land You Own",
                              "Your Vision, Made Doable", "See the Floor Plans", "Zero Down With SimplyMitchell",
                              "No Construction Loan Needed", "Closing Costs Paid", "Talk to a New Home Consultant"],
     "descriptions": ["You have been saving photos of this house for years. Bring them, we will bring the plans.",
                      "More than 40 floor plans and 40,000 selections to make it yours, priced before we build.",
                      "Zero down, closing costs paid and no construction loan with SimplyMitchell.",
                      SHARED_D]},
]


def check():
    errors = []
    for c in CONCEPTS:
        h, d = c["headlines"], c["descriptions"]
        if len(h) != 15 or len(set(h)) != 15:
            errors.append(f"{c['name']}: needs 15 unique headlines, has {len(set(h))}")
        if len(d) != 4:
            errors.append(f"{c['name']}: needs 4 descriptions")
        for text, limit in [(x, 30) for x in h] + [(x, 90) for x in d] + [(x, 15) for x in c["paths"]]:
            if len(text) > limit:
                errors.append(f"{c['name']}: over {limit} ({len(text)}): {text}")
            if any(ch in text for ch in "–—-"):
                errors.append(f"{c['name']}: dash in: {text}")
    return errors


def render():
    lines = ["MITCHELL HOMES PERSONA CAMPAIGN: GOOGLE SEARCH ADS (responsive search ads)",
             "For the Brand campaign test, one concept at a time, starting with Value Unlocker.",
             "15 headlines and 4 descriptions each. If you pin anything, pin Mitchell Homes to headline position 1.",
             "No incentive in the ads; the November offer lives on the landing pages.", ""]
    for c in CONCEPTS:
        lines += ["=" * 60, c["name"].upper(), f"Final URL: {c['url']}", f"Display path: {c['paths'][0]} / {c['paths'][1]}", "", "Headlines:"]
        lines += [f"{i}. {x}" for i, x in enumerate(c["headlines"], 1)]
        lines += ["", "Descriptions:"]
        lines += [f"{i}. {x}" for i, x in enumerate(c["descriptions"], 1)]
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    errs = check()
    if errs:
        sys.exit("\n".join(errs))
    text = render()
    with open(os.path.join(HERE, "google_search_rsa.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
