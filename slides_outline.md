# PastForward Meeting Slides Outline
## "Finding Political Memory: Word Embeddings for the PastForward Project"

### Slide 1: Title
- Finding Political Memory: Word Embeddings for the PastForward Project
- [Your name, date, meeting context]

### Slide 2: Data Overview
- 4 countries: Denmark, Finland, Norway, Sweden
- 68 Facebook pages (all parliamentary parties + leaders)
- 26,388 posts, 215,058 comments
- 12-month window per country, ending on election day

### Slide 3: The Hindsight Dictionary
- 61 English seed terms in 3 categories:
  - Conceptual (memory, tradition, heritage...)
  - Temporal markers (past, decade, "years ago"...)
  - Phrasal ("bring back", "old days", "in hindsight"...)
- Translated to 4 Nordic languages (96-187 entries each)
- Applied as filter: post matches if it contains 1+ terms
- Result: 4,583 posts = 17.4% of all posts

### Slide 4: So we have the posts. Now what?
- We know WHICH posts talk about the past
- But WHAT pasts are they talking about?
- How do we find out without reading 4,583 posts in 4 languages?

### Slide 5: What are word embeddings?
- Train a model on text
- Words that keep similar company end up close together
  in a mathematical space
- Not synonyms — contextual neighbours
- Example: "tradition" ends up near "heritage", "kulturarv", "bevare"
  because they appear in the same kinds of posts
- [Simple 2D diagram showing a few word clusters]

### Slide 6: A concrete example
- Sweden's model places these four words close together:
  - olof_palme (assassinated PM, 1986)
  - anna_lindh (assassinated foreign minister, 2003)
  - fadime_sahindal (honour killing victim, 2002)
  - raoul_wallenberg (Holocaust rescuer, disappeared 1945)
- Four murdered individuals = Sweden's dominant political memory
- The dictionary didn't ask for this. The model surfaced it.

### Slide 7: What this gives us
- Dictionary = "which posts talk about the past?"
- Embeddings = "what past is each country talking about?"
- Surfaces meaning we didn't put in the dictionary
- Each country has a distinctive memory profile:
  - Denmark: geopolitics (Nord Stream, Cold War)
  - Finland: indigenous rights, outdated legislation
  - Sweden: assassinations, Holocaust
  - Norway: 22 July attacks, racism

### Slide 8: Under the hood
- One Word2Vec model per country (not blended)
  - Captures what "tradition" means in Danish vs Finnish discourse
- Parameters:
  - 100 dimensions per word (enough for nuance, fits our corpus)
  - Window of 5 words (standard for semantic similarity)
  - Min 3 occurrences (filters noise)
  - 50 training passes (10x default — small corpus needs more)
- Preprocessing: lowercase, stopwords out, multi-word names joined

### Slide 9: From vectors to findings
- For each dictionary term: retrieve 20 nearest neighbours
- Keep only words connected to 2+ dictionary terms
  (filters noise from random one-off similarities)
- Composite score = (# connections) x (mean similarity)
  - Rewards breadth over flukey closeness to one term
- Manual curation pass for remaining noise

### Slide 10: Live demo
- "Let me show you."
- [Switch to dashboard URL]
