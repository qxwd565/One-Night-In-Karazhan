# Date-first Karazhan card data

Each original `data/<ID>.json` contains a complete launch-era specification and sparse, date-keyed changes. The 57 original IDs and DBF mappings are unchanged. Core cards, reprints, older same-name entities and adventure-only versions are not substituted.

A missing field in a delta retains its earlier value. `__remove` explicitly removes a field. Zero, false, null, empty strings, empty arrays and absence remain distinct. Minions use attack/health, weapons attack/durability, and spells have no combat-stat placeholders. Runic Egg and Animated Shield really have zero attack even when the XML omits a zero-valued ATK tag. The generic tests also cover hero armor versus base-hero health, locations, enchantments and type changes.

Display line breaks are exactly `<br></br>`. Raw Korean and English archive strings are retained without modification. Native `[x]`, numeric `$`/`#` markers and the identified keyword-punctuation `&` marker are display controls, not extra gameplay effects. The 32.0 movement of weapon durability from tag 187 to tag 45 is a storage migration, not a weapon nerf.

## Availability and uncertainty

The prologue and first wing establish 18 usable original entities on 2016-08-12 KST. For the remaining 39, 2016-08-19, 2016-08-26 and 2016-09-02 are verified **usable-no-later-than bounds** from weekly unlocks. An earlier ordinary-match generation date has not been established. Those dates are marked `estimated`, not promoted to verified earliest appearances. Class-challenge PvE decks, reveal dates and client preload on August 10 are excluded as ordinary-match evidence.

`fold(timeline, day)` performs exact date-key replay and returns no card before the first key. The compatibility `resolve` interface preserves earlier fallback for estimated releases unless the individual card explicitly sets `release.beforeDate: unavailable`. No such absence rule is imposed on these 39 uncertain releases. Opt-in strict lookup rejects qualified releases or baselines instead of certifying them. The `-date` reverse output has the same qualified fallback semantics as `resolve`.

## Output families

- `cards.json`, `render.json` and `history.json` remain schema 1 and work with the unchanged pinned PHP parser. They do not expose `__remove` or history schema 2. Old zero sentinels, weapon health/durability mirroring and before-release fallback are confined to this compatibility boundary.
- `cards-date.json`, `render-date.json` and `history-date.json` retain exact canonical field presence. The latter two advertise `historySchema: 2` and include release confidence and current-only field lists.
- All six files remain root siblings, preserving relative artwork URL resolution.

Edit canonical per-card JSON for future evidence-backed changes, then run `python tools/build-api.py`. Both API families are rebuilt. Immutable originals never replace an entire later canonical state. `legacyMechanicsConvention.canonicalBaseline` is the latest intrinsic keyword list at migration, not the launch list. It preserves the old current annotation convention while allowing new canonical keyword changes to propagate.

## Source preservation

`metadata/<ID>.json` preserves the exact original wrapper, current catalog entry and pinned source commit. Present-day artwork, native tags, flavor, portrait and exporter fields stay there and are not backdated. The original `data/history.json` stays byte-identical and is also copied to `tools/original-date-first-history.json`. It is noncanonical evidence, not another writable history source.

The shared-state source archive covers 234 selected client builds: 161 retained samples independently extracted for Karazhan, plus all 73 missing tagged builds inside intervals showing any Karazhan raw-state change. Every raw XML has a pinned commit URL and SHA-256. Every reconstructed card map has a separate hash. `Tag` and `ReferencedTag` remain distinct. Equal-ended intervals were not exhaustively sampled; this is not a claim to cover every live client or engine revision. Official balance records provide an independent cross-check of the selected changes.

Intrinsic abilities come from owned launch tags and explicitly identified printed keyword changes. Secret-related effects are not themselves Secrets; summoned Taunt or Stealth does not transfer that keyword to its parent. Discover is owned by Ivory Knight and Netherspite Historian. Soul Claws checks Spell Damage but does not provide it. Prince Malchezaar's formal Start of Game keyword starts with 11.0. Noncollectible rarity remains qualified because implementation tags alone do not prove dated visible rarity changes.

Functional engine fixes with unchanged printed fields are recorded in `tools/karazhan-behavior-audit.json`. They are evidence notes, not executable replay fields. Unresolved effective dates belong in `undatedEvidence`, never invented date keys.

## Validation

Run `.github/workflows/validate.yml` commands with full Git history. Missing pinned originals fail explicitly. Clean migration must reproduce every canonical file, sidecar and API bundle byte-for-byte. Tests cover IDs, membership, source numeric decoding, literal balance boundaries, sparse replay, qualified availability, zero/absence/removals, future edits, current differences, asset hashes, relative art URLs and repeated builds.

`python tools/extract-karazhan-archives.py --archive-dir <archive-directory> --require-all` re-extracts retained full XML and checks its hashes against the pooled evidence. The offline PHP fixture uses unchanged pinned parser files. No plugin, website, database or live visual renderer is modified or visually certified.
