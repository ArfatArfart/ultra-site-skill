# Semantic motion catalog

Rule: a word moves the way it means. Mark it up as `<span class="w" data-fx="name">word</span>`.
Each effect ships with a reason string that Why mode displays.

| fx | Use on | Motion | Reason |
|---|---|---|---|
| rough | raw, draft | chars fly in jagged, jitter, settle slightly crooked | raw things are unfinished |
| focus | idea, vision | blur 18px + wide tracking → sharp | ideas come into focus |
| enter | in, join | slides in from the right through a clip | the word literally enters |
| flap | shipped, launch | split flap board cycling letters | shipping is a departure |
| decode | software, code | ScrambleText from `01<>/{}#` | code is noise turned into meaning |
| launch | out, ship | letters rise with back ease, last glyph hops | a release leaving the pad |
| count | three, four | counts digits up, scrambles back to the word | a number word counts to itself |
| weight | discipline, team | font weight 100 → 600, scaleX 1.25 → 1 | weight is accumulated |
| stamp | one, workshop | scale 2.6 → 1 power4.in, heading shakes | a single impact |
| vanish | zero, none | appears then turns into an outline | zero empties out |
| relay | handoffs | highlight passes letter to letter | how work moves through handoffs |
| type | websites, write | typed with a moving caret | typed by hand |
| load | load, fast | stepped bar fills underneath | the most familiar progress |
| blink | blink | scaleY to 0.06 twice | literal |
| swipe | apps, unlock | clip reveal from below with a home pill | apps unlock with a swipe |
| doors | open | chars slide outward from the centre | doors opening |
| instant | thinking, instantly | no animation at all | without delay |
| pulse | backend, signal | glow travels across the letters | a request down a wire |
| calm | calm, stable | elastic jitter decays to still | calm is dampened noise |
| clock | 3am, tonight | runs a mono clock to 03:00 then scrambles back | the hour nobody notices |
| strike | strikes, hit | drops from above, heading shakes, slash | impact |
| sketch | sketch, draft | hand drawn SVG underline draws in | sketches are hand made |
| mark | selected, featured | highlighter sweeps behind | editors mark what matters |
| rec | live | blinking red dot | recording means live |
| orbit | orbit, around | letters spiral in from a ring | things in orbit settle |
| anchor | problem, core | heavy drop, stays still | everything else orbits it |
| shake | never, no | head shake keyframes | literal no |
| spin | round, cycle | one full rotation | literal round |
| cheap | cheap, claims | shrinks, dims, gets crossed out | value drops |
| measure | measured | ruler draws and prints the word's real px width | measured for real |
| curious | questions, why | letters tilt alternately then settle | a head tilting to ask |
| before | before, first | animates before every other word in its heading | literal order |

## Tagline reveal semantics

Words go from 28% to 100% opacity as the scroll passes them (scrubbed). Words wrapped in
`data-sem` get one extra behaviour on activation: `late` waits 700 ms, `breaks` glitches,
`forgotten` fades back to 16% and blurs, `hardened` stamps to bold, `everyday` beats twice.

## Icons

Every icon animates its own verb: a browser icon assembles its blocks, a phone icon's island expands
like a live notification, a database icon drops a packet through each layer, a flame burns, a pen
draws its curve, a hammer swings and flashes on impact, a shield fills and ticks, an up arrow leaves
a launch trail, the sound icon's bars dance only while audio is on, the Why icon turns `?` into `!`.
