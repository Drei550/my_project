# Ctrl + Think: panel recommendations (v257)

These are the game changes for the four recommendations the panel gave at the oral defense. The dependency score, the routes and the endings are unchanged.

| # | Panel recommendation | What was added | Where |
|---|---|---|---|
| 1 | A stronger opening with a twist | A cold open right after character select: Finals Week, Prof. Santos asks you to explain your own paper, you can't, and you get a 5.0. Then **REWIND**: "Hindi pa ito nangyayari." | `v257_cold_open` |
| 2 | Show the consequences, starting in Chapter 1 | The cold open above, plus Prof. Santos's story in the Chapter 1 classroom about a student who submitted an AI-written reflection paper and failed | `v257_cold_open`, `v257_ch1_reasons` |
| 3 | Give the reasons, not just "bawal" | Prof. Santos explains three reasons: cognitive offloading, AI being confidently wrong, and academic dishonesty | `v257_ch1_reasons` |
| 4 | Score and feedback after each chapter | A **Chapter Report** before the flowchart: points gained this chapter, the overall dependency score out of 100, Prof. Santos's feedback, and why the chapter's lesson matters | `v257_chapter_report` |

## How to add them to your project

1. Copy everything in `game/` here into your project's `game/` folder and replace the files when asked.
   - `v257_panel.rpy` is new.
   - `script.rpy`, `v241_progress.rpy` and `options.rpy` each gain one or two lines; `v257_existing_files.diff` shows exactly which.
2. Open the Ren'Py launcher, select the project, and click **Launch Project** to test.
3. Build as usual: **Build Distributions** for Windows, **Android → Build Package** for the APK.

If your local copy of `script.rpy`, `v241_progress.rpy` or `options.rpy` is newer than the October 14 build, don't replace them. Add the lines from the `.diff` file by hand instead.
