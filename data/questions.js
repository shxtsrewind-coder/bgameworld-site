/* Today's Question archive for bgameworld.com (homepage teaser + /question/ page).
   One question a day, the same for everyone, changing at midnight UTC with the puzzles.
   The day's question is picked by position from QUESTION_EPOCH, so add new questions
   at the END only; never reorder or edit past ones (their results are stored by date).
   Each entry: [question, [up to four answers]]. */
const QUESTION_EPOCH = Date.UTC(2026, 9, 26); // 26 Oct 2026 = the first question
const QUESTIONS = [
  ["How do you start a word puzzle?", ["Vowels first", "A favourite word", "Whatever comes to mind", "Peek at the hint"]],
  ["Best time of day for today's puzzles?", ["With morning coffee", "Lunch break", "Evening wind-down", "Right before bed"]],
  ["Pen or pencil for a paper crossword?", ["Pen, bravely", "Pencil, wisely", "Whatever's nearby", "I only play online"]],
  ["Your reaction when you lose a streak?", ["Shrug, start again", "Quiet sadness", "Never speak of it", "What streak?"]],
  ["Which would you rather solve?", ["A word puzzle", "A logic puzzle", "A trivia question", "A picture puzzle"]],
  ["Do you share your results?", ["Every single day", "Only the good ones", "Just with family", "Never"]],
  ["Most satisfying puzzle moment?", ["The first guess lands", "The last piece clicks", "Beating my best time", "Beating a friend"]],
  ["How many tries feels like a win?", ["One, obviously", "Two or three", "Any finish is a win", "Losing is fun too"]],
  ["Hints: yes or no?", ["Never, it's cheating", "Only when stuck", "Early and often", "I don't play to suffer"]],
  ["Best snack for puzzle time?", ["Something crunchy", "Something sweet", "Just a drink", "No snacks, full focus"]],
  ["Where do you play most?", ["On the sofa", "On the commute", "At my desk", "In bed"]],
  ["Which decade's photos would you guess best?", ["1950s", "1970s", "1990s", "2000s"]],
  ["The perfect puzzle length?", ["Under 2 minutes", "About 5 minutes", "10–15 minutes", "As long as it takes"]],
  ["You get a word wrong. You...", ["Laugh it off", "Look it up", "Blame the dictionary", "Pretend it didn't happen"]],
  ["Which superpower helps most with puzzles?", ["Perfect memory", "Seeing patterns", "Endless patience", "Super speed"]],
  ["Do you play the same games every day?", ["Yes, same order", "Same games, any order", "Whatever I feel like", "I try something new"]],
  ["Best way to learn a new word?", ["Reading", "Puzzles and games", "Conversation", "Looking it up on purpose"]],
  ["Your puzzle style?", ["Fast and fearless", "Slow and careful", "Chaotic but lucky", "Methodical lists"]],
  ["Which would you rather win?", ["A trophy", "Bragging rights", "A tiny prize", "Nothing, just the fun"]],
  ["Weekend puzzles should be...", ["Harder", "Easier", "Longer", "Exactly the same"]],
  ["What do you do while a puzzle loads?", ["Stretch", "Sip a drink", "Plan my first move", "It's already loaded"]],
  ["Favourite kind of word?", ["Long and fancy", "Short and punchy", "Funny-sounding", "Rare and obscure"]],
  ["Who in your house is the puzzle champion?", ["Me", "Someone else", "We're tied", "I play alone"]],
  ["How do you feel about timers?", ["Love the pressure", "Fine, I ignore them", "They stress me out", "Hide them, please"]],
  ["Which travel spot would you love a photo puzzle of?", ["A big city", "A tiny village", "A beach", "Mountains"]],
  ["Sound on or off?", ["Always on", "Always off", "Depends where I am", "What sound?"]],
  ["The best puzzle is one that...", ["Teaches me something", "Makes me laugh", "Really challenges me", "I finish fast"]],
  ["Dark mode or light mode?", ["Dark, always", "Light, always", "Follow my device", "Never thought about it"]],
  ["If puzzles were a food, today's would be...", ["Toast: simple", "Spaghetti: tangled", "Cake: a treat", "Chilli: spicy"]],
  ["How did you find BGameWorld?", ["A friend", "Social media", "A search", "Can't remember"]],
  ["Which would you rather unscramble?", ["Animal names", "City names", "Food words", "Long science words"]],
  ["Best feeling in a logic puzzle?", ["The first safe move", "Spotting the trick", "The final fill", "Undo saving me"]],
  ["Do you read the instructions?", ["Every word", "A quick skim", "Only if stuck", "Never"]],
  ["Morning person or night owl?", ["Morning person", "Night owl", "Afternoon hero", "Depends on coffee"]],
  ["Which game rule would you add everywhere?", ["One free hint", "A practice round", "An undo button", "A 'shuffle' button"]],
  ["Biggest puzzle pet peeve?", ["Unfair clues", "Obscure words", "Tiny buttons", "Spoilers online"]],
  ["What do you do after finishing today's set?", ["Brag a little", "Go about my day", "Play another round", "Check the leaderboard"]],
  ["Which language would you most like to learn?", ["Spanish", "French", "Japanese", "Something else"]],
  ["How competitive are you, honestly?", ["Extremely", "A healthy amount", "Only with friends", "Not at all"]],
  ["Best place for a long puzzle?", ["A café", "A train", "A park bench", "My own chair"]],
  ["A new game appears. You...", ["Play it immediately", "Read about it first", "Wait for friends' reviews", "Stick to my favourites"]],
  ["Favourite season for puzzling?", ["Spring", "Summer", "Autumn", "Winter"]],
  ["Which colour should the next game be?", ["Forest green", "Sunset orange", "Ocean blue", "Berry pink"]],
  ["Would you play a daily drawing game?", ["Yes, sounds fun", "Maybe once", "I can't draw", "Only to guess others'"]],
  ["How do you handle a really hard puzzle?", ["Walk away and return", "Brute-force it", "Ask someone", "Accept defeat gracefully"]],
  ["Most-used key on your keyboard while playing?", ["Backspace", "Enter", "E", "Whatever the hint key is"]],
  ["Ideal puzzle buddy?", ["A pet on my lap", "A friend beside me", "A group chat", "Nobody, peace and quiet"]],
  ["Which history era would you most like to see photos from?", ["Ancient wonders", "Victorian streets", "1960s cities", "The 1990s"]],
  ["What makes a game feel fair?", ["Clear rules", "Good hints", "Same puzzle for everyone", "No time pressure"]],
  ["Best reward for a long streak?", ["A badge", "A special puzzle", "Bragging rights", "The streak itself"]]
];
function questionFor(dateStr) {
  const i = Math.floor((Date.parse(dateStr + "T00:00:00Z") - QUESTION_EPOCH) / 864e5);
  return { index: i, question: QUESTIONS[((i % QUESTIONS.length) + QUESTIONS.length) % QUESTIONS.length] };
}
