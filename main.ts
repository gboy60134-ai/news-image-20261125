// News-image entry for 25 November 2026 (Node 22, standard library only).
// The image is drawn once by build_image.py from the day's verified
// headlines and held in this repository as entry.png; this program copies
// it to /output/entry.png, with no network and no randomness, so both
// grader runs write the same bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
