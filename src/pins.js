// Pinterest RSS feeds for auto-publishing Pins.
//
// Pinterest (Settings > Create Pins in bulk > Auto-publish) reads these feeds
// and turns each new item into a Pin on the board you pick, within 24 hours.
// A Pin only appears in its feed once its time in src/pins.json has passed,
// so Pins go out a few a day instead of all at once.
//
//   /feed/pins/word.xml      Word Puzzles board
//   /feed/pins/logic.xml     Logic Puzzles board
//   /feed/pins/language.xml  Language Quizzes board
//   /feed/pins/all.xml       everything, for a single board
//
// Each item links to its answer page on bgameworld.com (the portal Pin links
// to the home page) and carries a 1000x1500 image from /social/pin/.
import pins from "./pins.json";

const SITE = "https://bgameworld.com";
const BOARDS = {
  word: ["Word Puzzles", "Free daily word puzzles from BGameWorld: Wordle-style, word ladders, scrambles, word search and more."],
  logic: ["Logic Puzzles", "Free daily logic puzzles from BGameWorld: water sort, tile merge and connect the dots."],
  language: ["Language Quizzes", "Spot the false friend: free daily translation quizzes in Spanish, French, German, Italian and Portuguese."],
  all: ["Daily Brain Puzzles", "Free daily puzzles and brain games from BGameWorld."],
};

export function pinFeed(url, now) {
  const m = url.pathname.match(/^\/feed\/pins\/(word|logic|language|all)\.xml$/);
  if (!m) return null;
  const board = m[1];
  const [name, about] = BOARDS[board];
  const items = pins
    .filter((p) => (board === "all" || p.board === board) && Date.parse(p.at) <= now)
    .sort((a, b) => Date.parse(b.at) - Date.parse(a.at));
  const x = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const body = items.map((p) => `
  <item>
    <title>${x(p.title)}</title>
    <link>${x(p.link)}</link>
    <description>${x(p.description)}</description>
    <guid isPermaLink="false">bgameworld-pin-${p.id}</guid>
    <pubDate>${new Date(p.at).toUTCString()}</pubDate>
    <enclosure url="${x(p.image)}" type="image/jpeg" length="${p.bytes}"/>
    <media:content url="${x(p.image)}" medium="image" type="image/jpeg" width="1000" height="1500"/>
  </item>`).join("");
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
  <title>BGameWorld: ${x(name)}</title>
  <link>${SITE}/</link>
  <description>${x(about)}</description>
  <language>en</language>
  <lastBuildDate>${new Date(items.length ? items[0].at : now).toUTCString()}</lastBuildDate>${body}
</channel>
</rss>
`;
  return new Response(xml, {
    headers: { "content-type": "application/rss+xml; charset=utf-8", "cache-control": "public, max-age=900", "x-robots-tag": "noindex" },
  });
}
