## ============================================================
## v257 PANEL RECOMMENDATIONS (oral defense)
##
## The panel asked for four changes. Each one lives here and is
## reached by a one-line `call` from the existing story:
##
##   1. A stronger start with a twist     v257_cold_open       (start)
##   2. Show the consequences in Ch 1     v257_cold_open,      (start)
##                                        v257_ch1_reasons     (Ch1 classroom)
##   3. Give the reasons, not just "bawal" v257_ch1_reasons    (Ch1 classroom)
##   4. Score + feedback after a chapter  v257_chapter_report  (fc_after_chapter)
##
## Nothing here changes the dependency score, the route or the
## endings. The report only reads the numbers the story already keeps.
## ============================================================

default v257_marks = {}         # chapter -> (dependency total, critical thinking) when its report was shown

image bg v257_office = Transform("images/backgrounds/classroom.jpg", xysize=(1280, 720), matrixcolor=TintMatrix("#a9b2ff") * SaturationMatrix(0.55) * BrightnessMatrix(-0.28))

init python:
    def v257_dep_total():
        return store.dep_acads + store.dep_family + store.dep_mental + store.dep_creativity

    def v257_score():
        """Same formula as evaluate_route and the phone's Stats app."""
        raw = v257_dep_total() - store.crit_thinking
        return max(0, min(100, int(round(raw * 100.0 / 120.0))))

    def v257_route(score):
        if score <= 33:
            return ("Balanced Use", "#9ad9b5")
        if score <= 66:
            return ("Moderate Dependency", "#fab387")
        return ("High Dependency", "#e78284")

    # (verdict, colour, what Prof. Santos says) by how much this chapter
    # pushed the score: AI dependency gained minus critical thinking gained.
    V257_VERDICTS = [
        (5,   "You did the thinking", "#9ad9b5",
         "Ganyan. Ikaw ang nag-isip, kaya sa'yo ang natutunan mo. Hindi mabilis, pero totoo."),
        (15,  "Leaning on AI", "#fab387",
         "May mga pagkakataong ipinasa mo sa AI ang pag-iisip. Okay lang humingi ng tulong, basta naiintindihan mo pa rin ang sagot."),
        (999, "AI did the thinking", "#e78284",
         "Halos AI ang nagdesisyon ngayong chapter. Mabilis nga, pero kaunti ang natutunan mo. Sa exam at sa trabaho, walang AI na sasagot para sa'yo."),
    ]

    # Why each chapter's lesson matters (the panel: give a basis).
    V257_WHY = {
        1: "Kapag AI agad ang tinatanong mo, nakukuha mo ang sagot pero hindi ang pag-unawa. Ang pag-unawa ang nagagamit mo ulit.",
        2: "Ang sarili mong salita ang nagpapakita kung ano talaga ang naiisip mo. Kapag AI ang sumulat, hindi na ikaw ang nasa papel.",
        3: "Nagkakamali ang AI, minsan nang buong confidence. Kung hindi mo alam ang proseso, hindi mo mapapansin ang mali.",
        4: "Sa group work, tiwala ang puhunan. Kapag hindi mo maipaliwanag ang ambag mo, hindi mo rin ito maipagtatanggol.",
        5: "Ang natutunan mo ay nasa'yo kahit mawala ang files. Ang ipinagawa mo sa AI, kasama ring nawawala.",
        6: "Ang pinakamahirap na bahagi ay ang pagsisimula. Kapag ikaw ang nagsimula, ikaw rin ang may hawak ng direksyon.",
    }

    def v257_report_data(ch):
        """Snapshot this chapter and compare it with the last report."""
        dep, crit = v257_dep_total(), store.crit_thinking
        earlier = [c for c in store.v257_marks if c < ch]
        if ch == 1:
            prev = (0, 0)
        elif earlier:
            prev = store.v257_marks[max(earlier)]
        else:
            prev = None             # started from Chapter Select: no baseline
        marks = dict(store.v257_marks)
        marks[ch] = (dep, crit)
        store.v257_marks = marks
        if prev is None:
            return None, None, None
        dep_gain = max(0, dep - prev[0])
        crit_gain = max(0, crit - prev[1])
        return dep_gain, crit_gain, dep_gain - crit_gain

    def v257_verdict(net):
        for (limit, title, color, line) in V257_VERDICTS:
            if net <= limit:
                return title, color, line
        return V257_VERDICTS[-1][1:]


# ------------------------------------------------------------
# 1 + 2. COLD OPEN — a glimpse of the worst case, then rewind
# ------------------------------------------------------------
label v257_cold_open:
    stop music fadeout 1.0
    scene bg black
    with fade
    play music audio.bgm_tension fadein 1.5
    centered "{size=+14}{b}FINALS WEEK{/b}{/size}\n{size=-2}4:47 PM · Faculty Office{/size}"

    scene bg v257_office
    with dissolve
    show alex worried at left_alive, enter_left
    show prof at right_alive, enter_right, card_scale_side
    narrator "Nasa mesa ang final paper mo. May pulang marka sa unang pahina."
    prof "Maganda ang paper mo. Malinis. Walang kahit isang mali."
    prof "Kaya nga ako nagtataka."
    prof "Ipaliwanag mo nga sa akin ang second paragraph. In your own words."
    show alex confused at left_alive, confused_tilt
    alex_v "Ah... yung second paragraph po ay tungkol sa..."
    narrator "Binasa mo ulit. Parang ngayon mo lang nakita ang mga salitang 'yon."
    alex_v "{i}...Ano nga ba 'to?{/i}"
    prof "Hindi mo maipaliwanag ang sarili mong papel."
    prof "Ibig sabihin, hindi ito sa'yo."
    show alex sad at left_alive, scared_shake
    narrator "Sa tabi ng pangalan mo, isang numero ang nakasulat sa pula."
    narrator "{size=+26}{b}{color=#e78284}5.0{/color}{/b}{/size}"
    alex_v "{i}Paano ako umabot dito?{/i}"
    hide prof
    hide alex

    scene bg black
    with Fade(0.05, 0.0, 0.6, color="#ffffff")
    stop music fadeout 0.8
    centered "{size=+24}{b}{color=#cba6f7}REWIND{/color}{/b}{/size}\n{size=-2}Tatlong buwan bago nito{/size}"
    narrator "Hindi pa ito nangyayari."
    narrator "Ang bawat desisyong gagawin mo ang magdadala sa'yo dito... o hindi."
    play music audio.bgm_menu fadein 1.5
    return


# ------------------------------------------------------------
# 2 + 3. CHAPTER 1 — Prof. Santos gives the reasons
# ------------------------------------------------------------
label v257_ch1_reasons:
    prof "Hindi ko sinasabing bawal ang AI."
    prof "Ang tanong: bakit delikado kapag ito na ang nag-iisip para sa inyo?"
    narrator "Itinaas niya ang tatlong daliri."
    prof "Una. Ang utak, parang muscle. Kapag lagi mong ipinapasa sa AI ang pag-iisip, hindi na ito nag-e-exercise. Cognitive offloading ang tawag diyan."
    prof "Pangalawa. Nagkakamali ang AI, at minsan sobrang confident pa. Kung hindi mo naiintindihan ang topic, hindi mo malalaman na mali na pala ang ipinasa mo."
    prof "Pangatlo. Kapag ipinasa mo bilang sa'yo ang gawa ng AI, academic dishonesty 'yan. Hindi lang grade ang nawawala. Pati tiwala."
    prof "Last semester, may estudyanteng nagpasa ng reflection paper na AI ang gumawa."
    prof "Perfect ang grammar. Maayos ang structure."
    prof "Pero nung tinanong ko kung ano ang ibig sabihin ng conclusion niya, hindi niya masagot."
    narrator "Tumahimik ang buong klase."
    prof "Binagsak ko siya. Hindi dahil gumamit siya ng AI, kundi dahil wala siyang natutunan sa sarili niyang papel."
    prof "Kaya bago kayo mag-click, tanungin niyo muna ang sarili ninyo: tool ba ito ngayon, o replacement?"
    return


# ------------------------------------------------------------
# 4. CHAPTER REPORT — score + Prof. Santos's feedback
# ------------------------------------------------------------
label v257_chapter_report(ch):
    $ _v257_dep, _v257_crit, _v257_net = v257_report_data(ch)
    call screen v257_chapter_report(ch, _v257_dep, _v257_crit, _v257_net)
    return

transform v257_card_in(d):
    alpha 0.0 yoffset 18
    pause d
    easeout 0.35 alpha 1.0 yoffset 0

screen v257_chapter_report(ch, dep_gain, crit_gain, net):
    tag menu
    modal True
    add gui.main_menu_background
    add Solid("#0b0914ee")
    use ambient_particles(count=14, tint="#cba6f7")

    $ _title = dict((c[0], c[1]) for c in FC_CHAPTERS).get(ch, "")
    $ _score = v257_score()
    $ _route, _rcol = v257_route(_score)
    $ _has_delta = net is not None
    $ _verdict, _vcol, _line = v257_verdict(net if _has_delta else 0)
    if not _has_delta:
        $ _line = "Ito ang dependency score mo sa ngayon. Bantayan mo kung paano ito gagalaw sa mga susunod na chapter."

    text ("CHAPTER %d REPORT" % ch) xpos 60 ypos 34 size 30 color "#e3d3ff" font "fonts/Orbitron-ExtraBold-static.ttf"
    text _title xpos 62 ypos 78 size 20 color "#fab387" font "fonts/Rajdhani-Bold.ttf" substitute False

    # this chapter
    frame:
        xpos 60
        ypos 124
        xysize (560, 236)
        padding (26, 20)
        background Frame("images/minigames/ui/card.png", 16, 16)
        at v257_card_in(0.05)
        vbox:
            spacing 8
            text "THIS CHAPTER" size 14 color "#9399b2" font "fonts/Rajdhani-Bold.ttf" kerning 2
            if _has_delta:
                text ("%+d" % net) size 58 color _vcol font "fonts/Orbitron-ExtraBold-static.ttf"
                text _verdict size 22 color _vcol font "fonts/Rajdhani-Bold.ttf"
                text ("AI dependency +%d  ·  Critical thinking +%d" % (dep_gain, crit_gain)) size 16 color "#cfc4e8"
            else:
                null height 10
                text "Walang naunang chapter na maikukumpara." size 18 color "#cfc4e8"
                text "Nagsimula ka sa Chapter Select." size 16 color "#8a86a3"

    # overall score
    frame:
        xpos 660
        ypos 124
        xysize (560, 236)
        padding (26, 20)
        background Frame("images/minigames/ui/card_accent.png", 16, 16)
        at v257_card_in(0.18)
        vbox:
            spacing 8
            text "OVERALL DEPENDENCY SCORE" size 14 color "#9399b2" font "fonts/Rajdhani-Bold.ttf" kerning 2
            hbox:
                spacing 6
                text ("%d" % _score) size 58 color _rcol font "fonts/Orbitron-ExtraBold-static.ttf"
                text "/ 100" size 20 color "#8a86a3" yalign 0.85 font "fonts/Rajdhani-Bold.ttf"
            fixed:
                xysize (508, 10)
                add Solid("#00000066") xysize (508, 10)
                add Solid(_rcol) xysize (max(2, int(508 * _score / 100.0)), 10)
            text ("If it ended now: {b}%s{/b}" % _route) size 17 color _rcol
            text "0–33 Balanced  ·  34–66 Moderate  ·  67–100 High  ·  lower is better" size 14 color "#8a86a3"

    # Prof. Santos
    frame:
        xpos 60
        ypos 384
        xysize (1160, 232)
        padding (26, 20)
        background Frame("images/minigames/ui/card.png", 16, 16)
        at v257_card_in(0.31)
        vbox:
            spacing 10
            text "PROF. SANTOS" size 14 color "#b39ddb" font "fonts/Rajdhani-Bold.ttf" kerning 2
            text ("\"%s\"" % _line) size 20 color "#ffffff" xmaximum 1100 substitute False
            null height 4
            text "BAKIT ITO MAHALAGA" size 14 color "#9399b2" font "fonts/Rajdhani-Bold.ttf" kerning 2
            text V257_WHY.get(ch, "") size 18 color "#cfc4e8" xmaximum 1100 substitute False

    textbutton "See your choices  {font=DejaVuSans.ttf}▶{/font}" style "mg_go_btn" text_style "mg_go_btn_text" xalign 1.0 yalign 1.0 xoffset -40 yoffset -30 action Return(True) keysym ["K_RETURN", "K_KP_ENTER"]
