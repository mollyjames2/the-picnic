INTRO_TITLE = "The Picnic"
INTRO_SUBTITLE = "a story about a very good day"

# Scene 1 — picnic packing
SCENE_1_INTRO = "Sam: It's such a lovely day, we should go for a picnic!"

SCENE_1_ITEMS = {
    "onigiri":    "Onigiri! Definitely bringing these!",
    "strawberry": "Strawberries! These might survive the trip!",
    "suncream":   "Suncream! Feels optimistic, but okay!",
    "blanket":    "A picnic blanket is probably important for a picnic!",
    "bone":       "Maggie insists that this bone is essential picnic equipment!",
}

SCENE_1_MAGGIE_DIALOGUE = "Sam: Always in the way!"

SCENE_1_COMPLETE = "That should do it!"

# Scene 2 — leaving the house
SCENE_2_SAM_NICE_DAY = "Sam: It's too nice to stay inside today!"
SCENE_2_MOLLY_WHERE  = "Molly: Where should we go?"
SCENE_2_CHOICES      = [" - The beach", " - The woods", " - Somewhere with a view"]
SCENE_2_MOLLY_PLAN   = "Molly: Great shout! I know a good spot! C'mon let's go!"

# Scene 3 — the drive
SCENE_3_MOLLY_SUN      = "Molly: I'm so glad the sun's back!"
SCENE_3_SAM_BLOSSOMS   = "Sam: Hard to believe how long we've been here - remember when we first visited and the trees were full of blossoms?"
SCENE_3_MOLLY_QUESTION = "Molly: What's your favourite part of living here?"
SCENE_3_CHOICES        = ["The sea", "The town", "The house"]
# Keys match SCENE_3_CHOICES order and map to livingHereChoice values
SCENE_3_CHOICE_KEYS    = ["sea", "town", "house"]
SCENE_3_FOLLOWUP = {
    "sea":   "Molly: Hard to argue with waking up near the water - the river is so pretty!",
    "town":  "Molly: Dartmouth does have its charm....and its hills!",
    "house": "Molly: The house was a big step - glad I got to take it with you!",
}
SCENE_3_MOLLY_ARRIVED  = "Molly: OK we're here! perfect picnic location I reckon!"
SCENE_3_MAGGIE_BOOF    = "Maggie: Boof!"
SCENE_3_SAM_KNOWS      = "Sam: How does she always know when we've arrived?"
SCENE_3_MOLLY_MORON    = "Molly: She's pretty clever for a moron!"
SCENE_3_MAGGIE_LEGEND  = "Maggie: Pretty clever for an absolute legend!"
SCENE_3_MOLLY_ALRIGHT  = "Molly: Alright Mag!"

# Scene 4 — choosing the picnic spot
SCENE_4_INTRO_MOLLY         = "Molly: Right then! Let's find the perfect spot to set up!"
SCENE_4_INTRO_SAM           = "Sam: The whole place looks lovely. Let's have a proper look around first."
SCENE_4_INTRO_MAGGIE        = "Maggie: *Investigating a suspicious bush*"

# Tree — visited too early
SCENE_4_TREE_EARLY_MOLLY    = "Molly: Oh, this is really nice…"
SCENE_4_TREE_EARLY_SAM      = "Sam: Maybe we should check the other spots too, just in case?"

# Tree — final success
SCENE_4_TREE_SUCCESS_MOLLY  = "Molly: This is it. This is perfect."
SCENE_4_TREE_SUCCESS_SAM    = "Sam: Bit of shade, soft grass, nice view…"
SCENE_4_TREE_SUCCESS_MAGGIE = "Maggie: *immediately flops down*"
SCENE_4_TREE_SUCCESS_SAM_2  = "Sam: Yep. Definitely this one."

# Lake vignette
SCENE_4_LAKE_MOLLY          = "Molly: Being next to the water is so peaceful!"
SCENE_4_LAKE_MAGGIE         = "Maggie: Peaceful you say?......SPLASH!"
SCENE_4_LAKE_SAM            = "Sam: This is not going to be a relaxing picnic here!"
SCENE_4_LAKE_REPEAT         = "Maggie: Votes for swimming!"

# Sunny area vignette
SCENE_4_SUNNY_MOLLY         = "Molly: I do like the sun!"
SCENE_4_SUNNY_SAM           = "Sam: Too hot! Too hot! We're both far too pale for this!"
SCENE_4_SUNNY_REPEAT        = "Sam: No amount of suncream will ever be enough!"

# Flower patch vignette
SCENE_4_FLOWERS_MOLLY       = "Molly: Pretty!"
SCENE_4_FLOWERS_SAM         = "Sam: Maybe somewhere less pollen-heavy?"
SCENE_4_FLOWERS_REPEAT      = "Molly: Atchoo!"

# Scene 5 — picnic dialogue
SCENE_5_SAM_SPOT          = "Sam: This might be the best picnic spot yet!"

SCENE_5_HOUSE_QUESTION    = "Molly: It's perfect! Oh, I love living here with you! Do you remember when we first saw the house?"
SCENE_5_HOUSE_CHOICES     = [" - That was an impulsive day!", " - I liked that it was yellow!"]
SCENE_5_HOUSE_FOLLOWUP    = "Molly: We never weren't going to go for it!"

SCENE_5_HOME_QUESTION     = "Molly: I always wonder what it is that makes somewhere feel like home?"
SCENE_5_HOME_CHOICES      = [
    "- When it's quiet and comfortable",
    "- When it's full of little memories",
    "- When the right people are there",
]
SCENE_5_HOME_CHOICE_KEYS  = ["comfort", "memories", "people"]
SCENE_5_HOME_FOLLOWUP     = {
    "comfort":  "Molly: Yeah… I like that. Just feeling settled.",
    "memories": "Molly: They build up without you noticing, don't they?",
    "people":   "Molly: …yeah. That's probably it!",
}

SCENE_5_MIKE_MOLLY        = "Molly: Mike is definitely asleep somewhere right now!"
SCENE_5_MIKE_SAM          = "Sam: I doubt he cares we left him, he'll be sunbathing!"

SCENE_5_ADV_MOLLY_1       = "Molly: You know what's funny… I never remember trips the way I expect to!"
SCENE_5_ADV_SAM           = "Sam: What do you mean?"
SCENE_5_ADV_MOLLY_2       = "Molly: It's never the part I thought would matter most! What bit always sticks out to you?"
SCENE_5_ADV_CHOICES       = [
    "- The bit when you finally get there",
    "- All the stuff in between",
    "- Who you're with",
]
SCENE_5_ADV_CHOICE_KEYS   = ["destination", "journey", "together"]
SCENE_5_ADV_FOLLOWUP      = {
    "destination": (
        "Molly: Yeah… I do like that moment...",
        "When everything actually feels worth it!",
    ),
    "journey": (
        "Molly: That's where everything happens, isn't it?...",
        "All the little bits you don't plan!",
    ),
    "together": (
        "Molly: ...yeah!...",
        "I feel the same!",
    ),
}

# Scene 6 — proposal reveal
SCENE_6_SAM_WHAT   = "Sam: What's that?"
SCENE_6_MOLLY_OPEN = ("Molly: It's funny…",
                       "Today ended up answering things I didn't even know I was asking!")

SCENE_6_BEEN_THINKING = "I've been thinking about what you said earlier!"

# Maps stored choice keys → display text used in the speech
SCENE_6_LIVING_HERE_TEXT = {
    "sea":   "the sea",
    "town":  "the town",
    "house": "the house",
}
SCENE_6_HOME_TEXT = {
    "comfort":  "it being quiet and comfortable",
    "memories": "the little memories that build up",
    "people":   "the people",
}
SCENE_6_ADVENTURE_TEXT = {
    "destination": "that moment when you finally get there",
    "journey":     "all the stuff that happens in between",
    "together":    "who you share it with",
}

# Fallback text for isolated testing (any missing choice)
SCENE_6_LIVING_FALLBACK   = "the sea"
SCENE_6_HOME_FALLBACK     = "the people"
SCENE_6_ADVENTURE_FALLBACK = "who you share it with"

SCENE_6_CLOSING = (
    "I think… that's exactly why this all feels right!",
    "Being here... With you!",
    "I don't really need anything else figured out!",
    "So, I was hoping you'd keep sharing all of that with me....",
    "Forever?",
)

SCENE_6_PROPOSAL      = "Sam, will you marry me?"
SCENE_6_PRESS_ENTER   = "Press ENTER to continue the adventure"
SCENE_6_ENDING_LINE   = "The next adventure begins..."
SCENE_6_ENDING_TITLE  = "I love you!"


