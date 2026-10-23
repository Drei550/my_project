## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.


## Basics ######################################################################

## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.

define config.name = _("Ctrl + Think")


## Determines if the title given above is shown on the main menu screen. Set
## this to False to hide the title.

define gui.show_name = True


## The version of the game.

define config.version = "1.1"


## Text that is placed on the game's about screen. To insert a blank line
## between paragraphs, write \n\n.

define gui.about = _("""Ctrl + Think: An Interactive Visual Novel Game
Exploring AI Dependency Among College Students

A Capstone Project

Location backgrounds: Potat0Master (potat0master.itch.io)""")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "ctrl_think"

## Change the version used by the build system.
define build.version = "0.1"

## Sounds and music ############################################################

define config.has_sound = True
define config.has_music = True
define config.has_voice = False


## Transitions #################################################################

define config.enter_transition = dissolve
define config.exit_transition = dissolve

define config.after_load_transition = None

define config.end_game_transition = None


## Window management ###########################################################

define config.window = "auto"

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## Preference defaults #########################################################

default preferences.text_cps = 0

default preferences.afm_time = 15


## Save directory ##############################################################

define config.save_directory = "ctrl_think-0.1"


## Icon ########################################################################

define config.window_icon = "gui/window_icon.png"


## Build configuration #########################################################

init python:

    # SDK Fonts.
    config.searchpath.append(config.renpy_base + "/sdk-fonts")
    build.classify_renpy("sdk-fonts/**", "all")
    build._sdk_fonts = True

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.documentation('*.html')
    build.documentation('*.txt')


# Enable the console.
define config.console = True
define config.fadeout_audio = 1.2   # v229: songs fade into each other instead of cutting
