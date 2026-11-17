# State: Untitled

Read this first in every new session, after loading the cinecode skill (Claude Code: the Skill tool, never a plain read of SKILL.md), then `python3 KIT/scripts/init_film.py . --update-tools` silently; update "Now" before ending every turn. Keep it short.
Kit: /root/.claude/skills/cinecode
Method: this chat coordinates and builds what it holds the context for; a fresh helper takes only an independent part beside it (sound, narration takes, research, the independent viewer) or a long film's chapter, briefed from files (`/root/.claude/skills/cinecode/references/context-protocol.md`).

## Resume here
<!-- Updated at every gate and before every handoff. A new chat starts with "STATE.md'den devam et" / "Continue from STATE.md". -->
- **Phase:** 1 Interview
- **Pace:** through (Film mode: asked with the script gate)
- **Approved gates:** roadmap, script
- **Open notes:** none (notes/round-N.md)
- **Next action:** <one concrete line, with the files to read>
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
