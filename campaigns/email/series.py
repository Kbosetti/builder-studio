"""Fall 2026 email series for Mitchell Homes: Design Dollars, Home Portrait, Four Buyers, plus realtor and homeowner emails.

Every line follows campaigns/FACTS.md. Block types: p, list, steps, ladder, covers, quote, grid, offer, cta, small, video (a thumbnail that opens the video; see videos/).
Rendered by build.py into out/<id>.html (paste into Builder Studio or Lasso) and out/<id>.txt.
"""

M = "https://media.mitchellhomesinc.com/276/"
GHL = "https://assets.cdn.filesafe.space/5o5zLlUPPizy6Ajp61oF/media/"
QUIZ = "https://mitchellhomesliving.com/portrait"
SMH = "https://simplymitchellhomes.com"
DD = SMH + "/design-dollars"

def hero(path, alt):
    return {"src": M + path + "?width=1200&height=640&mode=crop", "alt": alt}

PAINT = {  # regional watercolors used on the quiz, 560 x 315
    "Fredericksburg": GHL + "67b7f0dc-c0d0-4510-816b-8952132379e1.jpg",
    "Raleigh": GHL + "9a7ff568-766d-4aad-bf94-2428d6c775e0.jpg",
    "Wilmington": GHL + "6773dfda-39de-4b52-9f6f-7f511483e779.jpg",
    "Newport News": GHL + "32da2899-c18d-49e6-a1f8-6d398238da40.jpg",
    "Richmond": GHL + "a579f035-57a0-4942-be79-a20750ce1402.jpg",
    "Lake": GHL + "666b6807-d99e-4cf5-9b4d-70d76e36e4fa.jpg",
}

DD_BAND = {"t": "offer",
           "head": "Up to $25,000 in Mitchell Design Dollars*",
           "text": "Every Mitchell home starts with $5,000, and the credit grows the more you personalize. Sign now and your incentive is locked. Your tier is set later, when you choose what goes in the home."}

DOWNEY = {"t": "quote",
          "text": "Talk about no closing costs, no down payment, no construction loan. That's a big deal. I don't think we appreciated what that meant initially. Now looking back, we're like wow, that's the best choice we could've made to go with Mitchell.",
          "by": "Lavonnia and Rick Downey, Mitchell homeowners, Henrico, Virginia",
          "link": "https://www.youtube.com/watch?v=9vmi-miQzKU", "linktext": "Watch their story"}

SERIES = [
    {"key": "portrait", "name": "The Home Portrait", "stage": "Discover", "campaign": "fall26_portrait",
     "audience": "Full marketing list, minus contacts already tagged home portrait quiz (they have their portrait) and anyone under contract.",
     "goal": "Quiz starts. Every email has one job: send the reader to the quiz.",
     "emails": [
        {"id": "hp1", "send": "Thursday, October 22", "segment": "Engaged contacts (opened or clicked in the last 90 days) and every lead since September 1",
         "subject": "What would your home look like?",
         "preview": "Answer eight questions. We paint your Home Portrait.",
         "hero": hero("2024/7/24/1.jpg", "A white Mitchell farmhouse with a wraparound porch, set back in the pines at the end of a long drive"),
         "eyebrow": "The Home Portrait", "headline": "Every home is a portrait. Discover yours.",
         "blocks": [
            {"t": "p", "text": "Every home we build is a portrait of the people who live in it. The porch where Saturday starts. The kitchen everyone ends up in. The view you already own."},
            {"t": "p", "text": "So we made a way to see yours. Answer eight questions about the home you dream of and the land it belongs on, and we paint your Home Portrait: a painting of a home in your region, the spaces you told us matter most, and a clear path from here to the keys."},
            {"t": "p", "text": "It takes about 90 seconds. Home first, land in the middle, timing last. If you do not own land yet, that is a good answer too."},
            {"t": "video", "v": "reel_land", "text": "Our 27-second reel: the land you already own, and the home only you would build."},
            {"t": "cta", "text": "Take the Quiz", "href": QUIZ},
            {"t": "small", "text": "Eight questions. About 90 seconds. Your portrait appears the moment you finish."}]},
        {"id": "hp2", "send": "Thursday, November 5", "segment": "Engaged contacts (written for landowners, welcoming to everyone)",
         "subject": "Your land is part of the portrait",
         "preview": "The question we ask fifth changes everything we paint.",
         "hero": hero("2024/8/14/10_iWQs7EE.jpg", "Aerial view of a Mitchell home in a green clearing surrounded by forest"),
         "eyebrow": "The Home Portrait", "headline": "Land is silent until you give it a voice",
         "blocks": [
            {"t": "p", "text": "Most builders ask about your land first. We ask fifth."},
            {"t": "p", "text": "By the time you reach that question in the Home Portrait, you have already pictured the porch, the kitchen and the people under the roof. Then we ask about the ground it stands on, because that one answer changes everything we paint for you."},
            {"t": "list", "items": [
                "If you own land, your portrait shows how it can carry the build: zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.",
                "If there is family land in the picture, it shows the same path.",
                "If you are still looking, it shows what you can start on now, before you hold a deed."]},
            {"t": "video", "v": "cuomo", "text": "See how their land became their home."},
            {"t": "cta", "text": "Take the Quiz", "href": QUIZ},
            {"t": "small", "text": "Eight questions. About 90 seconds."}],
         "financing": True},
        {"id": "hp3", "send": "Thursday, November 12", "segment": "Engaged contacts who have not taken the quiz yet",
         "subject": "Nine portraits. Which one is yours?",
         "preview": "The Landowner's, the Dreamer's, the Family, the Planner's, and one for the getaway.",
         "hero": hero("2024/6/24/Mathews_1_Aerial.jpg", "Aerial view of a Mitchell home on a wooded homesite"),
         "eyebrow": "The Home Portrait", "headline": "Nine portraits. One of them is yours.",
         "blocks": [
            {"t": "p", "text": "Your Home Portrait is painted from the answers you give. Your region sets the scene. Your land, your people and the way you make big decisions shape the rest."},
            {"t": "covers", "items": [
                ["The Landowner's Portrait", "For buyers who own land, or have family land, and want to see the math."],
                ["The Dreamer's Portrait", "For buyers who can already see the finished home and want a clear path to it."],
                ["The Family Portrait", "For a family in a full season of life, where big decisions become small steps."],
                ["The Planner's Portrait", "For buyers who want every step in order and every choice priced before we build."],
                ["The Gathering Place Portrait", "For the lake house, the coastal retreat or the mountain getaway."]]},
            {"t": "p", "text": "The first four each come in two versions, one for buyers who own land and one for buyers who are still looking. That makes nine."},
            {"t": "video", "v": "reel_which", "text": "Our 25-second reel: planner, dreamer, or the one already doing the math?"},
            {"t": "cta", "text": "Find Yours", "href": QUIZ}]},
        {"id": "hp4", "send": "Thursday, November 19", "segment": "Engaged contacts, or contacts interested in lake, coastal or mountain areas if that field exists",
         "subject": "The getaway you keep promising yourselves",
         "preview": "Lake, coast or mountains. Your portrait paints it.",
         "hero": hero("2026/3/24/10_mwFjkrl.jpg", "Aerial view of a Mitchell home among the trees beside the water"),
         "eyebrow": "The Home Portrait", "headline": "The place everyone comes home to",
         "blocks": [
            {"t": "p", "text": "Some homes are built for every day. Some are built for the long table, the full-house weekend and the place you plan to retire."},
            {"t": "p", "text": "If that is the home you keep talking about, there is a portrait for it. Choose Smith Mountain Lake, Lake Gaston, the Shenandoah Valley or the Eastern Shore and Outer Banks, tell us it is a getaway, a family retreat or the place you will retire, and we paint The Gathering Place Portrait: lake, coast or mountains."},
            {"t": "p", "text": "Second homes are where banks get strict. Mitchell self-funds every build, so there is no construction loan to qualify for. The second home banks make hard, Mitchell makes simple."},
            {"t": "video", "v": "reel_saturday", "text": "Our 27-second reel: coffee on the porch, bread in the oven, and room to run."},
            {"t": "cta", "text": "Take the Quiz", "href": QUIZ},
            {"t": "small", "text": "Eight questions. About 90 seconds."}],
         "financing": True},
     ]},

    {"key": "designdollars", "name": "Mitchell Design Dollars", "stage": "Decide", "campaign": "fall26_designdollars",
     "audience": "Warm audiences and the database only, per the approved rollout. Full marketing list, minus anyone already under contract.",
     "goal": "Design Center conversations and reservations before the monthly reserve-by date: October 31, then November 30 once Mitchell confirms it.",
     "emails": [
        {"id": "dd1", "send": "Tuesday, October 20", "segment": "Full list",
         "subject": "It is your land. Make it your home.",
         "preview": "Every Mitchell home now comes with $5,000 in Design Dollars. Personalize more, and we add more.",
         "hero": hero("2023/2/6/Design_Center_13_IfaBRgj.jpg", "A kitchen display in a Mitchell Design Center with white cabinets, a copper hood and brass pendants"),
         "eyebrow": "Mitchell Design Dollars", "headline": "The more of you goes into the home, the more Mitchell puts in",
         "blocks": [
            {"t": "p", "text": "You did not buy your land to live in a stranger's idea of a home. The cabinets, the counters, the tile, the light over the table: that is where a house becomes yours."},
            {"t": "p", "text": "Right now, every Mitchell home comes with $5,000 in Mitchell Design Dollars to spend at the Design Center. Personalize more, and we add more, up to $25,000."},
            {"t": "p", "text": "Nobody starts at zero. And you do not have to choose a single finish to secure it."},
            DD_BAND,
            {"t": "cta", "text": "See How It Works", "href": DD}],
         "dd": True},
        {"id": "dd2", "send": "Tuesday, October 27", "segment": "Full list",
         "subject": "Choose $60,000 in selections. Take home $75,000 worth.",
         "preview": "Here is how Mitchell Design Dollars grow with the choices you make.",
         "hero": hero("2026/3/24/59-DSC06144.jpg", "A finished Mitchell kitchen with wood cabinets, a white island and a farmhouse sink"),
         "eyebrow": "Mitchell Design Dollars", "headline": "Spend and add",
         "blocks": [
            {"t": "p", "text": "Here is the simplest way to explain Mitchell Design Dollars. You choose your selections at the Design Center. Mitchell adds Design Dollars on top, and the amount grows with what you choose."},
            {"t": "ladder"},
            {"t": "p", "text": "Choose $60,000 in selections and Mitchell adds $15,000. You pay for $60,000 and take home $75,000 worth, added on top as extra selections at retail."},
            {"t": "p", "text": "Design Dollars go toward cabinets, countertops, flooring, tile, trim and millwork, doors, lighting and electrical, plumbing fixtures, appliances, paint and hardware. They never come off the base price, and they are never cash."},
            {"t": "deadline", "text": "Reserve by Saturday, October 31, and your Design Dollars are locked. Your tier is set later, when you choose what goes in the home."},
            {"t": "cta", "text": "Find Your Tier", "href": DD}],
         "dd": True},
        {"id": "dd3", "send": "Tuesday, November 10", "segment": "Full list, minus anyone who booked a Design Center visit",
         "hold": "Says reserve by November 30, the November reserve-by date. Waits on Mitchell confirming it (question 1).",
         "subject": "You do not have to pick the tile today",
         "preview": "Sign now and your Design Dollars are locked. Your tier is set later.",
         "hero": hero("2023/3/24/Richmond_Design_Studio.jpg", "Inside the Richmond Design Studio, with a wall of cabinet and finish samples"),
         "eyebrow": "Mitchell Design Dollars", "headline": "Sign now. Choose later.",
         "blocks": [
            {"t": "p", "text": "Most people stall right here. They think every cabinet, countertop and tile has to be settled before they can move forward."},
            {"t": "p", "text": "It does not. Sign now, and your incentive is locked. Your tier is decided later, when you sit down at the Design Center and choose what actually goes in the home."},
            {"t": "p", "text": "When that day comes, you choose in daylight, with the number in front of you, before construction begins. And your reservation deposit is $150. That is all Mitchell receives until closing."},
            {"t": "video", "v": "ferguson", "text": "Tips from the Ferguson showroom team on choosing selections you will love for years."},
            {"t": "deadline", "text": "Reserve by Monday, November 30, and your Design Dollars are locked. Your tier is set later, when you choose what goes in the home."},
            {"t": "cta", "text": "Book Your Design Center Visit", "href": DD},
            {"t": "small", "text": "Start with a conversation, not a commitment. Tell us where you are building, and an online sales counselor will call you, usually within fifteen minutes."}],
         "dd": True},
        {"id": "dd4", "send": "Tuesday, November 24", "segment": "Full list, minus anyone who booked or reserved",
         "hold": "Says reserve by November 30, the November reserve-by date. Waits on Mitchell confirming it (question 1).",
         "subject": "Where your Design Dollars go",
         "preview": "Cabinets, counters, tile and more. Reserve by November 30, 2026.",
         "hero": hero("2023/2/6/Design_Center_15_WcldBUt.jpg", "A Mitchell Design Center kitchen display with a wood island, copper hood and plumbing and electrical selections"),
         "eyebrow": "Mitchell Design Dollars", "headline": "Picture your own list",
         "blocks": [
            {"t": "p", "text": "A quick guide to what Mitchell Design Dollars cover, so you can start picturing your own list."},
            {"t": "twocol", "left": ["Design Dollars apply to", ["Cabinets", "Countertops", "Flooring", "Tile", "Trim and millwork", "Doors", "Lighting and electrical", "Plumbing fixtures", "Appliances", "Paint and hardware"]],
             "right": ["They do not apply to", ["Structural options", "Decks", "Garages", "Basements", "Well and septic", "Site work", "Contract category options", "The base price of the home", "Cash of any kind"]]},
            {"t": "p", "text": "Every Mitchell home starts with $5,000, and the credit grows the more you personalize, up to $25,000."},
            {"t": "deadline", "text": "Reserve by Monday, November 30, 2026, and your Design Dollars are locked. Your tier is set later, when you choose what goes in the home."},
            {"t": "cta", "text": "Start With a Conversation", "href": DD}],
         "dd": True},
     ]},

    {"key": "fourbuyers", "name": "The Four Buyers", "stage": "Believe", "campaign": "fall26_fourbuyers",
     "audience": "Landowner segment (registered as owns land, or quiz contacts tagged with land) for the first four; the looking-for-land segment gets the fifth. Send to Virginia and Maryland contacts first; the Dreamer and No Land emails have Carolinas versions.",
     "goal": "Visits to the matching page and calls to a New Home Consultant. Each email carries one argument and one page.",
     "emails": [
        {"id": "fb1", "send": "Wednesday, November 4", "segment": "Owns land or family land, Virginia and Maryland",
         "subject": "Your land is worth more than you think",
         "preview": "You already own the hardest part of building. Here is the math.",
         "hero": hero("2024/7/5/1_GuQrrFW.jpg", "Aerial view of a Mitchell home standing alone on wide green farmland"),
         "eyebrow": "Building on your land", "headline": "Your land can be your down payment",
         "blocks": [
            {"t": "p", "text": "You already own the hardest part of building a custom home. Most landowners do not realize how far along that puts them."},
            {"t": "p", "text": "Most builders send you to a bank for a construction loan before anyone turns a shovel. We do not. Mitchell self-funds every build, so the land you hold counts toward the home, with zero down, zero closing costs and no construction loan."},
            {"t": "p", "text": "That means one closing instead of two, no draw period interest while the house goes up, and no bank deciding whether your land counts."},
            {"t": "cta", "text": "See What Your Land Can Build", "href": SMH + "/land"},
            DOWNEY,
            DD_BAND],
         "dd": True, "financing": True},
        {"id": "fb2", "send": "Tuesday, November 17", "segment": "Owns land or family land, Virginia and Maryland",
         "subject": "A custom home on your land, without the unknowns",
         "preview": "Start with a plan that already works. Every choice priced before we build.",
         "hero": hero("2026/3/24/38-DSC06023.jpg", "A bright Mitchell living room with a fireplace, built-in shelves and tall windows"),
         "eyebrow": "Building on your land", "headline": "Custom does not have to mean unpredictable",
         "blocks": [
            {"t": "p", "text": "Everyone has heard a build story that did not end well. The number moved after signing, and nobody explained why. That is the part our process is built to remove."},
            {"t": "steps", "items": [
                ["Start with a plan that works", "More than 40 floor plans from 1,000 to 3,000 square feet. You are editing a plan that already works, not inventing one and hoping."],
                ["Every choice priced before we build", "You choose in daylight, with the number in front of you, before construction begins. Your selections are reviewed and signed off at the pre-construction meeting, and then ground breaks."],
                ["You hear from us every week", "From groundbreaking to move-in, so you never have to wonder where things stand."]]},
            {"t": "video", "v": "keys", "text": "What happens between signing and the day you get your keys."},
            {"t": "cta", "text": "See How We Build", "href": SMH + "/land"},
            DD_BAND],
         "dd": True},
        {"id": "fb3", "send": "Later, when legal clears the wording (question 7)", "segment": "Owns land or family land, Virginia and Maryland",
         "hold": "Hold until legal approves the financing wording (to match the Transitioner ad and reel) and the comparison figures on the /calculator page are confirmed.",
         "subject": "No construction loan to build on your land",
         "preview": "If a bank is the reason you stopped, read this.",
         "hero": hero("2026/3/24/07-DJI_20260224134444_0238_D_copy.jpg", "A finished Mitchell home with a covered front porch, wood posts and a curved walk"),
         "eyebrow": "Building on your land", "headline": "If a construction loan is why you stopped, read this",
         "blocks": [
            {"t": "p", "text": "A lot of people who want to build on their land called a bank once, heard what a construction loan involves, and quietly put the plan away."},
            {"t": "p", "text": "A construction loan usually means a down payment before work starts, two closings, interest while the house goes up, and inspections before every draw. It is the obstacle that ends most builds before they begin."},
            {"t": "p", "text": "With Mitchell there is no construction loan. Mitchell self-funds every build, so there is zero down, zero closing costs and one closing. The land you already own counts toward the home."},
            {"t": "p", "text": "Then comes the part you wanted all along: a finished home on the land you already own."},
            {"t": "video", "v": "downey", "text": "Hear what building with no construction loan meant to them."},
            {"t": "cta", "text": "See the Math", "href": SMH + "/calculator"},
            DD_BAND],
         "dd": True, "financing": True},
        {"id": "fb4", "send": "Later, when the Dreamer page is fixed (question 5)", "segment": "Owns land or family land, Virginia and Maryland (fb4c for the Carolinas)",
         "hold": "Hold until the Dreamer pages drop the line A price locked from day one, which conflicts with the approved pricing claim.",
         "subject": "Your dream home has a folder, not a date",
         "preview": "One appointment. Bring the photos you have been saving.",
         "hero": hero("2026/3/3/55-DSC06124.jpg", "A Mitchell kitchen with a large white island, wood cabinets and woven pendant lights"),
         "eyebrow": "Building on your land", "headline": "It starts with one appointment",
         "blocks": [
            {"t": "p", "text": "You have been saving photos of this house for years. The kitchen. The porch. Where the light lands in the afternoon. You know exactly what you want."},
            {"t": "p", "text": "What is missing is not inspiration. It is a start."},
            {"t": "p", "text": "So here is the smallest possible next step: one appointment at a Mitchell Design Center. Bring the photos you have been saving. We will bring the plans and price what is in them. With more than 40 floor plans and more than 40,000 selections, most of what is in your folder is something we already carry."},
            {"t": "p", "text": "Design Centers in Fredericksburg, Richmond and Newport News."},
            {"t": "cta", "text": "Bring Your Photos", "href": SMH + "/dreamer"},
            DD_BAND],
         "dd": True,
         "variant": {"id": "fb4c", "segment": "Owns land or family land, North and South Carolina",
                     "replace": [["Design Centers in Fredericksburg, Richmond and Newport News.", "Design Centers in Raleigh and Wilmington."], [SMH + "/dreamer", SMH + "/dreamer-carolinas"]]}},
        {"id": "fb5", "send": "Wednesday, November 4", "segment": "Looking for land, Virginia and Maryland (fb5c for the Carolinas)",
         "hold": "Check first that the plan guide email is built: the /no-land form promises one, and nothing sends it yet.",
         "subject": "You do not have to own land yet",
         "preview": "Start designing now. Bring us the lot when you find it.",
         "hero": hero("2026/3/24/10_UuSAaPU.jpg", "Aerial view of a Mitchell home in a wooded valley below the mountains"),
         "eyebrow": "Building on your land", "headline": "Start the home before you have the land",
         "blocks": [
            {"t": "p", "text": "Buying land and building a house sound like two impossible things stacked on top of each other. We take one of them off your plate."},
            {"t": "steps", "items": [
                ["Still yours: finding the lot", "You choose where you want to be. We do not sell land, and we will not tell you where to buy."],
                ["Ours: everything after that", "The plan, the selections, the permits, the build, and the money that normally has to sit in a construction loan."]]},
            {"t": "p", "text": "You do not have to wait for a deed to begin. Come into a Design Center, walk the plan library, and see what your budget actually buys."},
            {"t": "video", "v": "land101", "text": "What to look for before you buy land to build on."},
            {"t": "cta", "text": "See How It Works", "href": SMH + "/no-land"},
            {"t": "small", "text": "Want to look around first? Browse more than 40 floor plans at mitchellhomesinc.com.", "href": "https://www.mitchellhomesinc.com/new-homes/floorplans/"},
            DD_BAND],
         "dd": True,
         "variant": {"id": "fb5c", "segment": "Looking for land, North and South Carolina",
                     "replace": [[SMH + "/no-land", SMH + "/no-land-carolinas"]]}},
     ]},

    {"key": "partners", "name": "Realtors and homeowners", "stage": "Refer", "campaign": "fall26_referral",
     "reason": "You are receiving this email because you are on the Mitchell Homes real estate partner list.",
     "audience": "Realtor and broker contacts (land listing agents first), and past Mitchell homeowners.",
     "goal": "Referrals into the quiz and the Design Dollars page from people who already know buyers.",
     "emails": [
        {"id": "re1", "send": "Wednesday, October 21", "segment": "Realtors and brokers, land listing agents first",
         "hold": "Confirm the current realtor incentive terms with Mitchell before sending.",
         "subject": "Your buyer owns land. We build on it.",
         "preview": "Zero down, no construction loan, and up to $25,000 in Design Dollars for your clients.",
         "hero": hero("2024/7/5/1_GuQrrFW.jpg", "Aerial view of a Mitchell home standing alone on wide green farmland"),
         "eyebrow": "For real estate professionals", "headline": "The easiest yes for a client with land",
         "blocks": [
            {"t": "p", "text": "When a client buys land, or already owns it, the next question is usually the hard one: how do we build on it without a construction loan and a second closing?"},
            {"t": "p", "text": "That is the question Mitchell answers. We build custom homes on land the buyer owns, and Mitchell self-funds every build: zero down, zero closing costs and no construction loan."},
            {"t": "list", "items": [
                "More than 40 floor plans from 1,000 to 3,000 square feet, and more than 40,000 selections.",
                "Every Mitchell home starts with $5,000 in Mitchell Design Dollars, up to $25,000 the more your client personalizes.",
                "Mitchell has a realtor incentive program for referred buyers. Ask us for the current terms."]},
            {"t": "p", "text": "Listing land? Buyers who can picture the home are easier to move. The Home Portrait gives them that picture in about 90 seconds."},
            {"t": "video", "v": "cuomo", "text": "A client story you can share with buyers who own land."},
            {"t": "cta", "text": "Send Your Client the Home Portrait", "href": QUIZ},
            {"t": "small", "text": "Eight questions, about 90 seconds, and your client sees a painted portrait of their home. Prefer to talk first? Call a New Home Consultant at the numbers below."}],
         "dd": True, "financing": True},
        {"id": "ra1", "send": "Wednesday, November 4", "segment": "Realtors and brokers, land and rural agents first",
         "hold": "Confirm with Mitchell that consultants may introduce buyers who are still looking for land to local agents (question 17).",
         "subject": "Our buyers need land. Do you know land?",
         "preview": "We would like to know the agents who do.",
         "hero": hero("2026/3/24/10_UuSAaPU.jpg", "Aerial view of a Mitchell home in a wooded valley below the mountains"),
         "eyebrow": "For real estate professionals", "headline": "Our buyers need agents who know land",
         "blocks": [
            {"t": "p", "text": "Every month, people come to Mitchell ready to build a custom home and still looking for the right lot. They need an agent who knows land: perc tests, wells and septic, road access, easements and county rules."},
            {"t": "p", "text": "We would like to know the agents who do. If land is part of your business, reply to this email with the counties you work in, and we will add you to our land partner list."},
            {"t": "p", "text": "When a Mitchell buyer is still looking, we want to be able to introduce them to someone who knows the ground."},
            {"t": "cta", "text": "See What We Tell Buyers Without Land", "href": SMH + "/no-land"},
            {"t": "small", "text": "Mitchell has a realtor incentive program for referred buyers. Ask us for the current terms."}]},
        {"id": "rb2", "send": "Wednesday, November 11", "segment": "Realtors and brokers, land listing agents first",
         "hold": "Confirm the current realtor incentive terms with Mitchell (question 11).",
         "subject": "When your land listing needs a picture",
         "preview": "Buyers who can see the home are easier to move.",
         "hero": hero("2024/8/14/10_iWQs7EE.jpg", "Aerial view of a Mitchell home in a green clearing surrounded by forest"),
         "eyebrow": "For real estate professionals", "headline": "Help land buyers see the home",
         "blocks": [
            {"t": "p", "text": "Raw land is hard to fall in love with. Most buyers walking a lot are trying to picture the house, and most cannot."},
            {"t": "p", "text": "That is what the Home Portrait does. Your buyer answers eight questions about the home they want and the land it belongs on, and in about 90 seconds they see a portrait of it, with a clear path to building."},
            {"t": "p", "text": "When they are ready, Mitchell builds custom homes on land the buyer owns and self-funds every build: zero down, zero closing costs and no construction loan."},
            {"t": "cta", "text": "Send Your Buyer the Home Portrait", "href": QUIZ},
            {"t": "small", "text": "Mitchell has a realtor incentive program for referred buyers. Ask us for the current terms."}],
         "financing": True},
        {"id": "rb3", "send": "Later, when the realtor incentive terms are confirmed (question 11)", "segment": "Realtors and brokers",
         "hold": "Confirm the current realtor incentive terms with Mitchell (question 11).",
         "subject": "Your client's down payment may be in the ground",
         "preview": "Inherited land, family land, the acreage they already own.",
         "hero": hero("2026/3/24/10_mwFjkrl.jpg", "Aerial view of a Mitchell home among the trees beside the water"),
         "eyebrow": "For real estate professionals", "headline": "The land your client owns can count toward the home",
         "blocks": [
            {"t": "p", "text": "Some of your clients own land they have never thought of as a down payment: a parcel they inherited, family acreage, a lot they bought years ago."},
            {"t": "p", "text": "With Mitchell, that land can count toward a custom home. Mitchell self-funds every build, so there is zero down, zero closing costs, no construction loan and one closing instead of two."},
            {"t": "p", "text": "Every Mitchell home also starts with $5,000 in Mitchell Design Dollars, up to $25,000 the more your client personalizes."},
            {"t": "list", "items": [
                "Refer a client: reply with their name and county, or have them call a New Home Consultant.",
                "Mitchell has a realtor incentive program for referred buyers. Ask us for the current terms."]},
            {"t": "cta", "text": "See What Their Land Can Build", "href": SMH + "/land"}],
         "dd": True, "financing": True},
        {"id": "ra2", "send": "Thursday, November 19, the day after the Lunch and Learn", "segment": "Realtors and brokers, land and rural agents first",
         "subject": "What our buyers check before they buy a lot",
         "preview": "A short checklist to share with your land clients.",
         "hero": hero("2024/7/24/1.jpg", "A white Mitchell farmhouse with a wraparound porch, set back in the pines at the end of a long drive"),
         "eyebrow": "For real estate professionals", "headline": "A lot checklist for your land clients",
         "blocks": [
            {"t": "p", "text": "When a buyer plans to build, the right lot is about more than the view. Here is what your clients will want to know before they make an offer."},
            {"t": "covers", "items": [
                ["Soil and perc test", "Whether the ground supports a septic system, and what kind."],
                ["Water", "A well or a public connection, and what either costs."],
                ["Access and utilities", "Road frontage, the driveway, power and internet."],
                ["Easements and restrictions", "What is recorded on the deed, and any covenants."],
                ["Zoning and flood zone", "What can be built, and where on the lot."],
                ["Clearing and grading", "How much work the site needs before the build."]]},
            {"t": "small", "text": "Behind the Build: Purchasing Land 101", "href": "https://www.youtube.com/watch?v=trgJ8maymOA"},
            {"t": "small", "text": "Behind the Build: Well and Septic", "href": "https://www.youtube.com/watch?v=zWwtw8qgp4w"},
            {"t": "cta", "text": "Share the Home Portrait", "href": QUIZ}]},
        {"id": "ho1", "send": "Later, when a homeowner referral thank-you is decided (question 12)", "segment": "Past Mitchell homeowners",
         "reason": "You are receiving this email because you built your home with Mitchell Homes.",
         "hold": "Confirm with Mitchell whether a homeowner referral thank-you exists before adding one. This version makes no offer.",
         "subject": "Know someone with land and a dream?",
         "preview": "The best Mitchell homes start with a homeowner's introduction.",
         "hero": hero("2026/3/3/ava_farmhouse-extended_sky.jpg", "A Mitchell farmhouse with a long front porch under an evening sky"),
         "eyebrow": "For Mitchell homeowners", "headline": "You already know what it is like",
         "blocks": [
            {"t": "p", "text": "You know what it took to build on your land, and what it felt like to walk through the front door for the first time. If someone you know is still dreaming about that moment, here is an easy way to help them start."},
            {"t": "p", "text": "If someone you know owns land, has family land, or keeps talking about the home they want to build someday, send them the Home Portrait. Eight questions, about 90 seconds, and they see a painted portrait of the home they have been describing."},
            {"t": "cta", "text": "Share the Home Portrait", "href": QUIZ},
            {"t": "p", "text": "And when they are ready to talk, they can call a New Home Consultant directly. Thank you for building with us, and for every introduction."}]},
     ]},

    {"key": "nurture", "name": "Quiet-lead nurture", "stage": "Nurture", "campaign": "fall26_nurture",
     "audience": "Any lead with no reply, no booked appointment and no stage change seven days after first contact. Leaves the moment they reply, book, reserve or opt out.",
     "goal": "A reply or a booked call. Personal notes from the consultant alternate with designed emails and texts over 60 days, then the lead moves to the monthly newsletter.",
     "emails": [
        {"id": "nu1", "send": "Day 0 of the nurture · personal email from the consultant", "segment": "Every quiet lead",
         "plain": True, "subject": "Did I catch you at a busy time?",
         "preview": "No pressure. Here are the three questions people ask me first.",
         "blocks": [
            {"t": "p", "text": "I tried to reach you about building with Mitchell, and I know life gets full. No pressure at all."},
            {"t": "p", "text": "In case it helps, here are the three questions people ask me first:"},
            {"t": "list", "items": [
                "Can my land be my down payment? If you own land, it can count toward the home.",
                "Do I need a construction loan? Not with Mitchell. We self-fund every build.",
                "Where do I start? Usually with a 15-minute call, at a time that works for you."]},
            {"t": "p", "text": "Just reply with a good time and I will call you then."}],
         "financing": True},
        {"id": "nu3", "send": "Day 5 · designed email", "segment": "Quiet leads who own land or have family land (nu3n for everyone else)",
         "subject": "What landowners ask us first",
         "preview": "Can my land be my down payment? Do I need a construction loan? Here are the answers.",
         "hero": hero("2024/8/14/10_iWQs7EE.jpg", "Aerial view of a Mitchell home in a green clearing surrounded by forest"),
         "eyebrow": "Building on your land", "headline": "Three answers for landowners",
         "blocks": [
            {"t": "covers", "items": [
                ["Can my land be my down payment?", "It can. With SimplyMitchell, the land you own counts toward the home, so there is zero down and zero closing costs."],
                ["Do I need a construction loan?", "No. Mitchell self-funds every build, so there is one closing, no draw period interest and no bank deciding whether your land counts."],
                ["What will it cost to build on my land?", "It depends on your plan, your selections and your site, including well, septic and clearing. A New Home Consultant can walk your land with you and put real numbers on it."]]},
            {"t": "video", "v": "wellseptic", "text": "What to know about a well and septic before you build on your land."},
            {"t": "cta", "text": "See What Your Land Can Build", "href": SMH + "/land"},
            {"t": "small", "text": "Want to go deeper? Watch Well and Septic on Behind the Build.", "href": "https://www.youtube.com/watch?v=zWwtw8qgp4w"}],
         "financing": True},
        {"id": "nu3n", "send": "Day 5 · designed email", "segment": "Quiet leads still looking for land, or land status unknown",
         "subject": "Before you buy land, check these six things",
         "preview": "What to know about a lot before you make an offer.",
         "hero": hero("2026/3/24/10_UuSAaPU.jpg", "Aerial view of a Mitchell home in a wooded valley below the mountains"),
         "eyebrow": "Building on your land", "headline": "Six things to check before you buy a lot",
         "blocks": [
            {"t": "covers", "items": [
                ["Soil and perc test", "Whether the ground supports a septic system, and what kind."],
                ["Water", "A well or a public connection, and what either costs."],
                ["Access and utilities", "Road frontage, the driveway, power and internet."],
                ["Easements and restrictions", "What is recorded on the deed, and any covenants."],
                ["Zoning and flood zone", "What can be built, and where on the lot."],
                ["Clearing and grading", "How much work the site needs before the build."]]},
            {"t": "p", "text": "We do not sell land, and we will not tell you where to buy. But you can start designing your home now and bring us the lot when you find it."},
            {"t": "video", "v": "land101", "text": "What to look for before you buy land to build on."},
            {"t": "cta", "text": "See How It Works", "href": SMH + "/no-land"},
            {"t": "small", "text": "Watch Purchasing Land 101 on Behind the Build.", "href": "https://www.youtube.com/watch?v=trgJ8maymOA"}]},
        {"id": "nu4", "send": "Day 12 · personal email from the consultant", "segment": "Every quiet lead",
         "plain": True, "subject": "What Lavonnia and Rick told us",
         "preview": "Two homeowners on what surprised them most.",
         "blocks": [
            {"t": "p", "text": "I wanted to share something one of our homeowner couples in Henrico said after they moved in:"},
            {"t": "p", "text": "\u201cTalk about no closing costs, no down payment, no construction loan. That's a big deal. I don't think we appreciated what that meant initially. Now looking back, we're like wow, that's the best choice we could've made to go with Mitchell.\u201d"},
            {"t": "p", "text": "Their story is short, if you would like to hear it in their own words:"},
            {"t": "link", "text": "Watch the Downey family's story", "href": "https://www.youtube.com/watch?v=9vmi-miQzKU"},
            {"t": "p", "text": "If you have questions about how it would work on your land, just reply."}],
         "financing": True},
        {"id": "nu6", "send": "Day 26 · designed email", "segment": "Every quiet lead",
         "subject": "When you are ready to make it yours",
         "preview": "Every Mitchell home starts with $5,000 in Design Dollars, up to $25,000.",
         "hero": hero("2023/2/6/Design_Center_13_IfaBRgj.jpg", "A kitchen display in a Mitchell Design Center with white cabinets, a copper hood and brass pendants"),
         "eyebrow": "Mitchell Design Dollars", "headline": "The finishes are where it becomes yours",
         "blocks": [
            {"t": "p", "text": "Cabinets, countertops, tile, the light over the table. The Design Center is where a plan turns into your home, and it is the part most people look forward to."},
            {"t": "p", "text": "Every Mitchell home now comes with $5,000 in Mitchell Design Dollars for those selections. Personalize more, and we add more, up to $25,000."},
            DD_BAND,
            {"t": "cta", "text": "See How Design Dollars Work", "href": DD}],
         "dd": True},
        {"id": "nu7", "send": "Day 35 · personal email from the consultant", "segment": "Every quiet lead",
         "plain": True, "subject": "Should I keep your file open?",
         "preview": "My last note for a while.",
         "blocks": [
            {"t": "p", "text": "I do not want to fill your inbox, so this is my last note for a while."},
            {"t": "p", "text": "If building is still on your list, reply yes and I will reach out at a time that works for you. If the timing is not right, reply later and I will check back in the spring."},
            {"t": "p", "text": "Either way, thank you for thinking of Mitchell."}]},
        {"id": "nu9", "send": "Day 60 · designed email, then the monthly newsletter", "segment": "Every quiet lead who has not replied",
         "subject": "Whenever you are ready",
         "preview": "Floor plans, the Home Portrait and a Design Center near you, all in one place.",
         "hero": hero("2026/3/3/ava_farmhouse-extended_sky.jpg", "A Mitchell farmhouse with a long front porch under an evening sky"),
         "eyebrow": "Mitchell Homes", "headline": "Whenever you are ready, we are here",
         "blocks": [
            {"t": "p", "text": "Building a home on your land is a big decision, and it is yours to make on your schedule. Here is everything in one place for when the time is right."},
            {"t": "list", "items": [
                "Browse more than 40 floor plans, from 1,000 to 3,000 square feet.",
                "Take the Home Portrait: eight questions, about 90 seconds.",
                "Visit a Design Center in Fredericksburg, Richmond, Newport News, Raleigh or Wilmington.",
                "Hear how it all works on Behind the Build, the podcast from Scott Sleeme and Deven Sellers."]},
            {"t": "video", "v": "roadmap", "text": "Every step from your first call to your keys, in one episode."},
            {"t": "cta", "text": "Take the Home Portrait", "href": QUIZ},
            {"t": "small", "text": "Browse the floor plans", "href": "https://www.mitchellhomesinc.com/new-homes/floorplans/"}]},
     ]},
]



# My Mitchell Story, the homeowner contest, lives in campaigns/homeowners/contest.json (make_contest.py); its emails
# join here as their own series so they render, preview and load into Builder Studio like the rest.
def _add_contest_series():
    import json, os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "homeowners", "contest.json")
    if not os.path.exists(path):
        return
    c = json.load(open(path))
    rec_path = os.path.join(os.path.dirname(path), "..", "builder_studio", "created.json")
    rsvp = next((v["field"] for v in json.load(open(rec_path)).get("links", {}).values() if v.get("event") == "e7"), None) if os.path.exists(rec_path) else None
    emails = []
    for e in c["emails"] + c["workflow_emails"]:
        e = json.loads(json.dumps(e).replace("[RSVP link]", rsvp)) if rsvp else dict(e)
        path_, alt = e.pop("hero_path", None), e.pop("hero_alt", "")
        if path_:
            e["hero"] = hero(path_, alt)
        short = {"hw1": "Automatic, when an entry arrives", "hw2": "Automatic, when an entry is verified",
                 "hw3": "About December 8, to each finalist", "hw4": "About December 8, to the winner"}.get(e["id"])
        if short:
            e["segment"] = (e.get("segment", "") + " " + e["send"] + ".").strip()
            e["send"] = short
        emails.append(e)
    launch = next((e for e in emails if e["id"] == "ho3"), None)
    if launch and not any(b["t"] == "video" for b in launch["blocks"]):
        i = next(i for i, b in enumerate(launch["blocks"]) if b["t"] == "cta")
        launch["blocks"].insert(i, {"t": "video", "v": "downey", "text": "Need an idea? This is how the Downey family told theirs."})
    SERIES.append({"key": "homeowners", "name": c["name"], "stage": "Homeowners", "campaign": "fall26_homeowners",
                   "reason": "You are receiving this email because you built your home with Mitchell Homes.",
                   "audience": "Past Mitchell homeowners. Contest emails after November 18 skip anyone who has already entered.",
                   "goal": " ".join(c["summary"]) if isinstance(c["summary"], list) else c["summary"],
                   "emails": emails})


_add_contest_series()

# Event invitations ride inside existing emails (campaigns/events/events.json), linked through the per event
# RSVP trigger links in Builder Studio (campaigns/builder_studio/created.json), so one link update fixes them all.
def _add_event_blocks():
    import json, os
    here = os.path.dirname(os.path.abspath(__file__))
    ev_path = os.path.join(here, "..", "events", "events.json")
    rec_path = os.path.join(here, "..", "builder_studio", "created.json")
    if not (os.path.exists(ev_path) and os.path.exists(rec_path)):
        return
    links = {v.get("event"): v["field"] for v in json.load(open(rec_path)).get("links", {}).values() if v.get("event")}
    by_id = {e["id"]: e for s in SERIES for e in s["emails"]}
    for ev in json.load(open(ev_path))["events"]:
        for r in ev.get("rides_in", []):
            em = by_id.get(r["email"])
            if em is None or any(b.get("event") == ev["id"] for b in em["blocks"]):
                continue
            b = r["block"]
            em["blocks"].append({"t": "event", "event": ev["id"], "eyebrow": "You are invited", "head": b["head"], "text": b["text"],
                                 "cta": b["cta"], "href": links.get(ev["id"], "[RSVP link]")})


_add_event_blocks()
