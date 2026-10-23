## ============================================================
## v241 PROGRESS: choice FLOWCHART, story ACHIEVEMENTS, TROPHY
## ROOM, COMPLETION % and the EXTRAS menu.
##
## Everything is read from variables the story already sets, so no
## line of Christian's script had to change. The only additions to
## his files are one-line `call`s at chapter ends (flowchart) and in
## the_end (epilogue / wrapped / credits).
## Nothing here changes the dependency score or the endings.
## ============================================================

default persistent.fc_seen = set()       # "node:option" found in any playthrough
default persistent.story_ach = set()
default fc_ending = None                  # "A"/"B"/"C" for this playthrough
default fc_new = set()                    # paths discovered for the first time this run
default temptations = {"total": 0, "resisted": 0}

init python:
    def _gv(name, default=None):
        return getattr(store, name, default)

    # ------------------------------------------------ flowchart model
    # (chapter, title, [(node id, question, [(option id, label)])])
    FC_CHAPTERS = [
        (1, "Morning Chaos", [
            ("mg_room", "Morning Chaos", [("clean", "Found everything, no AI"), ("hint", "Used AI hints"), ("partial", "Left things behind")]),
            ("c1_puzzle", "The three-switch puzzle", [("self", "Figured it out yourself"), ("classmates", "Asked classmates"), ("ai", "Asked AI")]),
        ]),
        (2, "The Blank Page", [
            ("c2_notif", "The AI notification", [("swipe", "Swiped it away"), ("later", "Left it for later")]),
            ("mg_reflection", "Idea Match", [("alone", "Matched it yourself"), ("hint", "AI Hint"), ("auto", "AI Auto-Solve")]),
        ]),
        (3, "Process Over Answers", [
            ("mg_pattern", "Miguel's pattern challenge", [("alone", "Solved it yourself"), ("hint", "AI Hint"), ("auto", "AI Auto-Solve")]),
            ("c3_chloe", "Chloe's question", [("helping", "\"It helps.\""), ("weaker", "\"It makes us weaker.\""), ("depends", "\"Depende.\"")]),
            ("mg_fact", "Ethan's AI-written report", [("manual", "Fact-checked it yourself"), ("scanner", "Ran the AI Checker")]),
        ]),
        (4, "Whose Work Is It?", [
            ("mg_research", "Research sprint", [("clean", "No AI hints"), ("hint", "Used AI hints")]),
            ("c4_premium", "The free Premium trial", [("later", "Maybe Later"), ("upgrade", "Upgrade Now"), ("none", "Closed the phone")]),
            ("c4_qa", "Proposal Q&A", [("own", "Own words"), ("read", "Read the slide"), ("freeze", "Looked at Miguel")]),
        ]),
        (5, "The Final Challenge", [
            ("c5_rebuild", "The corrupted files", [("alone", "Rebuilt from memory"), ("ai", "AI Rebuild")]),
            ("fd", "Free Day", [("room", "Room"), ("library", "Library"), ("canteen", "Canteen"), ("creative", "Art Room")]),
        ]),
        (6, "What We Carry", [
            ("spot", "Chloe's submissions", [("sharp", "Spotted the AI"), ("fooled", "Got fooled")]),
            ("final", "\"Need help getting started?\"", [("own", "Start on your own"), ("ai", "Let AI start it")]),
            ("ending", "Ending", [("A", "Route A · Balanced"), ("B", "Route B · Moderate"), ("C", "Route C · High")]),
        ]),
    ]
    FC_TOTAL = sum(len(o) for (_c, _t, nodes) in FC_CHAPTERS for (_n, _q, o) in nodes)

    def fc_current():
        """node -> set(option) for THIS playthrough"""
        cur = {}
        def put(node, opt):
            if opt:
                cur.setdefault(node, set()).add(opt)
        put("c1_mood", _gv("c1_mood"))
        cr = _gv("_chaos_result")
        if cr is not None:
            if _gv("_chaos_hints"):
                put("mg_room", "hint")
            elif cr >= len(MORNING_CHAOS_ITEM_INFO):
                put("mg_room", "clean")
            else:
                put("mg_room", "partial")
        put("c1_puzzle", _gv("c1_puzzle"))
        put("c2_notif", _gv("c2_notif"))
        put("mg_reflection", _gv("_rb_mode"))
        put("mg_pattern", _gv("_pl_mode"))
        put("c3_chloe", _gv("c3_chloe"))
        put("mg_fact", _gv("_dc_mode"))
        rh = _gv("_research_hints")
        if rh is not None:
            put("mg_research", "hint" if rh else "clean")
        put("c4_premium", _gv("c4_premium"))
        put("c4_qa", _gv("c4_qa"))
        put("c5_rebuild", _gv("c5_rebuild"))
        for loc, v in (_gv("map_visited", {}) or {}).items():
            if v and loc in ("room", "library", "canteen", "creative"):
                put("fd", loc)
        sr = _gv("spot_result")
        if sr is not None:
            put("spot", "sharp" if sr >= len(SPOT_ROUNDS) else "fooled")
        put("final", _gv("final_choice"))
        put("ending", _gv("fc_ending"))
        return cur

    def fc_sync():
        seen = set(persistent.fc_seen or set())
        for node, opts in fc_current().items():
            for o in opts:
                k = node + ":" + o
                if k not in seen:
                    seen.add(k)
                    store.fc_new = store.fc_new | {k}
        persistent.fc_seen = seen
        ach_check()

    def fc_pct():
        return int(round(100.0 * len(persistent.fc_seen or ()) / FC_TOTAL))

    # ------------------------------------------------ story achievements
    # (id, title, how to get it, secret?)
    STORY_ACH = [
        ("early",    "Not Late After All",     "Find everything in Morning Chaos without AI.", False),
        ("switch",   "Feel the Heat",          "Solve the three-switch puzzle yourself.", False),
        ("asked",    "Ask a Human",            "Ask your classmates instead of AI.", False),
        ("swipe",    "Swipe Left on AI",       "Swipe away the AI notification in Chapter 2.", False),
        ("ownwords", "My Own Words",           "Match every idea card without any AI help.", False),
        ("boss",     "Miguel's Match",         "Solve all of Miguel's patterns with no hints and no mistakes.", False),
        ("editor",   "Perfect Editor",         "Catch every error in Ethan's report with no wrong taps.", False),
        ("offline",  "Phone Down",             "Close the phone on the free Premium trial.", False),
        ("clear",    "\"Clear.\"",             "Answer Prof. Santos in your own words.", False),
        ("memory",   "It Was In Us",           "Save the project files yourself.", False),
        ("spotter",  "AI Detector",            "Spot the fake in every round of Chloe's photos.", False),
        ("resist",   "Not Today",              "Resist every timed AI temptation in one playthrough.", False),
        ("encore",   "Encore!",                "Clear the 7-tile encore round.", False),
        ("stars",    "Star Student",           "Get 3 stars in 5 different mini games.", False),
        ("route_a",  "Balanced",               "Reach Route A.", False),
        ("route_b",  "Somewhere in Between",   "Reach Route B.", False),
        ("route_c",  "Wake-Up Call",           "Reach Route C.", True),
        ("all3",     "Every Ending",           "See all three endings.", False),
        ("flow50",   "Path Finder",            "Discover half of the flowchart.", False),
        ("flow100",  "Every Path",             "Discover the whole flowchart.", False),
        ("keys10",   "Key Collector",          "Find 10 hidden Ctrl keys.", False),
        ("keys20",   "Ctrl + Found",           "Find all 20 hidden Ctrl keys.", False),
        ("wrapped",  "That's a Wrap",          "See your Semester Wrapped.", False),
        ("secret",   "Behind the Code",        "Watch the secret scene.", True),
    ]
    STORY_ACH_BY_ID = dict((a[0], a) for a in STORY_ACH)
    _story_ach_queue = []

    def story_ach(aid):
        got = set(persistent.story_ach or set())
        if aid in got or aid not in STORY_ACH_BY_ID:
            return
        got.add(aid)
        persistent.story_ach = got
        _story_ach_queue.append(aid)
        if not renpy.get_screen("story_ach_toast"):
            renpy.show_screen("story_ach_toast", aid=_story_ach_queue[0])
        renpy.play("audio/sfx_correct.ogg", channel="detail")

    def story_ach_next():
        if _story_ach_queue:
            _story_ach_queue.pop(0)
        renpy.hide_screen("story_ach_toast")
        if _story_ach_queue:
            renpy.show_screen("story_ach_toast", aid=_story_ach_queue[0])

    def ach_check():
        cur = fc_current()
        def has(node, opt):
            return opt in cur.get(node, ())
        if has("mg_room", "clean"): story_ach("early")
        if has("c1_puzzle", "self"): story_ach("switch")
        if has("c1_puzzle", "classmates"): story_ach("asked")
        if has("c2_notif", "swipe"): story_ach("swipe")
        if has("mg_reflection", "alone"): story_ach("ownwords")
        if has("mg_pattern", "alone") and not _gv("pl_wrong"): story_ach("boss")
        if has("mg_fact", "manual") and (_gv("dc_found") or 0) >= CE_MAIN_ERR and not _gv("dc_false"): story_ach("editor")
        if has("c4_premium", "none"): story_ach("offline")
        if has("c4_qa", "own"): story_ach("clear")
        if has("c5_rebuild", "alone"): story_ach("memory")
        if (_gv("spot_result") or 0) >= len(SPOT_ROUNDS): story_ach("spotter")
        t = _gv("temptations") or {}
        if t.get("total", 0) >= 2 and t.get("resisted", 0) == t.get("total", 0) and _gv("story_chapter", 0) >= 7:
            story_ach("resist")
        if (persistent.mg_best and len([k for k, v in persistent.mg_best.items() if v >= 3]) >= 5):
            story_ach("stars")
        if persistent.seen_route_a: story_ach("route_a")
        if persistent.seen_route_b: story_ach("route_b")
        if persistent.seen_route_c: story_ach("route_c")
        if persistent.seen_route_a and persistent.seen_route_b and persistent.seen_route_c: story_ach("all3")
        p = fc_pct()
        if p >= 50: story_ach("flow50")
        if p >= 100: story_ach("flow100")
        nk = len(persistent.ctrl_keys or ())
        if nk >= 10: story_ach("keys10")
        if nk >= len(CTRL_KEYS): story_ach("keys20")

    # ------------------------------------------------ completion %
    def completion_pct():
        endings = sum(1 for r in ("a", "b", "c") if getattr(persistent, "seen_route_" + r))
        parts = [
            (0.35, len(persistent.fc_seen or ()) / float(FC_TOTAL)),
            (0.30, len(persistent.story_ach or ()) / float(len(STORY_ACH))),
            (0.15, len(persistent.ctrl_keys or ()) / float(len(CTRL_KEYS))),
            (0.20, endings / 3.0),
        ]
        return int(round(100 * sum(w * min(1.0, v) for w, v in parts)))

    def _v241_label_cb(name, abnormal):
        if name in ("ending_route_a", "ending_route_b", "ending_route_c"):
            store.fc_ending = name[-1].upper()
            fc_sync()
        elif name in ("chapter2", "chapter3", "chapter4", "chapter5", "chapter6", "free_day_end", "the_end"):
            fc_sync()

    config.label_callbacks.append(_v241_label_cb)


# ------------------------------------------------------------ toast
transform story_toast_in:
    yoffset -30 alpha 0.0
    easeout 0.3 yoffset 0 alpha 1.0
    pause 2.6
    easein 0.3 yoffset -30 alpha 0.0

screen story_ach_toast(aid):
    zorder 610
    $ _a = STORY_ACH_BY_ID[aid]
    timer 3.3 action Function(story_ach_next)
    frame:
        xalign 1.0
        xoffset -24
        ypos 88
        padding (16, 10, 22, 10)
        background Frame("images/minigames/ui/card_accent.png", 18, 18)
        at story_toast_in
        hbox:
            spacing 12
            fixed:
                xysize (40, 40)
                add Transform("images/minigames/ui/circle.png", matrixcolor=TintMatrix("#cba6f7") * BrightnessMatrix(-0.35), xysize=(40, 40))
                text "{font=DejaVuSans.ttf}★{/font}" size 22 color "#f1e8ff" xalign 0.5 yalign 0.5
            vbox:
                yalign 0.5
                text "TROPHY UNLOCKED" size 12 color "#cba6f7" kerning 2 font "fonts/Rajdhani-Bold.ttf"
                text _a[1] size 19 color "#ffffff" font "fonts/Rajdhani-Bold.ttf" substitute False


# ------------------------------------------------------------ flowchart
transform fc_node_in(d):
    alpha 0.0 xoffset -16
    pause d
    easeout 0.3 alpha 1.0 xoffset 0

transform fc_new_pulse:
    alpha 1.0
    block:
        ease 0.6 alpha 0.55
        ease 0.6 alpha 1.0
        repeat

label fc_after_chapter(ch):
    $ fc_sync()
    # v257 (panel): the chapter's score and Prof. Santos's feedback first.
    call v257_chapter_report(ch) from _call_v257_chapter_report
    call screen flowchart(ch, True)
    $ fc_new = set()
    return

screen flowchart(ch=1, after=False, from_phone=False):
    tag menu
    modal True
    default fc_ch = (max(1, min(6, story_chapter)) if from_phone else ch)
    add gui.main_menu_background
    add Solid("#0b0914ee")
    use ambient_particles(count=14, tint="#cba6f7")

    $ _cur = fc_current() if not main_menu else {}
    $ _seen = persistent.fc_seen or set()
    $ _chs = dict((c[0], c) for c in FC_CHAPTERS)
    $ _reached = (story_chapter if not main_menu else 7)

    text "FLOWCHART" xpos 60 ypos 34 size 30 color "#e3d3ff" font "fonts/Orbitron-ExtraBold-static.ttf"
    text ("Paths discovered: %d / %d  ·  %d%%" % (len(_seen), FC_TOTAL, fc_pct())) xpos 62 ypos 78 size 16 color "#8a86a3" font "fonts/Rajdhani-SemiBold.ttf"

    # chapter tabs
    hbox:
        xpos 60
        ypos 112
        spacing 8
        for (_c, _t, _n) in FC_CHAPTERS:
            $ _ok = main_menu or _c <= max(1, _reached) or any(k.split(":")[0] in [n[0] for n in _n] for k in _seen)
            textbutton ("CH %d" % _c):
                action SetScreenVariable("fc_ch", _c)
                sensitive _ok
                selected fc_ch == _c
                style "mg_btn"
                text_style "mg_btn_text"
                selected_background Frame("images/minigames/ui/btn_ai.png", 23, 23)
                xminimum 92

    $ _cc, _ct, _nodes = _chs[fc_ch]
    text _ct xpos 60 ypos 176 size 24 color "#fab387" font "fonts/Rajdhani-Bold.ttf"

    # the spine
    add Solid("#cba6f755") xpos 79 ypos 222 xysize (2, 100 * len(_nodes) + 6)

    for _i, (_nid, _q, _opts) in enumerate(_nodes):
        $ _y = 222 + _i * 100
        fixed:
            xpos 60
            ypos _y
            xysize (1160, 96)
            at fc_node_in(0.08 + _i * 0.12)
            add Transform("images/minigames/ui/circle.png", matrixcolor=TintMatrix("#cba6f7"), xysize=(22, 22)) xpos 9 ypos 6
            text _q xpos 48 ypos 2 size 17 color "#d9d2ee" font "fonts/Rajdhani-Bold.ttf" substitute False
            hbox:
                xpos 48
                ypos 32
                spacing 12
                for (_oid, _ol) in _opts:
                    $ _k = _nid + ":" + _oid
                    $ _taken = _oid in _cur.get(_nid, ())
                    $ _known = _k in _seen
                    frame:
                        xsize 250
                        ysize 52
                        padding (12, 6)
                        background Frame(("images/minigames/ui/card_accent.png" if _taken else "images/minigames/ui/card.png"), 14, 14)
                        if _known:
                            hbox:
                                yalign 0.5
                                spacing 8
                                if _taken:
                                    text "{font=DejaVuSans.ttf}✔{/font}" size 16 color "#a6e3a1" yalign 0.5
                                text _ol size 15 color ("#ffffff" if _taken else "#a39dbd") yalign 0.5 xmaximum 200 substitute False
                            if _k in fc_new:
                                text "NEW" size 11 color "#f9e2af" font "fonts/Rajdhani-Bold.ttf" xalign 1.0 yalign 0.0 at fc_new_pulse
                        else:
                            hbox:
                                yalign 0.5
                                spacing 8
                                text "???" size 15 color "#5d5878" yalign 0.5 font "fonts/Rajdhani-Bold.ttf"
                                text "not found yet" size 12 color "#4f4a66" yalign 0.5 italic True

    hbox:
        xalign 1.0
        yalign 1.0
        xoffset -40
        yoffset -30
        spacing 14
        if after:
            textbutton "Continue" style "mg_go_btn" text_style "mg_go_btn_text" action Return(True) keysym ["K_RETURN", "K_KP_ENTER"]
        elif from_phone:
            textbutton "Back" style "mg_btn" text_style "mg_btn_text" action ShowMenu("phone_home")
        else:
            textbutton "Back" style "mg_btn" text_style "mg_btn_text" action Return()
    if not after:
        key "game_menu" action Return()


# ------------------------------------------------------------ trophies
screen trophy_room():
    tag menu
    modal True
    add gui.main_menu_background
    add Solid("#0c0a15ee")
    use ambient_particles(count=12, tint="#cba6f7")
    $ _got = persistent.story_ach or set()
    $ _nk = len(persistent.ctrl_keys or ())

    text "TROPHY ROOM" xpos 60 ypos 34 size 30 color "#e3d3ff" font "fonts/Orbitron-ExtraBold-static.ttf"
    text ("%d of %d trophies  ·  Ctrl keys %d / %d  ·  Game %d%% complete" % (len([a for a in STORY_ACH if a[0] in _got]), len(STORY_ACH), _nk, len(CTRL_KEYS), completion_pct())) xpos 62 ypos 78 size 16 color "#8a86a3" font "fonts/Rajdhani-SemiBold.ttf"

    # Ctrl keys strip
    hbox:
        xpos 60
        ypos 106
        spacing 10
        for _kid in CTRL_KEY_ORDER:
            $ _have = _kid in (persistent.ctrl_keys or ())
            add Transform("images/fx/ctrl_key.png", zoom=0.86, matrixcolor=(IdentityMatrix() if _have else SaturationMatrix(0.0) * BrightnessMatrix(-0.45))) alpha (1.0 if _have else 0.5)

    vpgrid:
        cols 4
        spacing 14
        xpos 60
        ypos 168
        xysize (1170, 458)
        mousewheel True
        draggable True
        for (_id, _t, _d, _secret) in STORY_ACH:
            $ _ok = _id in _got
            frame:
                xsize 282
                ysize 104
                padding (14, 12)
                background Frame(("images/minigames/ui/card_accent.png" if _ok else "images/minigames/ui/card.png"), 16, 16)
                hbox:
                    spacing 12
                    fixed:
                        xysize (42, 42)
                        add Transform("images/minigames/ui/circle.png", matrixcolor=(TintMatrix("#cba6f7") * BrightnessMatrix(-0.3) if _ok else TintMatrix("#3a3550")), xysize=(42, 42))
                        text ("{font=DejaVuSans.ttf}★{/font}" if _ok else "?") size 22 color ("#f1e8ff" if _ok else "#6b6785") xalign 0.5 yalign 0.5
                    vbox:
                        spacing 3
                        xsize 200
                        text ((_t) if (_ok or not _secret) else "Secret trophy") size 16 color ("#ffffff" if _ok else "#a39dbd") font "fonts/Rajdhani-Bold.ttf" substitute False
                        text ((_d) if (_ok or not _secret) else "Keep playing to find out.") size 13 color ("#cfc4e8" if _ok else "#6f6a88") substitute False

    hbox:
        xalign 1.0
        yalign 1.0
        xoffset -40
        yoffset -26
        spacing 14
        textbutton "Campus Life achievements" style "mg_btn" text_style "mg_btn_text" action ShowMenu("cl_achievements")
        textbutton "Back" style "mg_btn" text_style "mg_btn_text" action Return()
    key "game_menu" action Return()


# ------------------------------------------------------------ extras
screen extras():
    tag menu
    modal True
    add gui.main_menu_background at kenburns_slow
    add Solid("#0c0a15d8")
    use ambient_particles(count=16, tint="#cba6f7")

    text "EXTRAS" xpos 80 ypos 60 size 40 color "#e3d3ff" font "fonts/Orbitron-ExtraBold-static.ttf"
    text ("Game %d%% complete" % completion_pct()) xpos 82 ypos 112 size 18 color "#cba6f7" font "fonts/Rajdhani-Bold.ttf"
    fixed:
        xpos 82
        ypos 140
        xysize (420, 8)
        add Solid("#2a2640") xysize (420, 8)
        add Solid("#cba6f7") xysize (max(2, int(420 * completion_pct() / 100.0)), 8)

    $ _sec = len(persistent.ctrl_keys or ()) >= len(CTRL_KEYS)
    $ _tiles = [
        ("Flowchart", "Every choice, and the paths you haven't found", ShowMenu("flowchart", 1, False), True),
        ("Trophy Room", "Story trophies, Ctrl keys and Campus Life", ShowMenu("trophy_room"), True),
        ("Watch the Opening", "The opening movie", Start("watch_opening"), True),
        ("Credits", "The people who made Ctrl + Think", Start("watch_credits"), True),
        ("Campus Life", "Free time between chapters", ShowMenu("cl_menu"), cl_unlocked()),
        ("Behind the Code", ("Secret scene" if _sec else "Find all 20 hidden Ctrl keys to unlock"), Start("secret_scene"), _sec),
    ]
    grid 2 3:
        xpos 80
        ypos 180
        spacing 16
        for (_tt, _td, _ta, _on) in _tiles:
            button:
                xysize (420, 120)
                padding (22, 16)
                background Frame("images/minigames/ui/card.png", 16, 16)
                hover_background Frame("images/minigames/ui/card_hover.png", 16, 16)
                insensitive_background Frame("images/minigames/ui/btn_off.png", 16, 16)
                hover_sound "audio/ui_hover.ogg"
                activate_sound "audio/ui_select.ogg"
                sensitive _on
                action _ta
                vbox:
                    spacing 6
                    yalign 0.5
                    text _tt size 24 color ("#e3d3ff" if _on else "#5a5570") font "fonts/Rajdhani-Bold.ttf"
                    text _td size 15 color ("#a39dbd" if _on else "#4f4a66")

    textbutton "Back" style "mg_btn" text_style "mg_btn_text" xpos 80 ypos 640 action Return()
    key "game_menu" action Return()
