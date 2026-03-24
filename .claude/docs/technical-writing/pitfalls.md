<!-- last_verified: 2026-03-05 -->
# Technical Writing Pitfalls

Common mistakes that waste the reader's time or create confusion.

## 1. The Wall of Text

**Problem**: Paragraphs where lists belong. The reader's eyes glaze over by sentence three.

**Fix**: If you have 3+ parallel items, use a list or table. If a paragraph is more than 4 sentences, it probably contains two ideas and should be split.

## 2. The Phantom Audience

**Problem**: Writing for an imagined beginner who doesn't exist, or an imagined expert who doesn't need docs.

**Fix**: Know who actually reads this document. For internal agent docs, the audience is the lead agent and the user — both technical, both busy. Don't explain what a REST API is. Do explain which REST conventions this project follows.

## 3. The Missing Example

**Problem**: Three paragraphs explaining a concept with no code sample.

**Fix**: Show the thing working. Then explain why. Most readers will copy the example and modify it. They'll read the explanation only if the example doesn't work.

## 4. The Stale Doc

**Problem**: Documentation that was accurate six months ago. Now it's a trap.

**Fix**: Date architecture docs. Put version numbers on API references. If you can't keep it current, delete it — no docs is better than wrong docs.

## 5. The Buried Lede

**Problem**: The critical information is in paragraph four of section three.

**Fix**: Put the most important thing first. If the document has a "Getting Started" section, it should be the first section after the intro, not after "Philosophy" and "Architecture Overview."

## 6. The Apology Tour

**Problem**: "Sorry, this is a bit complex" / "Unfortunately, you'll need to..." / "We know this isn't ideal, but..."

**Fix**: Just state the facts. The reader doesn't need your emotional support. "This requires three configuration files" is fine. They'll form their own opinions.

## 7. The Jargon Spiral

**Problem**: Using five domain-specific terms in one sentence without defining any of them.

**Fix**: Define terms on first use, or link to a glossary. One new term per sentence maximum. If a sentence requires the reader to already know the conclusion, restructure it.

## 8. The False Precision

**Problem**: "The system processes approximately 1,247.3 requests per second." (On what hardware? Under what load? Measured when?)

**Fix**: Include conditions for any performance claim. Round to meaningful precision. "~1,200 req/s on a single 4-core instance under synthetic load" is more useful than a number with spurious decimal places.

## 9. The Screenshot Novel

**Problem**: Step-by-step screenshots for a CLI tool, or screenshots of text that should be code blocks.

**Fix**: Use code blocks for anything the reader might need to copy. Screenshots are for GUIs, and even then, annotate them — a screenshot without context is just a picture.

## 10. The Infinite Scroll

**Problem**: A 500-line README that covers installation, usage, API reference, contributing guidelines, changelog, and the author's philosophy of software.

**Fix**: Split into separate documents. README is the landing page — keep it short, link to the rest. Nobody reads a 500-line README. People do click links to the specific section they need.
