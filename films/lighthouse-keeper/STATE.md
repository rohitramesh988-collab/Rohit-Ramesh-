# State: Untitled

Read this first in every new session, after loading the cinecode skill (Claude Code: the Skill tool, never a plain read of SKILL.md), then `python3 KIT/scripts/init_film.py . --update-tools` silently; update "Now" before ending every turn. Keep it short.
Kit: /root/.claude/skills/cinecode
Method: this chat coordinates and builds what it holds the context for; a fresh helper takes only an independent part beside it (sound, narration takes, research, the independent viewer) or a long film's chapter, briefed from files (`/root/.claude/skills/cinecode/references/context-protocol.md`).

## Resume here
<!-- Updated at every gate and before every handoff. A new chat starts with "STATE.md'den devam et" / "Continue from STATE.md". -->
- **Audio done (v1):** audio/build.py writes stems, tools/mix.py + master_audio.py give audio/master-v1.wav at -14 LUFS, TP -1.0 (loudnorm ran in dynamic mode: a light compression, because the whistle peaks are high). Not yet heard by the user: needs a listen at 7.2 s, 10.2 s, 33 to 38 s (silence), 47 s and 55.4 s. Type: Newsreader (user's pick under Pace through: ★), local files in fonts/newsreader, rows in LICENSES.csv.
- **Phase:** 4 Style frame done as progress stills (review/sheet4.png: eight shots, one frame each). Sea haze, far tower and lips now read; hand in S04 and the keeper's face are still crude. Next: type, audio, animatic, draft.
- **Pace:** through
- **Approved gates:** roadmap, script
- **Open notes:** none (notes/round-N.md)
- **Next action:** fix the test stills in review/test: the sea is blown out white (lower its brightness or the exposure), the far rock is lost in fog (lower fog or move it closer), and the S01 camera sits inside lamp room geometry (move it, hide the glass). Re-render with: node tools/capture.mjs --url engine/whistle.html --out review/test --frames "72,240,432,624,816,1056,1200,1368" --params "w=640&h=360" --flags "--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist" (about 0.75 fps at 640x360, so a full 60 s draft is about 32 min). Still to do: type pick, audio (whistle and music in code), animatic, draft. engine/vendor is not in git: restore it with npm install three@0.186.1 postprocessing@6.39.5 and copy build and examples/jsm into engine/vendor (the CDNs are blocked here).
- **Budget so far:** <~estimate> of the <Balanced> ceiling (<n>%)

## Now
- **Step:** 1 Interview
- **Gate:** <waiting for user: what / passed>
- **Next step:** <one concrete line>
- **Waiting for:** <user / background job / nothing>
- **Profile:** balanced
- **Purpose:** <cinematic · ad & product> (`/root/.claude/skills/cinecode/references/purpose-<cinematic|ad>.md`)
- **Format:** <length, aspect, size, fps>
- **Medium:** 3D realistic (user). Renders need software WebGL: capture flags "--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist" work, slow.
- **Look:** <preset id or custom>
- **Finishing:** <none · motion blur (shots) · print tone · gate weave> <!-- off by default; chosen at the style frame -->
- **Music:** <recording: file · own: file · code · none> (user) <!-- always asked, the recording picked by ear -->
- **Type:** <pairing id: display + text (+ mono) · user's reason · type direction (case, align, scale) · rule breaks named, or none>
- **Subtitles:** off
- **Last output:** <path, version>
- **Disk free at last check:** <GB, date>

## Running jobs
| Job | Command (short) | PID | Status file | Log | Started |
|---|---|---|---|---|---|

## Gates
| Step | Gate | Result | Date | Note |
|---|---|---|---|---|
| 1 | interview answered / defaults accepted | | | |
| 2 | roadmap approved | | | |
| 3 | script and text approved | | | |
| 4 | style frame approved, finishing chosen | | | |
| 4b | type pairing picked | | | |
| 5 | animatic approved | | | |
| 6a | draft cut approved | | | |
| 6 | final delivered | | | |

## Decisions
| Date | Decision | Why | Who |
|---|---|---|---|

## Notes rounds
Verbatim notes and the per-shot split live in `notes/round-N.md`.

| Round | File | Shots touched | Unchanged | Status |
|---|---|---|---|---|

## Agent tasks
| Task | Calls | Brief (files read) | Output file | Result |
|---|---|---|---|---|

## Budget meter
Ceiling: <Economy / Balanced / Quality> (internal caps: `references/context-protocol.md` §6). Stop and ask at 80%.

| Phase | Share of ceiling | Estimate so far | % of share | Note |
|---|---|---|---|---|
| 1-2 Interview + roadmap | 10% | | | |
| 3 Script | 10% | | | |
| 4 Style frame | 20% | | | |
| 5 Animatic | 15% | | | |
| 6 Render, sound, final | 35% | | | |
| Notes rounds | 10% | | | |
| **Total** | 100% | | | |

## Versions
| Version | File | What changed | Snapshot |
|---|---|---|---|


## Interview so far
- Idea: The Whistle (user): two keepers on separate rocks talk in whistled language; one night the other stops answering. Spark s2, angle place-remembers.
- Length/format: 60 s, 16:9 (user)
- Sound: narrator plus music (user); identity seed: under pressure
- Look: A Salt Dawn (user): overcast pre-dawn, pearl grey and rose, lamp amber, long lens, shallow focus
- Music: code (user). Voice: intimate first person, English (user). References: none (stills search blocked by proxy 403)
