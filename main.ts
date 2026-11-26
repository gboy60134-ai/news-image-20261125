import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(out, { recursive: true });
const src = join(root, "entry.png");
if (!existsSync(src)) throw new Error("entry.png missing from repository");
const header = readFileSync(src).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!header.equals(pngMagic)) throw new Error("entry.png is not a PNG file");
copyFileSync(src, join(out, "entry.png"));
console.log(`copied entry.png (${statSync(src).size} bytes) to ${out}`);
