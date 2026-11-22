# Puzzle-tips articles for bgameworld.com/tips/. Original writing for BGameWorld.
# Each section is (heading, [paragraphs or ("ul", [items])]).

ARTICLES = [
{
 "slug": "best-first-guess-five-letter-word-game",
 "title": "How to choose a strong first guess in a five-letter word game",
 "desc": "Why some opening words tell you far more than others, and how to pick a first guess that sets up a fast solve in Wordezy.",
 "game": ("Wordezy", "https://wordezy.bgameworld.com", "/games/wordezy/"),
 "lede": "Your first guess in a five-letter word game is the only one you make knowing nothing at all. That makes it the easiest guess to plan in advance, and the one that most affects how quickly you finish.",
 "sections": [
  ("A first guess is a question, not an answer", [
   "It is tempting to treat the opening word as a lucky shot. In practice the chance of hitting the answer on guess one is tiny, so the real job of the first word is to ask the puzzle as much as possible. Every tile that comes back green, yellow or grey removes a slice of the possible answers.",
   "A good opener is one where every result is useful. If the word comes back all grey, you have still learned that five common letters are missing, which rules out a huge share of the dictionary.",
  ]),
  ("Use common letters, and use five different ones", [
   "English letters are not used equally. In ordinary text, E, T, A, O, I, N, S, R and H turn up far more often than letters such as J, Q, X and Z. An opening word built from common letters is more likely to light up tiles, and every lit tile narrows the field.",
   "Repeated letters waste space. A word like EERIE only tests three different letters, while a word with five different letters tests five. Save double letters for later, when you have a reason to suspect them.",
  ]),
  ("Balance vowels and consonants", [
   "Almost every five-letter answer has at least one vowel, so learning which vowels are present is valuable. But a word made almost entirely of vowels tells you little about the consonants that give a word its shape. Most strong openers contain two or three vowels and two or three common consonants.",
   ("ul", [
    "Two or three vowels: enough to locate the vowel sound of the answer.",
    "Common consonants such as R, S, T, L and N: they appear in a large share of words.",
    "No repeated letters: five letters tested, not four.",
   ]),
  ]),
  ("Think about position, not just letters", [
   "Letters have favourite places. Many English words start with S, C, B or T, and many end with E, Y, T or R. A green tile is worth more than a yellow one, so an opener that puts common letters in their common positions tends to earn more greens.",
   "You do not need to memorise statistics. Simply ask: does this letter often sit here? A word that ends in E or Y, for example, is placing a common ending letter where it often belongs.",
  ]),
  ("Pick one opener and stick with it", [
   "Changing your first word every day feels creative, but using the same strong opener has real advantages. You learn what its results usually mean, you stop spending time deciding, and your second guesses get better because you have seen the same patterns many times.",
   "Some players use a fixed pair: a first word and a second word that between them cover ten different common letters. If the first word comes back almost empty, the second one fills in the gaps without any extra thought.",
  ]),
  ("What to do after the first guess", [
   "The second guess is where the skill really shows. If you have several yellow tiles, move them to new positions. If you have greens, keep them. If almost nothing lit up, play a second word made of untried common letters rather than guessing wildly at the answer.",
   "When only a handful of answers remain, it can be smarter to play a word that cannot be the answer but tests the letters that separate the remaining options. One clean test often saves two guesses later.",
  ]),
  ("A quick checklist", [
   ("ul", [
    "Five different letters.",
    "Two or three vowels.",
    "Common consonants in common positions.",
    "The same opener every day, so you learn its patterns.",
    "A planned second word for the days the first one comes back grey.",
   ]),
  ]),
 ],
},
{
 "slug": "word-ladder-puzzles-history-and-strategy",
 "title": "Word ladders: where they came from and how to solve them",
 "desc": "The Victorian word game that became the modern word ladder, and practical strategies for reaching the target word in as few steps as possible.",
 "game": ("Wordezy Ladder", "https://wordezy-ladder.bgameworld.com", "/games/wordezy-ladder/"),
 "lede": "A word ladder asks you to turn one word into another by changing a single letter at a time, with every step a real word. It is one of the oldest word puzzles still played today, and one of the most satisfying to get right.",
 "sections": [
  ("A puzzle from the 1870s", [
   "The word ladder was popularised by Lewis Carroll, the author of Alice's Adventures in Wonderland, who published a series of these puzzles under the name Doublets in the late 1870s. His challenge was simple: link two words of the same length, changing one letter at a time, using as few links as possible.",
   "The idea has stayed almost unchanged ever since. It has appeared in newspapers, school classrooms and puzzle books for well over a century, and the daily ladder on BGameWorld follows the same rules Carroll used.",
  ]),
  ("Start by comparing the two words", [
   "Before you change anything, line up the start word and the target word letter by letter. Any position where they already match can usually be left alone. Any position where they differ will need at least one change, which gives you a quick idea of the shortest possible route.",
   "For four-letter words that differ in every position, you will need at least four moves. If the par for the puzzle is higher, some letters will need to change more than once, or you will need a detour through a helpful middle word.",
  ]),
  ("Vowels are the hinges", [
   "Changing a vowel often opens up many more real words than changing a consonant. Words with the same consonants and a different vowel, such as BAT, BET, BIT and BUT, form natural stepping stones. If you feel stuck, try swapping the vowel first and see what new words appear.",
  ]),
  ("Work backwards from the target", [
   "It is often easier to find the second-to-last word than the second word. Ask yourself which real words are one letter away from the target. Then ask which of those is closest to where you are now. Building the ladder from both ends usually reveals the middle.",
  ]),
  ("Common traps", [
   ("ul", [
    "Changing the letters strictly from left to right. The best order depends on which in-between words exist.",
    "Fixing a letter too early. Sometimes a letter must change away from the target and back again to make room for a real word.",
    "Forgetting less common but ordinary words. Words like FORD, SLAT or WREN are valid steps even if you rarely use them.",
   ]),
  ]),
  ("A worked example", [
   "To turn COLD into WARM, one route is COLD, CORD, CARD, WARD, WARM. Each step changes one letter and every word is ordinary English. Notice that the R and the A arrive early, because they are shared with useful middle words, and the W and M come last.",
   "Not every pair of words has such a tidy route. When a ladder resists you, try a different first change rather than pushing harder in the same direction.",
  ]),
  ("Practise with short ladders", [
   "Three- and four-letter ladders are the best way to build the skill, because short words have so many neighbours. Once moving between them feels natural, five-letter ladders, which have far fewer neighbours, become much less intimidating.",
  ]),
 ],
},
{
 "slug": "word-search-tips-find-words-faster",
 "title": "Ten habits that make you faster at word searches",
 "desc": "Practical scanning techniques for word search puzzles, from hunting rare letters to reading the grid backwards.",
 "game": ("Wordezy Search", "https://wordezy-search.bgameworld.com", "/games/wordezy-search/"),
 "lede": "Word searches look like a test of patience, but fast solvers rely on a few simple habits. Here are ten that make the biggest difference, whether you are racing the clock or just want to finish without getting stuck on the last word.",
 "sections": [
  ("1. Scan for rare letters first", [
   "Letters such as Q, Z, X, J and K are uncommon in most grids. If a word on your list contains one, find that letter in the grid and check the squares around it. There are usually only a few places it can be.",
  ]),
  ("2. Search for pairs, not single letters", [
   "Looking for the letter E is hopeless, because there are dozens. Looking for the pair E then X, side by side in any direction, is much faster. Pick the least common two-letter combination in the word and hunt for that.",
  ]),
  ("3. Do the longest words early", [
   "Long words cross a large part of the grid, so they are easier to spot. Finding them also crosses out many letters, which makes the remaining short words stand out.",
  ]),
  ("4. Remember all eight directions", [
   "Words can run across, down, diagonally and backwards. If a word seems missing, it is very often reversed or diagonal. Make a deliberate pass reading right to left and bottom to top.",
  ]),
  ("5. Work through the grid in strips", [
   "Jumping around the grid at random means you look at the same area again and again. Instead, move through it in horizontal strips of two or three rows, checking each strip carefully before moving on.",
  ]),
  ("6. Use the theme", [
   "Themed word searches give you a head start. If the theme is the kitchen, you can expect words like SPOON or OVEN, so you already know which letter shapes to look for before you have read the list.",
  ]),
  ("7. Read the word list once, properly", [
   "Before you start, read the whole list slowly. Your brain will then recognise words as you pass them while hunting for something else, a bit like hearing your name across a noisy room.",
  ]),
  ("8. Change your focus when stuck", [
   "Staring at one patch for a long time makes letters blur together. Move to a different word for a minute and come back. Fresh eyes often spot the missing word immediately.",
  ]),
  ("9. Watch for shared letters", [
   "Words in a grid often cross each other. When you find a word, look at the letters around it: another word frequently starts or ends inside the one you just found.",
  ]),
  ("10. Keep track of what is left", [
   "Near the end, check which words remain and how long they are. A three-letter word hides more easily than a nine-letter one, so leave the short ones until you have cleared the clutter.",
  ]),
 ],
},
{
 "slug": "water-sort-puzzle-strategy-guide",
 "title": "Water sort puzzles: a beginner's guide to the logic",
 "desc": "How colour sorting puzzles work, why an empty tube is your most valuable tool, and how to plan pours so you never get stuck.",
 "game": ("Sortezy", "https://sortezy.bgameworld.com", "/games/sortezy/"),
 "lede": "In a water sort puzzle, coloured layers are mixed up across glass tubes and you pour them until each tube holds a single colour. It looks relaxing, and it is, but the harder levels reward real planning.",
 "sections": [
  ("The rules in one paragraph", [
   "You can pour from one tube into another only if the receiving tube is empty or its top colour matches the colour you are pouring, and only as much as will fit. The puzzle is solved when every tube is either full of one colour or completely empty.",
  ]),
  ("Your empty tube is your most valuable space", [
   "An empty tube can accept any colour, which makes it the most flexible space on the board. Filling it early with something that has nowhere better to go is the most common way to get stuck. Keep at least one tube empty for as long as you can, and use it only when a pour clearly moves the puzzle forward.",
  ]),
  ("Look underneath before you pour", [
   "Every pour reveals what was hiding below. Before choosing a move, check what it will uncover. A pour that exposes a colour you can immediately use is usually better than one that simply looks tidy.",
   "On BGameWorld's daily Sortezy only the top colour of each tube is visible, so each pour is also a small discovery. That makes it even more important to keep space free for surprises.",
  ]),
  ("Finish tubes one at a time", [
   "A tube that is complete is out of play for good. Completing tubes reduces the number of things you have to think about, so it is usually worth finishing one tube before spreading colours around several.",
  ]),
  ("Plan the endgame", [
   "Near the end, most mistakes come from rushing. Count how many layers of each colour remain and where they are. Often there is only one order that works, and a few seconds of thought saves several wasted moves.",
   ("ul", [
    "Count the remaining layers of each colour.",
    "Decide which tube each colour will finish in.",
    "Pour into the finishing tubes last, when nothing is left on top of them.",
   ]),
  ]),
  ("Is every puzzle solvable?", [
   "Randomly mixed tubes are not always solvable. Every Sortezy puzzle is checked by a solver before it is shown, so a solution always exists. If you are stuck, the problem is the order of your earlier moves, not the puzzle, and undo or a restart will get you out.",
  ]),
  ("Why the move count matters", [
   "Anyone can finish an easy board with enough pours. Solving it in close to the minimum number of moves is the real challenge, and it is a good measure of how well you planned. Try a puzzle twice: once to finish it, and once to finish it efficiently.",
  ]),
 ],
},
{
 "slug": "how-to-unscramble-words-anagram-tips",
 "title": "How to unscramble words: techniques that actually work",
 "desc": "Simple, reliable methods for solving anagram and word scramble puzzles, from spotting endings to rearranging tiles.",
 "game": ("Wordezy Scramble", "https://wordezy-scramble.bgameworld.com", "/games/wordezy-scramble/"),
 "lede": "Some people see the answer to a word scramble instantly. Most of us need a method. The good news is that a few techniques solve the large majority of scrambles quickly, and they get faster with practice.",
 "sections": [
  ("Start with the ending", [
   "English words often end in a small set of letter groups: -ING, -ED, -ER, -LY, -EST, -TION and -NESS among them. If those letters are present, set them aside. A seven-letter scramble with I, N and G becomes a four-letter puzzle, which is far easier.",
  ]),
  ("Then try common beginnings", [
   "Words also start in predictable ways. Pairs such as TH, CH, SH, ST, PR, BR and GR appear at the start of many words. Pull out a likely pair and see whether the remaining letters form something familiar.",
  ]),
  ("Separate vowels from consonants", [
   "Writing the vowels in one group and the consonants in another helps you see the skeleton of the word. Most English words alternate vowels and consonants in fairly regular patterns, so you can start trying shapes like consonant, vowel, consonant, consonant, vowel.",
  ]),
  ("Shuffle on purpose", [
   "The order the letters arrive in is random, but your brain treats it as meaningful and keeps reading the same false words. Shuffling the tiles breaks that pattern. If a word will not come after a few seconds, shuffle twice before you think again.",
  ]),
  ("Look for little words inside", [
   "Long words are often built from shorter ones. Spotting a small word such as AND, OUR or PEN inside the letters can unlock the whole thing. Compound words, such as SUNFLOWER, split neatly once you find the first half.",
  ]),
  ("A worked example", [
   "Take the letters G, N, I, K, L, A, W. The I, N and G suggest an -ING ending. That leaves K, L, A and W, which can only make one sensible word: WALK. Put the pieces together and you have WALKING.",
   "Or take D, N, I, W, W, O. Two Ws and an O suggest a W at the start and an OW sound somewhere. Trying WIN first leaves D, O and W, which completes WINDOW.",
  ]),
  ("When you really are stuck", [
   ("ul", [
    "Say the letters out loud. Hearing them can trigger a word that looking does not.",
    "Try putting each letter first in turn, one at a time.",
    "Take a short break. Answers often appear the moment you look away.",
   ]),
  ]),
 ],
},
{
 "slug": "false-friends-words-that-trick-language-learners",
 "title": "False friends: words that look familiar but mean something else",
 "desc": "A tour of common false friends across Spanish, French, German, Italian and Portuguese, and why they catch out so many language learners.",
 "game": ("Lingoezy", "https://lingoezy.bgameworld.com", "/games/lingoezy/"),
 "lede": "A false friend is a word that looks or sounds like a word in another language but means something different. They are some of the most memorable mistakes language learners make, and some of the most useful words to learn.",
 "sections": [
  ("Why false friends exist", [
   "Many European languages share roots in Latin, and English borrowed heavily from French and Latin over the centuries. Over time, words that started out with the same meaning drifted apart in different languages. Others look alike purely by coincidence. Either way, the familiar spelling invites a confident but wrong guess.",
  ]),
  ("Twelve classic examples", [
   ("ul", [
    "Spanish embarazada means pregnant, not embarrassed.",
    "Spanish éxito means success, not exit.",
    "Spanish constipado means having a cold, not constipated.",
    "Spanish carpeta means a folder, not a carpet.",
    "French librairie means a bookshop, not a library.",
    "French actuellement means currently, not actually.",
    "French blesser means to wound, not to bless.",
    "German Gift means poison, not a present.",
    "German Rock means a skirt, not a rock.",
    "German bekommen means to get or receive, not to become.",
    "Italian camera means a room, not a camera.",
    "Portuguese puxar means to pull, though it looks like push.",
   ]),
  ]),
  ("True friends are real too", [
   "Not every look-alike is a trap. Many words really do mean the same thing across languages: hotel, chocolate, radio and many technical words are good examples. That is what makes false friends tricky. You cannot simply distrust every familiar word, so you have to learn which ones to watch.",
  ]),
  ("How to stop being fooled", [
   ("ul", [
    "Pay attention to context. If a sentence would be strange with the English meaning, the word may be a false friend.",
    "Learn false friends in pairs, alongside the word that actually means what you expected.",
    "Make the mistake once, on purpose, in a game. Being caught out is one of the best ways to remember.",
   ]),
  ]),
  ("Related languages help each other", [
   "If you know one Romance language, you can often reason your way through another. Spanish, Portuguese and Italian share many roots, so a word you know in one frequently hints at the meaning in another. Just remember that the shared root can also be where the false friend hides.",
  ]),
  ("Practise with a game", [
   "Lingoezy on BGameWorld mixes false friends with true friends in random directions between English, Spanish, French, Portuguese, German and Italian. Every answer comes with an explanation, so each mistake teaches you something you are likely to remember.",
  ]),
 ],
},
{
 "slug": "how-to-date-an-old-photograph",
 "title": "How to date an old photograph: clues hiding in plain sight",
 "desc": "The visual clues that help you guess when and where an old photo was taken, from clothing and cars to the photograph itself.",
 "game": ("When & Where", "https://when-and-where.bgameworld.com", "/games/when-and-where/"),
 "lede": "Every photograph carries clues about when and where it was taken. Historians, archivists and family researchers use the same small set of clues again and again, and once you know them you will start noticing them everywhere.",
 "sections": [
  ("Start with the photograph itself", [
   "The type of image is a strong first clue. Photography became practical in the late 1830s, and early processes produced very distinctive images on metal and glass. For most of the following century, ordinary photographs were black and white. Colour film existed from the 1930s, but colour snapshots only became everyday in many countries from the 1960s and 1970s.",
   "So a crisp, natural-looking colour street photo points to the second half of the twentieth century or later, while a faded black and white image could come from almost any time before then. Combine this with other clues to narrow it down.",
  ]),
  ("Clothes and hairstyles", [
   "Fashion changes quickly and is easy to see. Long skirts and hats on almost everyone suggest an earlier period, while very wide collars, flared trousers or particular hairstyles can point to a specific decade. Look at ordinary people in the background as well as the main subject, because they are less likely to be dressed for a special occasion.",
  ]),
  ("Vehicles are excellent clocks", [
   "Cars, buses, trams and bicycles change shape over time. Horse-drawn carts with no motor vehicles in sight suggest an early date. Rounded car bodies, tall narrow cars or very boxy designs each belong to different eras. Even if you cannot name the model, the general shape tells you a lot.",
  ]),
  ("Read every piece of writing", [
   "Shop signs, posters, street names and number plates are often the fastest way to find the place. The language and the alphabet narrow the country immediately, and the style of the lettering can hint at the period. Advertising for a particular product or event can sometimes date a photo almost exactly.",
  ]),
  ("Look at the street itself", [
   ("ul", [
    "Which side of the road are vehicles driving on?",
    "Are there tram lines, overhead wires or street lamps of a particular style?",
    "What are the buildings made of, and how tall are they?",
    "Are there plants or landscapes typical of a climate or region?",
   ]),
  ]),
  ("Guessing the day of the week", [
   "This is the hardest clue, and often there is no answer at all. But crowds in their best clothes heading to a place of worship, busy markets, or empty office streets can all suggest a particular day. When there is nothing to go on, a guess costs you little.",
  ]),
  ("Put the clues together", [
   "No single clue is reliable on its own. A photo can show an old building next to a new car, or a person wearing their grandparents' coat. The skill is in combining evidence: the photographic process, the clothes, the vehicles and the writing should all point to the same period and place.",
  ]),
 ],
},
{
 "slug": "build-a-daily-puzzle-habit",
 "title": "How to build a daily puzzle habit that lasts",
 "desc": "Simple ways to make a short daily puzzle a regular, enjoyable part of your day, and to keep a streak going without it feeling like a chore.",
 "game": ("the daily puzzles", "https://bgameworld.com/", "/games/"),
 "lede": "Daily puzzles work best as a small, regular routine. A few minutes each day is easy to fit in, gives you something to look forward to, and gives you a shared topic with friends who play the same puzzle.",
 "sections": [
  ("Why daily puzzles suit a routine", [
   "A daily puzzle is the same for everyone and changes once a day. That makes it naturally short and naturally regular: there is one to do, and then you are done until tomorrow. Many people find that this limit is what keeps the habit enjoyable instead of overwhelming.",
  ]),
  ("Attach it to something you already do", [
   "Habits stick best when they are tied to an existing routine. Solve your puzzle with your morning coffee, on the bus, or just before bed. After a couple of weeks, the routine itself reminds you to play.",
  ]),
  ("Keep it small", [
   "Start with one puzzle you enjoy rather than ten you feel you should do. Once that one is automatic, add another. A short session you look forward to is worth more than a long one you avoid.",
  ]),
  ("Use streaks kindly", [
   "Streaks are motivating, but they can also turn a game into a chore. Treat a streak as a nice bonus, not an obligation. If you miss a day, start again without guilt. The point is to enjoy the puzzles, not to protect a number.",
  ]),
  ("Play with other people", [
   "Because everyone gets the same daily puzzle, it is easy to compare results with friends or family. Sharing a result grid without spoilers, or comparing who needed fewer moves, turns a solo habit into a small social ritual.",
  ]),
  ("Mix the kinds of puzzle", [
   ("ul", [
    "Word puzzles, such as Wordezy, Wordezy Ladder and Warmezy, exercise vocabulary and spelling.",
    "Logic puzzles, such as Sortezy, Linkezy and Mergezy, reward planning ahead.",
    "Trivia, such as When & Where, rewards curiosity and close observation.",
   ]),
   "Switching between types keeps things fresh and gives you something to look forward to each day.",
  ]),
  ("Learn from the hard days", [
   "Some days the puzzle will beat you. Those are often the days you learn the most. After a tough one, read the explanation or the guide, and notice what you would do differently. The next similar puzzle will feel easier.",
  ]),
 ],
},
]

# Extra sections, merged into the articles above (kept separate to keep each article readable).
EXTRA = {
 "best-first-guess-five-letter-word-game": [
  ("Hard mode changes the plan", [
   "Some players choose to play with a rule that every later guess must use the hints already found: greens stay where they are and yellows must appear somewhere. Under that rule you cannot play a pure testing word, so the first two guesses matter even more. A strong, varied opener gives you more freedom for the rest of the game.",
  ]),
  ("Beware of the near-miss trap", [
   "Sometimes four letters turn green and one stays stubbornly unknown, with many possible fillers: think of patterns where only the first letter differs, like _ATCH or _IGHT. Guessing them one by one can burn every remaining turn. When you see that pattern early, spend a guess on a word that tests several of the candidate letters at once, even though it cannot be the answer.",
   "This is the single most common way players lose with five or six greens almost in hand. Recognising the trap a guess earlier is often the difference between a win and a miss.",
  ]),
  ("Keep notes in your head, not just on the keyboard", [
   "The coloured keyboard shows which letters you have tried, but not where yellows have already been. Before each guess, remind yourself of the positions each yellow letter has already occupied. Placing a yellow letter in a spot it has already failed in is a wasted guess.",
  ]),
 ],
 "word-ladder-puzzles-history-and-strategy": [
  ("Why some ladders are much harder", [
   "Short words have many neighbours. A common three-letter word may be one letter away from a dozen others, so there are lots of routes. Longer words have far fewer neighbours, which means a five-letter ladder can have only one or two possible routes. That is why the same puzzle feels easy at four letters and fiendish at five.",
   "Some letters are also lonelier than others. Words containing J, Q, X or Z usually have very few neighbours, so if the start or target contains one, deal with it early, while you still have options.",
  ]),
  ("Use the par as a hint", [
   "The par tells you the fewest moves the ladder can be solved in. If the start and target differ in four positions and par is four, every move must change a letter straight to its final value. If par is five or six, at least one letter has to make a detour. Knowing this before you start stops you from searching for a direct route that does not exist.",
  ]),
  ("Make your own ladders", [
   "A good way to improve is to build ladders for friends. Pick two words, find a route, then try to find a shorter one. Setting puzzles teaches you which words make good stepping stones, and you will start to recognise them instantly when you play.",
  ]),
 ],
 "word-search-tips-find-words-faster": [
  ("Why these habits work", [
   "Our eyes are good at spotting patterns but poor at checking every square systematically. All of the habits above do the same thing: they give your eyes something specific and unusual to look for, instead of asking them to read the whole grid. A rare letter, a long word or a two-letter pair stands out; a common single letter does not.",
  ]),
  ("Practise speed separately from finishing", [
   "If you want to get faster, time yourself on a few grids and note which words took longest. Usually they share a feature: they were short, backwards or diagonal. Next time, make a deliberate pass for exactly that kind of word before it becomes the last one standing.",
  ]),
  ("Make it a game with others", [
   "Word searches are easy to share. Two people can race on the same grid, or take turns finding words. Because every player gets the same daily grid on BGameWorld, you can compare times with friends without anyone seeing the answers.",
  ]),
 ],
 "water-sort-puzzle-strategy-guide": [
  ("A useful way to think about each move", [
   "Before every pour, ask two questions. Will this reveal something useful? And will it leave me with at least one free space? If the answer to both is no, look for a different move. This simple check prevents most dead ends on harder levels.",
  ]),
  ("Common beginner mistakes", [
   ("ul", [
    "Pouring a single layer into an empty tube just because it is possible.",
    "Leaving a colour split across three or four tubes instead of gathering it.",
    "Burying a nearly finished tube under a different colour.",
    "Restarting too quickly instead of undoing one or two moves.",
   ]),
  ]),
  ("Why sorting puzzles feel calming", [
   "Sorting puzzles have a clear goal, steady visible progress and no time pressure unless you choose it. Each completed tube is a small, tidy success. That combination makes them a popular way to unwind, while the harder levels still give planners plenty to think about.",
  ]),
 ],
 "how-to-unscramble-words-anagram-tips": [
  ("Common letter patterns to recognise", [
   ("ul", [
    "Double letters such as LL, SS, EE and OO often sit in the middle or at the end of a word.",
    "QU almost always travels together, so treat it as one piece.",
    "CK, PH, WH and GH are common consonant pairs that rarely split.",
    "A final E often makes the vowel before it long, as in KITE or HOPE.",
   ]),
   "Treating these pairs as single blocks reduces the number of pieces you are juggling, which makes the word easier to see.",
  ]),
  ("Why one letter set can have several answers", [
   "Some letter sets spell more than one real word. LISTEN, SILENT and ENLIST are all the same six letters, for example. In a scramble with one intended answer, if your word is real but not accepted, keep the same letters and look for a different arrangement before you assume you are wrong.",
  ]),
  ("Build the skill over time", [
   "Anagram solving improves quickly with practice, because your brain starts to recognise common chunks automatically. Short daily practice is more effective than occasional long sessions. Five scrambles a day, from short to long, is a good routine.",
  ]),
 ],
 "false-friends-words-that-trick-language-learners": [
  ("Partial false friends", [
   "Some words are only partly false. They share one meaning with the English look-alike but have others as well, or are used in different situations. These are harder to spot than outright false friends because the familiar meaning sometimes works and sometimes does not. A good dictionary entry, with example sentences, is the best guide.",
  ]),
  ("False friends between other languages", [
   "False friends are not only an English problem. Speakers of Spanish and Portuguese, or of Spanish and Italian, trip over each other's words too, because the languages are close enough to look familiar but have drifted apart in places. Learning a third language often means learning a new set of false friends between the two you already know.",
  ]),
  ("Turning mistakes into memories", [
   "The best thing about false friends is how memorable they are. A word that once embarrassed you is unlikely to fool you twice. Keep a short list of the ones that caught you out, and review it occasionally. You will be surprised how quickly the list stops growing.",
  ]),
 ],
 "how-to-date-an-old-photograph": [
  ("Use what is missing", [
   "Absences are clues too. A busy city street with no cars at all suggests an early date. A modern-looking street with no mobile phones, satellite dishes or plastic signs suggests the photo is older than it first appears. Ask yourself what you would expect to see today, and notice when it is not there.",
  ]),
  ("Practise with your own family photos", [
   "Family albums are a great training ground, because someone can usually tell you the real answer. Before asking, make your own estimate from the clothes, cars and photo quality, then check how close you were. Over time your estimates get noticeably sharper.",
  ]),
  ("Close is good enough", [
   "Even experts often date photographs to a range of years rather than an exact date. In a game like When & Where, points are awarded for getting close, so a sensible estimate based on several clues beats a confident guess based on one.",
  ]),
 ],
 "build-a-daily-puzzle-habit": [
  ("Set a time limit you like", [
   "Decide roughly how long you want to spend, such as ten minutes, and let the puzzles fit into that time. A clear limit stops the habit from growing until it feels like work, and makes it easy to start because you know exactly what you are signing up for.",
  ]),
  ("Track progress in a way that feels good", [
   "Many daily games show statistics such as your win rate, average guesses or best time. Look at them occasionally to see how far you have come, but avoid checking after every game. Improvement is easier to see over weeks than over days.",
  ]),
  ("A simple weekly routine", [
   ("ul", [
    "Weekdays: one or two short puzzles at a fixed time.",
    "Weekend: try a game you do not usually play, or a harder level.",
    "Once a week: read a guide or tip for a game you find difficult.",
   ]),
   "Small, regular sessions like these are easy to keep up, and over a month they add up to a lot of practice.",
  ]),
 ],
}
for _a in ARTICLES:
    _a["sections"] = _a["sections"][:-1] + EXTRA.get(_a["slug"], []) + _a["sections"][-1:]
