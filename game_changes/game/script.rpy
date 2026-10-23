## ============================================================
## CTRL + THINK — Prototype Build
## An Interactive Visual Novel Exploring AI Dependency
## ============================================================
## Character art lives in game/images/characters/<name>/<expression>.png.
## Miguel, Myka, Sofia, Ethan, Angelica, and Alex (protagonist, split
## alex_f/alex_m by gender) each have a full expression set. Prof.
## Santos and the parents are still placeholder art.

# ---------------------------------------------------------
# CHARACTERS
# ---------------------------------------------------------
define narrator   = Character(None, what_italic=True)
define alex_v      = Character("[pname]", color="#8ab4f8")
define miguel     = Character("Miguel", color="#66bb6a")
define myka       = Character("Myka", color="#f7b733")
define sofia      = Character("Sofia", color="#4dd0e1")

# v167: drei sent a reference video (a Teams-style chat app) and asked for
# the texting scenes to move "like this" -- messages piling up in a real
# scrolling thread instead of each line wiping out the one before it.
# ChatCharacter records every line it says into _chat_history (a plain
# `default` list, so it saves/rolls-back correctly) the moment the say
# statement actually runs, once per line -- NOT inside the say screen
# itself, which redraws many times per statement and would otherwise
# duplicate every message on every redraw. The say screen (screens.rpy)
# then renders the whole history as a scrolling stack of bubbles instead
# of just the current line. _chat_history is reset to empty right after
# each `scene bg phone` in this file, so every phone scene starts its own
# fresh thread instead of carrying over the last one.
init python:
    class ChatCharacter(ADVCharacter):
        def __call__(self, what, *args, **kwargs):
            _chat_history.append((self.name, what))
            return ADVCharacter.__call__(self, what, *args, **kwargs)

    # v192: Christian flagged that in threads where more than one person
    # texts, the phone header kept flipping to whoever sent the latest
    # line ("Myka" then "Sofia"). Real group chats show the GC's own name
    # instead. Every phone scene now opens its thread with start_chat():
    # start_chat() for a one-on-one DM (header = that person's name, like
    # before), start_chat("Section 3A") for a group chat (header = GC name,
    # group avatar, sender names above bubbles).
    def start_chat(group=None):
        store._chat_history = []
        store._chat_group = group

    # Accent colour per texter (header avatar, sender-name label), and
    # which avatar art to use -- Myka/Sofia have their own, everyone else
    # (classmates, the player) falls back to the generic lavender one.
    CHAT_ACCENTS = {
        "Myka": "#f7b733",
        "Sofia": "#4dd0e1",
        "Classmate": "#a6e3a1",
        "Classmate 2": "#fab387",
    }

    def _chat_avatar_key(name):
        n = (name or "").lower()
        return n if n in ("myka", "sofia") else "generic"

default _chat_history = []
default _chat_group = None

# Group chat names used in the story.
define GC_CLASS   = "Section 3A"                 # the class GC (v227: no course shown -- Christian)
define GC_FRIENDS = "Future Pro Crammers"        # Alex/Myka/Sofia -- from Myka's "future professional crammers" line

define myka_text  = ChatCharacter("Myka (Text Message)", color="#f7b733")
define sofia_text = ChatCharacter("Sofia (Text Message)", color="#4dd0e1")
define classmate1_text = ChatCharacter("Classmate (Text Message)", color="#a6e3a1")
define classmate2_text = ChatCharacter("Classmate 2 (Text Message)", color="#fab387")
define prof       = Character("Prof. Santos", color="#b39ddb")
define parents    = Character("Mrs. De Guzman", color="#9e9e9e")

# ---------------------------------------------------------
# SPRITES
# ---------------------------------------------------------
# Miguel / Myka / Sofia / Ethan / Angelica each have a full
# expression set (images/characters/<name>/<expression>.png).
# "show <name> <expression>" picks the pose; "show <name>" alone
# falls back to neutral.

image miguel angry        = "images/characters/miguel/angry.png"
image miguel annoyed      = "images/characters/miguel/annoyed.png"
image miguel confused     = "images/characters/miguel/confused.png"
image miguel disappointed = "images/characters/miguel/disappointed.png"
image miguel excited      = "images/characters/miguel/excited.png"
image miguel happy        = "images/characters/miguel/happy.png"
image miguel happy_very   = "images/characters/miguel/happy_very.png"
image miguel neutral      = "images/characters/miguel/neutral.png"
image miguel sad          = "images/characters/miguel/sad.png"
image miguel shy          = "images/characters/miguel/shy.png"
image miguel surprised    = "images/characters/miguel/surprised.png"
image miguel              = "images/characters/miguel/neutral.png"

image myka angry        = "images/characters/myka/angry.png"
image myka annoyed      = "images/characters/myka/annoyed.png"
image myka confused     = "images/characters/myka/confused.png"
image myka disappointed = "images/characters/myka/disappointed.png"
image myka excited      = "images/characters/myka/excited.png"
image myka happy        = "images/characters/myka/happy.png"
image myka happy_very   = "images/characters/myka/happy_very.png"
image myka neutral      = "images/characters/myka/neutral.png"
image myka playful      = "images/characters/myka/playful.png"
image myka pleasant     = "images/characters/myka/pleasant.png"
image myka sad          = "images/characters/myka/sad.png"
image myka shy          = "images/characters/myka/shy.png"
image myka surprised    = "images/characters/myka/surprised.png"
image myka worried      = "images/characters/myka/worried.png"
image myka              = "images/characters/myka/neutral.png"

image sofia angry        = "images/characters/sofia/angry.png"
image sofia annoyed      = "images/characters/sofia/annoyed.png"
image sofia confused     = "images/characters/sofia/confused.png"
image sofia disappointed = "images/characters/sofia/disappointed.png"
image sofia excited      = "images/characters/sofia/excited.png"
image sofia happy        = "images/characters/sofia/happy.png"
image sofia happy_very   = "images/characters/sofia/happy_very.png"
image sofia neutral      = "images/characters/sofia/neutral.png"
image sofia sad          = "images/characters/sofia/sad.png"
image sofia shy          = "images/characters/sofia/shy.png"
image sofia surprised    = "images/characters/sofia/surprised.png"
image sofia worried      = "images/characters/sofia/worried.png"
image sofia              = "images/characters/sofia/neutral.png"

image ethan angry        = "images/characters/ethan/angry.png"
image ethan confused     = "images/characters/ethan/confused.png"
image ethan disappointed = "images/characters/ethan/disappointed.png"
image ethan excited      = "images/characters/ethan/excited.png"
image ethan happy        = "images/characters/ethan/happy.png"
image ethan happy_very   = "images/characters/ethan/happy_very.png"
image ethan neutral      = "images/characters/ethan/neutral.png"
image ethan sad          = "images/characters/ethan/sad.png"
image ethan shy          = "images/characters/ethan/shy.png"
image ethan surprised    = "images/characters/ethan/surprised.png"
image ethan worried      = "images/characters/ethan/worried.png"
image ethan              = "images/characters/ethan/neutral.png"

image angelica angry        = "images/characters/angelica/angry.png"
image angelica annoyed      = "images/characters/angelica/annoyed.png"
image angelica confused     = "images/characters/angelica/confused.png"
image angelica disappointed = "images/characters/angelica/disappointed.png"
image angelica excited      = "images/characters/angelica/excited.png"
image angelica happy        = "images/characters/angelica/happy.png"
image angelica happy_very   = "images/characters/angelica/happy_very.png"
image angelica neutral      = "images/characters/angelica/neutral.png"
image angelica sad          = "images/characters/angelica/sad.png"
image angelica shy          = "images/characters/angelica/shy.png"
image angelica surprised    = "images/characters/angelica/surprised.png"
image angelica worried      = "images/characters/angelica/worried.png"
image angelica              = "images/characters/angelica/neutral.png"

# Alex (protagonist) is gender-switched on top of the expression.
#
# v159: this used to be a ConditionSwitch() per pose -- Alex was the
# only character in the whole cast built that way, and also the only
# one showing the v156 half-body-crop "gap above the textbox" bug
# (floating well above the dialogue box instead of bleeding flush
# behind it, despite the cropped PNG itself having zero transparent
# padding at its bottom edge, confirmed by inspecting the file
# directly). Swapped ConditionSwitch for "[var]" bracket-substitution
# in the path -- drei tested it and the gap was still there, which
# rules out ConditionSwitch specifically but not "some kind of
# dynamically-resolved image" in general.
#
# v160 tried going further and registering "alex <expr>" as a truly
# static renpy.image() once gender was picked, so it would be no
# different from any other character's plain image -- that crashed
# ("Images may only be declared inside init blocks", since renpy.image()
# can't be called at runtime/from a label, only from init). Reverted
# that specific approach back to the bracket-substitution below (v161),
# which at least runs.
#
# Given BOTH of Ren'Py's supported "pick an image by a runtime
# condition" mechanisms (ConditionSwitch and this bracket-substitution)
# show the same gap, and a true static conversion isn't possible without
# rewriting every "show alex ..." call site in the script (50+ of them)
# to pick between two entirely separate image tags, Alex's image-
# resolution mechanism is very unlikely to be the real cause. Official
# Ren'Py docs also rule out the two engine-level theories we chased
# (chained transforms resetting xalign/yalign/zoom; zoom being applied
# after position when animated) -- neither is true per the docs. The
# floating gap is still UNRESOLVED as of v161; this build is a crash
# fix only. Leading remaining theory: a stale local Ren'Py cache on
# drei's machine still holding the old full-body sprite dimensions.
image alex angry        = "images/characters/[_alex_art]/angry.png"
image alex annoyed      = "images/characters/[_alex_art]/annoyed.png"
image alex confused     = "images/characters/[_alex_art]/confused.png"
image alex disappointed = "images/characters/[_alex_art]/disappointed.png"
image alex excited      = "images/characters/[_alex_art]/excited.png"
image alex happy        = "images/characters/[_alex_art]/happy.png"
image alex happy_very   = "images/characters/[_alex_art]/happy_very.png"
image alex neutral      = "images/characters/[_alex_art]/neutral.png"
image alex sad          = "images/characters/[_alex_art]/sad.png"
image alex shy          = "images/characters/[_alex_art]/shy.png"
image alex surprised    = "images/characters/[_alex_art]/surprised.png"
image alex worried      = "images/characters/[_alex_art]/worried.png"
image alex              = "images/characters/[_alex_art]/neutral.png"

image prof   = Transform("images/characters/prof_santos_sprite.png", zoom=2.0)   # v245: Dr. Liam art (drei: "dr liam is santos"); card_scale_* halves it
image parents = "images/characters/parents.png"

# ---------------------------------------------------------
# BACKGROUNDS
# ---------------------------------------------------------
image bg black     = Transform("images/backgrounds/black.png", xysize=(1280, 720))
image bg room      = Transform("images/backgrounds/room.jpg", xysize=(1280, 720))
image bg phone     = Transform("images/backgrounds/phone.png", xysize=(1280, 720))
image bg classroom = Transform("images/backgrounds/classroom.jpg", xysize=(1280, 720))
image bg hallway   = Transform("images/backgrounds/hallway.jpg", xysize=(1280, 720))
image bg night     = Transform("images/backgrounds/night.jpg", xysize=(1280, 720))
image bg street    = Transform("images/backgrounds/street.png", xysize=(1280, 720))
image bg canteen   = Transform("images/backgrounds/canteen.jpg", xysize=(1280, 720))
image bg library   = Transform("images/backgrounds/library.jpg", xysize=(1280, 720))
image bg art_room  = Transform("images/backgrounds/art_room.jpg", xysize=(1280, 720))

# ---------------------------------------------------------
# BACKGROUND MUSIC — mood shifts with the story's situation
# ---------------------------------------------------------
# v229: longer music (2-2.5 min instead of 42 s loops) -- Kevin MacLeod,
# incompetech.com, CC BY 4.0 (credited in About). Same file names.
define audio.bgm_menu     = "audio/bgm_menu.ogg"      # character select / menus
define audio.bgm_morning  = "audio/bgm_morning.ogg"   # calm daily-life school scenes
define audio.bgm_hub      = "audio/bgm_hub.ogg"       # free-day map exploration
define audio.bgm_tension  = "audio/bgm_tension.ogg"   # mounting pressure (group project, exam week)
define audio.bgm_night    = "audio/bgm_night.ogg"     # quiet unease, sleepless night
define audio.bgm_creative = "audio/bgm_creative.ogg"  # art elective, inspired mood
define audio.bgm_ending_a = "audio/bgm_ending_a.ogg"  # Route A — balanced, hopeful
define audio.bgm_ending_b = "audio/bgm_ending_b.ogg"  # Route B — bittersweet
define audio.bgm_ending_c = "audio/bgm_ending_c.ogg"  # Route C — heavy dependency

# ---------------------------------------------------------
# SOUND EFFECTS — subtle UI feedback (global, applies to every
# button in the game automatically) plus a phone notification
# chime used whenever a friend texts about an AI shortcut.
# ---------------------------------------------------------
define audio.sfx_notification = "audio/notification.ogg"

# ---------------------------------------------------------
# AMBIENT SOUNDSCAPE — a quiet background texture (birds + breeze
# by day, crickets + a softer breeze at dusk) layered under bgm_hub
# on the Free Day campus map only, tied to the same daypart index
# as the map's tint/lighting. Plays on its own "ambience" channel
# (registered in theme.rpy) so it fades in/out independently of
# whatever music track is playing.
# ---------------------------------------------------------
define audio.amb_day  = "audio/amb_day.ogg"   # birdsong + light breeze (morning/afternoon)
define audio.amb_dusk = "audio/amb_dusk.ogg"  # crickets + a softer night breeze (evening)

# NOTE: hover/activate sounds are applied via the "button" style below
# (config.hover_sound / config.activate_sound are not real Ren'Py
# variables — using them crashes the game on startup).
style button:
    hover_sound "audio/ui_hover.ogg"
    activate_sound "audio/ui_select.ogg"

# ---------------------------------------------------------
# GAME VARIABLES
# ---------------------------------------------------------
default dep_acads = 0
default dep_family = 0
default dep_mental = 0
default dep_creativity = 0
default c1_mood = None
default c1_puzzle = None

# Ending gallery tracking — persists across saves/restarts (unlike the
# dep_* stats, which reset each playthrough), since the point is to
# track your progress toward seeing all three endings over time.
default persistent.seen_route_a = False
default persistent.seen_route_b = False
default persistent.seen_route_c = False

# Free Day only gives the player time for a limited number of the
# four locations — forcing a real trade-off instead of letting them
# collect every stat effect for free. This is what makes the hub an
# actual choice instead of a checklist.
define FREE_DAY_MAX_SLOTS = 2
default free_day_slots_used = 0
default dependency_score = 0
default pname = "Alex"
default player_gender = "male"
default _alex_art = "alex_m"


# ---------------------------------------------------------
# CHARACTER SELECTION — male / female protagonist
# ---------------------------------------------------------
# v220: redesigned -- the two protagonists now stand in the stage's two
# spotlights (the art already has them) instead of sitting in square boxes.
# Hover one and they step forward, brighten and smile; the other dims.
define CHOOSE_CAST = [
    # (return value, name, art folder, accent, crop box, x centre)
    ("male",   "ALEX", "alex_m", "#cba6f7", (82, 0, 294, 605),   430),
    ("female", "AIRA", "alex_f", "#fab387", (15, 178, 398, 486), 850),
]

transform cs_figure(on, dim):
    easein 0.22 zoom (1.04 if on else 1.0) alpha (0.45 if dim else 1.0) matrixcolor BrightnessMatrix(0.05 if on else 0.0)

transform cs_rise(d=0.0):
    alpha 0.0 yoffset 18
    pause d
    easein 0.5 alpha 1.0 yoffset 0

transform cs_line(on):
    easein 0.2 xzoom (1.0 if on else 0.45)

screen choose_character():
    modal True
    zorder 400
    default cs_hover = None

    add Transform("images/backgrounds/character_select.png", xysize=(config.screen_width, config.screen_height))
    use ambient_particles(count=22, tint="#cba6f7")

    text "CHOOSE YOUR CHARACTER" size 30 color "#ece6f7" font "fonts/Orbitron-ExtraBold-static.ttf" kerning 2 xalign 0.5 ypos 44 at cs_rise(0.0)
    text "Your choices will shape how this story unfolds." size 17 color "#a9a3c3" xalign 0.5 ypos 92 at cs_rise(0.1)

    for _i, (_g, _nm, _art, _acc, _crop, _cx) in enumerate(CHOOSE_CAST):
        $ _on = cs_hover == _g
        $ _dim = cs_hover is not None and not _on
        $ _face = "happy_very" if _on else "happy"

        # the character, standing on the stage line (y=586)
        button:
            xpos _cx
            ypos 586
            xanchor 0.5
            yanchor 1.0
            xysize (330, 440)
            background None
            action Return(_g)
            hovered SetScreenVariable("cs_hover", _g)
            unhovered SetScreenVariable("cs_hover", None)
            at cs_rise(0.2 + _i * 0.12)
            add Transform(Crop(_crop, "images/characters/%s/%s.png" % (_art, _face)), fit="contain", xysize=(330, 440)) xalign 0.5 yalign 1.0 at cs_figure(_on, _dim)

        # name plate under the stage line
        vbox:
            xpos _cx
            xanchor 0.5
            ypos 604
            spacing 4
            at cs_rise(0.35 + _i * 0.12)
            text "PLAY AS" size 13 color ("#e8e2f5" if _on else "#8a84a6") font "fonts/Rajdhani-Bold.ttf" kerning 4 xalign 0.5
            text _nm size 34 color (_acc if not _dim else "#6b6785") font "fonts/Orbitron-ExtraBold-static.ttf" kerning 4 xalign 0.5
            add Solid(_acc) xysize (110, 3) xalign 0.5 at cs_line(_on)

    text "Click a character to begin" size 15 color "#7f7899" xalign 0.5 yalign 0.975 at cs_rise(0.6)

label choose_character_label:
    call screen choose_character
    $ player_gender = _return
    $ pname = "Aira" if player_gender == "female" else "Alex"
    $ _alex_art = "alex_f" if player_gender == "female" else "alex_m"
    $ chs_remember_player()
    return

# ---------------------------------------------------------
# START
# ---------------------------------------------------------
label start:

    # v193: the prologue now follows the script's "Intro" word for word
    # (it used to be an English paraphrase with an extra street scene).

    scene bg black
    with fade

    play music audio.bgm_menu fadein 1.5

    call choose_character_label from _call_choose_character_label

    # v257 (panel): open on a flash-forward of the worst case, then rewind.
    call v257_cold_open from _call_v257_cold_open

    show screen ambient_particles(count=16, tint="#cba6f7")

    narrator "Sa panahon ngayon, halos lahat ng impormasyon ay isang click lang ang layo."
    narrator "Assignments? May AI."
    narrator "Research? May AI."
    narrator "Presentations? May AI."
    narrator "Minsan nga pati simpleng pagbuo ng email o pag-iisip ng sagot sa discussion forum, AI na rin ang gumagawa."
    narrator "Hindi naman masama ang paggamit nito."
    narrator "Pero paano kung dumating sa punto na hindi mo na kayang gumawa ng kahit simpleng gawain nang wala ito?"

    hide screen ambient_particles
    scene bg black
    with fade
    "\"Nagsisimula ang lahat sa isang simpleng desisyon.\""

    scene bg room
    with fade
    play music audio.bgm_morning fadein 2.0

    # Script: "(Ang pangalan mo ay Alex.) - pipili na ung player ng name dito"
    $ pname = renpy.input("Ano ang pangalan mo?", default=pname).strip() or pname
    $ chs_remember_player()
    narrator "Ang pangalan mo ay [pname]."

    show alex neutral at center_alive, enter_center
    narrator "Isang ordinaryong college student na kasalukuyang nasa ikaapat na taon ng kolehiyo."
    narrator "Katulad ng karamihan, marami kang iniisip araw-araw."
    narrator "Deadlines. Projects. Quizzes. Group works."
    show alex worried at center_alive
    narrator "At ang pinakakinatatakutan ng lahat..."
    narrator "Mga requirements na sabay-sabay ang due date."
    narrator "Sa una, ginagawa mo naman ang lahat nang sarili mo."
    narrator "Pero habang tumatagal, mas dumarami ang gawain."
    narrator "Mas humihirap ang subjects. Mas kumakaunti ang oras."
    narrator "At doon mo unang nakilala ang isang bagay na tila magiging solusyon sa lahat ng problema mo."
    narrator "Artificial Intelligence."
    show alex neutral at center_alive
    narrator "Noong una, simpleng tulong lang."
    narrator "Pag-check ng grammar. Paghingi ng ideas. Pagpapaliwanag ng mahihirap na topics."
    narrator "Pero habang lumilipas ang mga buwan..."
    narrator "Napansin mong mas madalas mo na itong gamitin."
    narrator "Hanggang sa minsan..."
    show alex confused at center_alive, confused_tilt
    narrator "Hindi ka na nagsisimula hangga't wala muna itong sagot."
    narrator "Hindi ka na nag-iisip hangga't wala muna itong suggestion."
    narrator "Hindi mo na alam kung tulong pa ba ito..."
    narrator "O unti-unti ka nang umaasa rito."
    hide alex

    scene bg phone
    with dissolve
    $ start_chat(GC_FRIENDS)
    play sound audio.sfx_notification
    show screen ambient_particles(count=18, tint="#cba6f7")

    myka_text "Uy [pname], nakita mo na ba yung bagong AI update? Sobrang galing. Kaya na niyang gawin halos lahat."

    play sound audio.sfx_notification
    sofia_text "Good morning! Huwag mong kalimutan yung reflection paper natin. Due mamayang hapon."

    hide screen ambient_particles
    scene bg room
    with dissolve

    show alex surprised at center_alive, surprised_jump
    narrator "Reflection Paper."
    narrator "Today."
    narrator "Due mamayang hapon."
    narrator "At wala ka pang nasisimulan."
    hide alex

    scene bg black
    with fade
    show screen ambient_particles(count=16, tint="#cba6f7")
    narrator "At dito nagsisimula ang kwento mo."
    narrator "Ang bawat desisyong gagawin mo ay makaaapekto sa paraan ng iyong pag-aaral, pakikitungo sa iba, at pagtingin sa sarili."
    narrator "Gagamitin mo ba ang AI bilang kasangkapan lamang?"
    narrator "O hahayaan mong ito ang mag-isip para sa iyo?"
    narrator "The story begins..."

    hide screen ambient_particles
    jump chapter1


# ============================================================
# CHAPTER 1 — Umagang Magulo (from the new script — Scene 1: House, Scene 2: School Entrance)
# ============================================================
label chapter1:

    call show_chapter_card("CHAPTER 1", "Morning Chaos") from _call_show_chapter_card_1
    $ _loc4 = pname + "'s Room"

    scene bg room
    with fade

    call show_scene_caption("1", _loc4, "Morning", "room") from _call_show_scene_caption_6

    play music audio.bgm_morning fadein 2.0

    narrator "Minsan hindi naman nagsisimula ang problema sa malaking pagkakamali."
    narrator "Minsan..."
    narrator "Nagsisimula ito sa isang simpleng desisyon."
    narrator "Isang maliit na shortcut."
    narrator "Isang beses na pagsabi ng..."
    narrator "\"Okay lang siguro. Ngayon lang naman.\""
    narrator "Madilim pa yung room. Sobrang tahimik ng buong bahay."

    "BEEP! BEEP! BEEP!"

    alex_v "{i}...{/i}"
    alex_v "{i}...{/i}"
    alex_v "{i}Five minutes pa.{/i}"
    narrator "Pinindot mo yung snooze, tapos hinila mo ulit yung kumot over your head."

    show alex sad at center_alive, enter_center
    "BEEP!"

    show alex annoyed at center_alive, defeated_tilt
    alex_v "Bwiset..."
    narrator "Napaupo ka sa kama. You check your phone, half-open pa yung mata mo."

    narrator "6:12 AM."
    narrator "Thursday."
    narrator "Midterms Week."
    narrator "17 unread notifications. 8 messages. 3 emails. 2 missed calls."
    narrator "And one message from the professor."
    alex_v "{i}Bakit may message si Sir nang ganito kaaga?{/i}"

    alex_v "...Ayoko na."

    scene bg phone
    with dissolve
    $ start_chat(GC_CLASS)
    play sound audio.sfx_notification
    show screen ambient_particles(count=14, tint="#cba6f7")

    myka_text "GUYS NAG ANNOUNCE SI MA'AM"
    myka_text "CHECK NIYO EMAIL"
    classmate1_text "May submission daw today?!"
    classmate2_text "Kala ko next week pa"

    prof "\"Reminder: Individual Reflection Paper (2000 words) due today, 5:00 PM.\""
    prof "\"No extensions will be entertained.\""

    # v175: this whole reaction (show alex ... alex_v "Reflection paper?"
    # etc.) used to play BEFORE the scene cut back from the phone-chat
    # visual to the room -- Alex was shown standing over the raw "bg
    # phone" background (a dark screen-OFF bezel photo, meant to only
    # ever be lit up by the phone-chat screen's own ambient_particles
    # overlay, per the comment on screen say() at the top of screens.rpy)
    # instead of her actual room. Drei sent a screenshot of exactly this:
    # "Aira" reacting in person against a plain dark background. Fixed by
    # cutting back to the room (and dropping the phone's ambient_particles
    # overlay) right after the last phone message, before Alex is shown
    # reacting in person, instead of after.
    hide screen ambient_particles
    scene bg room
    with dissolve

    show alex confused at center_alive, enter_center
    alex_v "Reflection paper?"
    alex_v "Today?"
    show alex confused at center_alive, confused_tilt
    alex_v "Wait..."
    show alex surprised at center_alive, panicked_flip
    alex_v "AKALA KO NEXT WEEK PA TO!"
    hide alex

    narrator "Books scattered. Open notebooks. Half-finished assignments. Coffee cups."
    narrator "One cup still has last night's coffee in it. Cold now."
    narrator "A room that clearly belongs to a stressed college student."
    narrator "College wasn't supposed to be this hard. At least that's what everyone said before entering university."
    narrator "But reality was different. Deadlines. Projects. Research papers. Presentations."
    narrator "Groupmates who disappear. Professors who assign three activities in one day."
    narrator "And the constant pressure of trying not to fail."
    alex_v "{i}2000 words. Wala pa akong kahit isang sentence.{/i}"

    show alex worried at center_alive, scared_shake
    alex_v "Okay... kailangan ko na maghanap ng gamit ko bago pa ako ma-late."

    call play_morning_chaos from _call_play_morning_chaos

    # The line here used to be the same no matter how the search went —
    # even a full timeout with half the items left behind still got
    # "at least I'm not late," which undercuts the whole point of racing
    # a clock. Branch it on the actual result instead.
    if _chaos_result >= len(MORNING_CHAOS_ITEM_INFO):
        alex_v "Okay..."
        alex_v "At least hindi ako late."
        narrator "Complete na lahat ng gamit. Medyo nakahinga ka habang sinusuot yung bag."
    elif _chaos_result >= 3:
        alex_v "Okay, kulang pa nga pero sige na."
        alex_v "Baka konting late lang."
    else:
        alex_v "Ugh, wala na akong oras maghanap pa."
        alex_v "Ma-late na naman ako."
        narrator "Ni-grab mo agad yung bag kahit kulang pa yung laman."

    scene bg phone
    with dissolve
    $ start_chat()
    play sound audio.sfx_notification
    sofia_text "Good morning, sleepyhead."
    sofia_text "Alive ka pa ba?"

    # v255: the reply choice was removed (drei / Christian)

    hide alex

    call show_scene_caption("2", "Campus Gate", "Morning", "campus_gate_morning") from _call_show_scene_caption_7

    scene bg campus_gate_morning
    with fade

    narrator "Students rushing. Some reviewing notes. Some cramming. Some pretending they studied."
    narrator "Busina ng jeep sa labas, tawanan, tapos sunod-sunod na yabag papasok ng campus."
    alex_v "{i}Everyone looks like they know what they're doing. Ako lang yata yung hindi.{/i}"

    show sofia happy at center_alive, enter_center
    sofia "Uy!"
    narrator "She waves enthusiastically."
    sofia "Mukha kang nakipag-away sa kama."

    show alex sad at left_alive
    show sofia happy at right_alive
    alex_v "Mas malala."
    sofia "Ano?"
    alex_v "Sakit na ng ulo dahil sa midterm na yan."
    narrator "Sofia laughs."
    sofia "Midterms week lang yan."
    alex_v "Ayun na nga eh, basta bahala na."
    alex_v "{i}Honestly, hindi ko pa alam paano ko sisimulan yung paper.{/i}"

    narrator "As they walk toward the building..."
    narrator "Someone suddenly appears behind them."

    show expression Solid("#0a081280", xysize=(config.screen_width, config.screen_height)) as trio_dim
    hide alex
    hide sofia
    show alex neutral at left_trio
    show sofia neutral at right_trio
    show myka happy_very at center_trio_jiggle
    myka "GOOD MORNING MGA FUTURE PROFESSIONAL CRAMMERS!"
    sofia "Ayan na."
    alex_v "Nurse, gising na siya."
    myka "Guys relax."
    myka "Wala nang impossible ngayon."
    narrator "Myka raises her phone proudly."
    myka "Ayan oh, one click lang to."
    myka "Essay? Reflection? Research?"
    myka "One click lang yan dito HAHAHA."
    show sofia annoyed at right_trio_huff
    sofia "Myka!!"
    show myka playful at center_trio_jiggle
    myka "What? Minsan lang naman e."
    sofia "That's not healthy."
    show myka worried at center_trio
    myka "Hindi healthy ang puyat at stress."
    narrator "Hindi ka sumagot. Pero napatingin ka sa phone ni Myka nang mas matagal than you should."

    hide trio_dim
    hide alex
    hide myka
    hide sofia

    call show_scene_caption("3", "Classroom", "Morning", "classroom") from _call_show_scene_caption_8

    scene bg classroom
    with fade

    narrator "Professor Santos enters. The room immediately becomes quiet."
    narrator "Yung hum na lang ng aircon ang naririnig. Amoy freshly printed paper yung buong room."
    show prof at center_alive, enter_center, card_scale_center
    prof "Good morning."
    narrator "Nobody responds."
    prof "I said... good morning."
    narrator "Class: \"GOOD MORNING SIR!\""
    prof "Better."
    narrator "He places a stack of papers on the table."
    prof "Before we start, I want to ask something."
    prof "Ngayon palang, sino sa inyo ang gumamit ng AI?"
    narrator "Walang nagtaas ng kamay."
    narrator "Nagkatinginan yung iba. Some phones quietly disappear sa ilalim ng desk."
    prof "Ahh, talaga lang ha."
    narrator "He writes on the board: TOOL. ASSISTANT. REPLACEMENT."
    narrator "Isinulat niya yung last word nang mas madiin kaysa sa iba."
    prof "There's a difference."
    narrator "The room becomes silent."
    prof "Technology becomes dangerous when you stop thinking and start depending."
    # v257 (panel): the reasons behind the rule, and what it cost someone.
    call v257_ch1_reasons from _call_v257_ch1_reasons
    hide prof

    show expression Solid("#0a081280", xysize=(config.screen_width, config.screen_height)) as trio_dim
    show alex neutral at left_trio, enter_left
    show myka playful at right_trio, enter_right
    myka "{i}(whispers) Boomer take.{/i}"
    show sofia annoyed at center_trio, enter_center
    sofia "Shhh."
    narrator "Napangiti ka nang konti. Pero yung three words sa board, hindi mo maalis sa isip."

    hide trio_dim
    hide alex
    hide myka
    hide sofia

    call show_scene_caption("4", "Lunch Break", "Afternoon", "garden_day") from _call_show_scene_caption_9

    scene bg garden_day
    with fade

    narrator "The protagonist sits alone under a tree."
    narrator "Leaves rustle overhead. The smell of cut grass and canteen food drifts over."
    narrator "Everyone around seems busy. Studying. Talking. Preparing for deadlines."
    alex_v "{i}Everyone's busy. Ako, nakatitig lang sa blank document.{/i}"

    play sound audio.sfx_notification
    narrator "(Phone vibrates again.)"
    ai_notif "Need help writing your reflection paper?"
    ai_notif "Generate instantly with AI."
    narrator "You stare at the notification for a while. Hindi mo binuksan. Hindi mo rin dinismiss."

    show alex annoyed at center_alive, enter_center
    alex_v "{i}Grabe, kahit yung phone ko sinusubukan din akong i-convince.{/i}"
    narrator "Binalik mo yung phone sa bulsa. Ramdam mo pa rin yung bigat nito."

    narrator "Habang naghihintay ka, biglang lumapit si Prof. Santos na may dalang simpleng logic puzzle para sa buong klase."
    narrator "\"Three switches control three light bulbs in another room. How can you identify which switch controls which bulb if you can only enter the room once?\""

    menu:
        "Paano mo sasagutin ang puzzle?"

        # Script, Mini Game 2 "Critical Thinking Challenge" hidden
        # score: A = +10 Dependency, B = 0, C = +5.
        "A. Ask AI immediately.":
            $ dep_acads += 10
            $ c1_puzzle = "ai"
            alex_v "Mabilis lang naman kung AI agad ang tatanungin ko."
            narrator "Halos automatic na yung thumb mo papunta sa app."

        "B. Try solving it first.":
            $ c1_puzzle = "self"
            alex_v "Hayaan mo, subukan ko munang isipin."
            narrator "Hindi mo nilabas yung phone. You take a deep breath muna."

        "C. Ask classmates.":
            $ dep_acads += 5
            $ c1_puzzle = "classmates"
            alex_v "Baka may makatulong sa mga kaklase, subukan ko munang magtanong."
            narrator "Tumayo ka tapos hinanap mo sina Sofia at Myka."

    # v239: the puzzle gets an answer (no score change)
    call ch1_puzzle_reveal from _call_ch1_puzzle_reveal

    hide alex

    scene bg black
    with fade

    $ renpy.notify("Tip: check Phone > Stats anytime to see your dependency meter.")

    call fc_after_chapter(1) from _call_fc_after_chapter
    jump chapter2


# ============================================================
# FREE DAY — Campus Map Hub
# ============================================================
label free_day:

    call show_chapter_card("FREE DAY", "Choose a Destination") from _call_show_chapter_card_2

    play music audio.bgm_hub fadein 2.0

    $ map_visited = {"room": False, "library": False, "canteen": False, "creative": False}
    $ free_day_slots_used = 0

label free_day_loop:

    scene bg black
    with dissolve

    call screen campus_map
    $ _map_dest = _return

    if _map_dest == "done":
        jump free_day_end

    if map_visited.get(_map_dest):
        $ renpy.notify("Already did this today.")
        jump free_day_loop

    if free_day_slots_used >= FREE_DAY_MAX_SLOTS:
        $ renpy.notify("Out of time today — you can only visit {} places.".format(FREE_DAY_MAX_SLOTS))
        jump free_day_loop

    if _map_dest == "room":
        call map_scene_room from _call_map_scene_room
    elif _map_dest == "library":
        call map_scene_library from _call_map_scene_library
    elif _map_dest == "canteen":
        call map_scene_canteen from _call_map_scene_canteen
    elif _map_dest == "creative":
        call map_scene_creative from _call_map_scene_creative
    elif _map_dest == "garden":
        call map_scene_garden from _call_map_scene_garden
    elif _map_dest == "netcafe":
        call map_scene_netcafe from _call_map_scene_netcafe
    elif _map_dest == "lab":
        call map_scene_lab from _call_map_scene_lab

    $ map_visited[_map_dest] = True
    $ free_day_slots_used += 1
    jump free_day_loop


label free_day_end:
    scene bg black
    with fade
    narrator "After a chill Saturday, you got ready again for the next challenges of the week."
    narrator "The bag is packed again. The phone charges face-down on the desk."
    alex_v "{i}One week na lang. Kaya ko 'to... siguro.{/i}"

    # v193: Free Day is the weekend between the final presentation
    # (end of Ch5) and the last week of the semester (Ch6: "Lumipas ang
    # ilang araw mula nang kanilang final presentation").
    # v239: the last free week (and Group Night) before Chapter 6
    call cl_break(4) from _call_cl_break
    jump chapter6


# ---------- Free Day location: Kwarto (Mental Well-Being) ----------
label map_scene_room:
    scene bg room
    with fade

    $ _loc5 = pname + "'s Room"
    call show_scene_caption(str(free_day_slots_used + 1), _loc5, "Weekend", "room") from _call_show_scene_caption_10

    show alex neutral at center_alive, enter_center
    narrator "A rare bit of free time. No deadline you need to worry about this minute."
    narrator "The house is quiet. Just the electric fan humming and a tricycle passing outside."
    alex_v "What should I do now? Maybe I could write down what I'm really feeling this week."

    menu:
        "What will you do with your free time?"

        "Journal about what happened this week — in your own words.":
            $ dep_mental += 5
            narrator "You wrote down your thoughts, messy as they were. You feel lighter afterward."
            narrator "The handwriting is uneven, crossed out in places. But every word is yours."

        "Just ask AI how to 'manage' your stress.":
            $ dep_mental += 15
            narrator "AI gave you a list of tips. They're good, pero parang hindi rin nagbago ang tunay mong nararamdaman."
            alex_v "{i}I've read so many tips. Pero bakit parang hindi ko pa rin pinakinggan yung sarili ko?{/i}"

    hide alex
    with dissolve
    return


# ---------- Free Day location: Aklatan (Academics) ----------
label map_scene_library:
    scene bg library
    with fade

    call show_scene_caption(str(free_day_slots_used + 1), "Library", "Weekend", "library") from _call_show_scene_caption_11

    show sofia happy at center_alive, enter_center
    narrator "You find Sofia in a quiet corner, surrounded by books."
    narrator "It smells like old paper and floor wax. The aircon hums somewhere above the shelves."
    sofia "Hey! Turns out I'm also getting a head start studying here. Want to join?"
    sofia "Fair warning — your phone's probably going to blow up with notifications. Good luck ignoring them."
    hide sofia

    call play_focus_mode from _call_play_focus_mode_1
    $ _resisted, _gave_in = _focus_result

    scene bg library
    with dissolve
    show sofia neutral at center_alive, enter_center

    if _resisted >= 5:
        $ dep_acads += 4
        $ dep_mental += 6
        show sofia happy_very at center_alive, happy_jiggle
        sofia "Wow, you really didn't touch your phone once. Ang galing mo talaga mag-focus."
        narrator "You got through the material clean — no shortcuts, no distractions. It actually felt good."
        narrator "Sofia slides a highlighter across the table without a word. You both keep going."
    elif _resisted >= 3:
        $ dep_acads += 8
        $ dep_mental += 2
        show sofia happy at center_alive
        sofia "Medyo nadistract ka rin, pero okay lang — at least natapos mo."
        narrator "A few notifications got the better of you, but you still pushed through most of it yourself."
    else:
        $ dep_acads += 14
        $ dep_mental += 10
        show sofia disappointed at center_alive, annoyed_huff
        sofia "Grabe, parang ang dami mong pinindot na notifications."
        narrator "By the end, you'd clicked into almost every shortcut that popped up. The reading barely happened."
        alex_v "{i}I came here para mag-aral. Bakit parang notifications lang yung nabasa ko?{/i}"

    hide sofia
    with dissolve
    return


# ---------- Free Day location: Kantina (Family/Friendship) ----------
label map_scene_canteen:
    scene bg canteen
    with fade

    call show_scene_caption(str(free_day_slots_used + 1), "Canteen", "Weekend", "canteen") from _call_show_scene_caption_12

    show myka happy at center_alive, enter_center
    narrator "You find Myka at the canteen, sitting alone, focused on her phone."
    narrator "The canteen is half-empty on a weekend. Plastic chairs, the smell of fried rice, a TV nobody's watching."
    myka "Hey! Want to eat together?"
    show alex neutral at left_alive
    show myka happy at right_alive
    alex_v "Sure, i-set ko lang phone ko sa silent."
    narrator "Pinindot mo yung side button hanggang mag-silent, tapos tinaob mo yung phone sa table."

    narrator "Habang kumakain, sinimulan ni Myka ikwento ang linggo niya."
    show myka worried at right_alive, defeated_tilt
    myka "Grabe, ang hirap ng requirements this week — three papers due pareho ng deadline."
    myka "Kaya nga hindi ako nakatulog nang maayos, puyat na puyat ako."
    myka "Pero buti na lang may Free Day tayo ngayon — sobrang kailangan ko na rin talaga ng break, lalo na kasama ka."
    hide alex
    hide myka
    with dissolve

    narrator "Sandaling nawala si Myka para bumili ng inumin. Habang naghihintay, sinubukan mong alalahanin ang mga sinabi niya."

    $ _listen_correct = 0

    menu:
        "Ano ang dahilan kung bakit puyat si Myka?"

        "Kasi three papers ang deadline niya sa parehong araw.":
            $ _listen_correct += 1
            narrator "Tama."

        "Kasi may kinakabahan siyang exam.":
            narrator "Hindi — mali ang naalala mo."

    menu:
        "Ano ang sinabi niya tungkol sa Free Day na ito?"

        "Kailangan niya rin ng break, lalo na kasama ka.":
            $ _listen_correct += 1
            narrator "Tama."

        "Gusto niya lang mag-shopping.":
            narrator "Hindi — mali ang naalala mo."

    show myka neutral at center_alive, enter_center

    if _listen_correct >= 2:
        $ dep_family += 4
        show myka happy_very at center_alive, happy_jiggle
        myka "Uy, ang galing mo pala makinig ha. Di ko akalain na naaalala mo pa lahat ng sinabi ko."
        narrator "You put the phone down completely this time. It's a small thing, but Myka noticed."
        narrator "Myka keeps talking, hands moving as she tells the story. The food goes cold, and neither of you minds."
    elif _listen_correct == 1:
        $ dep_family += 9
        show myka pleasant at center_alive
        myka "Sige lang, medyo distracted ka lang siguro. Okay lang yun."
        narrator "You got some of it, but a few details slipped past you while your mind wandered."
    else:
        $ dep_family += 14
        show myka disappointed at center_alive, defeated_tilt
        myka "Parang wala ka masyadong naalala sa kwento ko, ah."
        narrator "You realize you were nodding along without actually taking any of it in — your attention had already wandered somewhere else."
        alex_v "{i}She's right here sa harap ko. Bakit nasa iba yung isip ko?{/i}"

    hide myka
    with dissolve
    return


# ---------- Free Day location: Art Room (Creativity) ----------
label map_scene_creative:
    scene bg art_room
    with fade

    call show_scene_caption(str(free_day_slots_used + 1), "Art Room", "Weekend", "art_room") from _call_show_scene_caption_13

    show alex neutral at center_alive, enter_center
    narrator "You spot your old sketchbook, untouched for a while under your books."
    narrator "You turn the pages. Mga lumang drawing, karamihan unfinished."
    alex_v "I kinda want to draw again... but it's been so long since I last tried."
    alex_v "Maybe I'll start small — just try to remember a pattern, see if my hand still listens to me."
    hide alex

    call play_pattern_memory from _call_play_pattern_memory_1
    $ _pattern_score = _pattern_result

    scene bg art_room
    with dissolve
    show alex neutral at center_alive, enter_center

    if _pattern_score >= 4:
        $ dep_creativity += 4
        show alex happy at center_alive, proud_scaleup
        alex_v "Okay... hindi pa pala ako nawawalan ng touch."
        narrator "Your hand remembered more than you expected. You open the sketchbook and actually start drawing — kahit magaspang pa ang resulta."
        narrator "The pencil scratches softly across the page. It's the only sound in the room."
    elif _pattern_score >= 2:
        $ dep_creativity += 9
        narrator "You got some of it right, some of it not. Close enough — you pick up the pencil anyway, half out of stubbornness."
    else:
        $ dep_creativity += 15
        show alex disappointed at center_alive, defeated_tilt
        alex_v "Ang tagal na talaga... baka mas mabilis na lang kung AI gagawa nito."
        narrator "You found some beautiful images from an AI generator instead. But afterward, you never opened your sketchbook again."

    hide alex
    with dissolve
    return


# Chapters 2-6 now live in story_ch2.rpy ... story_ch6.rpy, ported
# scene by scene from Christian's script (v193). The old placeholder
# chapters (Group Project / Art Elective / Sleepless Night / Finals Week)
# were replaced by the script's own story; a copy of the old file is
# kept outside the game folder.


# ============================================================
# ROUTE EVALUATION
# ============================================================
label evaluate_route:

    scene bg black
    with fade
    stop music fadeout 1.5
    show screen ambient_particles(count=30, tint="#cba6f7")

    narrator "Based on the decisions you made throughout the story..."
    $ renpy.pause(1.5)
    hide screen ambient_particles

    # v193 (script port): the script scores a hidden Dependency number
    # (Mini Games 2-5, AI hints, the Free Day choices, the final choice)
    # plus a separate Critical Thinking number for puzzles solved on
    # your own. Dependency is still recorded per category (Academics,
    # Family/Friendship, Mental Well-Being, Creativity) for the Stats
    # app and the ending breakdown; the route uses the total minus
    # Critical Thinking, scaled to 0-100 for display.
    python:
        _dep_total = dep_acads + dep_family + dep_mental + dep_creativity
        _route_raw = _dep_total - crit_thinking
        dependency_score = max(0, min(100, int(round(_route_raw * 100.0 / 120.0))))

    # The script's own ending is the MC choosing to start on his own,
    # so Route A needs that final choice; choosing AI at the very end
    # can at best land on Route B.
    if final_choice != "ai" and dependency_score <= 33:
        jump ending_route_a
    elif final_choice != "ai" or dependency_score <= 66:
        jump ending_route_b
    else:
        jump ending_route_c


# ---------- ROUTE A: BALANCED USE ----------
label ending_route_a:
    $ persistent.seen_route_a = True
    call show_chapter_card("ROUTE A", "Balanced Use") from _call_show_chapter_card_3

    play music audio.bgm_ending_a fadein 2.5

    # The script's own ending (Ch6 Scene 4, after "[START ON YOUR OWN]"),
    # ported verbatim in story_ch6.rpy.
    call ch6_script_ending from _call_ch6_script_ending

    call show_ending_summary("ROUTE A", "Balanced Use", "Responsible use of AI strengthened — not weakened — your ability as a student. This is the whole point of the game: use technology as a tool, not as a replacement for your own thinking.", dependency_score, dep_acads, dep_family, dep_mental, dep_creativity) from _call_show_ending_summary

    jump the_end


# ---------- ROUTE B: MODERATE DEPENDENCY ----------
label ending_route_b:
    $ persistent.seen_route_b = True
    call show_chapter_card("ROUTE B", "Moderate Dependency") from _call_show_chapter_card_4

    play music audio.bgm_ending_b fadein 2.5

    scene bg classroom
    with dissolve
    narrator "As the weeks passed, your decisions were a mixed bag — sometimes you thought things through yourself, sometimes you leaned on AI."
    narrator "You noticed a gradual gap forming in your skills. A few teachers started asking questions about the originality of your work."

    scene bg hallway
    with dissolve
    show alex worried at left_alive, enter_left
    show miguel neutral at right_alive, enter_right
    miguel "[pname], there's nothing wrong with asking for help, but make sure you're still the one making the decisions."
    alex_v "I know naman... I think I really need to cut back on how much I lean on it."
    narrator "You nodded, not entirely convinced by your own words. But at least, you know where to start."
    hide alex
    hide miguel

    call show_ending_summary("ROUTE B", "Moderate na Pag-asa sa AI", "Even light dependency on AI, when repeated often enough, slowly weakens your independence in thinking. It needs regular self-check before it gets worse.", dependency_score, dep_acads, dep_family, dep_mental, dep_creativity) from _call_show_ending_summary_1

    jump the_end


# ---------- ROUTE C: HIGH DEPENDENCY ----------
label ending_route_c:
    $ persistent.seen_route_c = True
    call show_chapter_card("ROUTE C", "High Dependency") from _call_show_chapter_card_5

    play music audio.bgm_ending_c fadein 2.5

    scene bg night
    with dissolve
    narrator "You'd been leaning on AI for almost all of your academic work for a while now."
    narrator "One day, you got called to the disciplinary office — there's an issue about the originality of what you submitted."

    scene bg room
    with dissolve
    show alex sad at left_alive, enter_left
    show parents at right_alive, enter_right, card_scale_side
    parents "Anak... how did this happen? We thought you could handle this."
    alex_v "I can naman... I guess I just got used to it being easier when someone — something — else did it for me."
    hide parents
    hide alex
    with dissolve
    narrator "For the first time, you felt real anxiety and a loss of confidence in your own ability."
    narrator "Sitting alone in your room, you wonder: when was the last time you did something without asking AI for help?"
    narrator "You can't quite remember."

    call show_ending_summary("ROUTE C", "High na Pag-asa sa AI", "Relying too heavily on AI for everything can result in cognitive inertia, academic penalties, burnout, and a loss of self-confidence. Balance matters — a lot.", dependency_score, dep_acads, dep_family, dep_mental, dep_creativity) from _call_show_ending_summary_2

    jump the_end


# ============================================================
# END OF PROTOTYPE
# ============================================================
label the_end:
    scene bg black
    with fade
    # v227: the ending song used to be cut off and swapped for the menu
    # music the moment The End appeared. Now it keeps playing under The
    # End and fades out gently when you leave.
    call v241_finale from _call_v241_finale
    call screen the_end_screen
    return
