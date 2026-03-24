<!-- last_verified: 2026-03-05 -->
# Technical Writing Style Guide

## Core Principles

1. **Respect the reader's time.** They came here to solve a problem, not to admire your prose.
2. **Be correct.** A beautifully written lie is worse than an ugly truth.
3. **Be specific.** "Fast" means nothing. "~50ms p99" means something.
4. **Show, then tell.** A code example followed by a one-line explanation beats three paragraphs of theory.

## Sentence-Level Rules

- Lead with the action or the important information. "Run `make test` to verify" not "In order to verify your changes, you can run `make test`."
- Use imperative mood for instructions: "Install the package" not "You should install the package."
- One idea per sentence. If a sentence has two commas and a semicolon, it's two sentences.
- Avoid weasel words: "simply", "just", "easily", "obviously". If it were obvious, they wouldn't be reading the docs.
- Don't hedge unnecessarily. "This deletes the file" not "This should delete the file" (unless it genuinely might not).

## Structure

- **Headings**: Use them generously. Most readers are scanning.
- **Lists**: Use bullet points for unordered items, numbered lists for sequences.
- **Tables**: Use for comparisons, option references, and anything with 3+ parallel attributes.
- **Code blocks**: Always specify the language. Use inline code for file paths, commands, and identifiers.
- **Front-load**: Put the most important information first — in the document, in each section, and in each paragraph.

## Document Types

### README
- What it is (1-2 sentences)
- How to install/set up
- How to use (quick start)
- Where to find more (links)
- Keep under 100 lines when possible

### Changelog
- Group by: Added, Changed, Fixed, Removed
- One line per entry, component name first
- Breaking changes at the top, clearly marked
- Link to relevant commits or issues

### API Reference
- Every endpoint/function: signature, parameters, return value, example
- Note required vs optional parameters
- Include error responses — people spend more time debugging than succeeding

### Architecture Docs
- Start with the 30-second version (diagram + paragraph)
- Then go deeper for those who need it
- Date the document — architecture docs rot fast

## Humor Guidelines

Humor is a spice, not a main course. Rules:

1. **Maximum density**: 1-2 moments per document. Zero is fine.
2. **Deadpan delivery**: State the absurd implication as if it were mundane.
3. **Never at the reader's expense.** Laugh with them about the situation, not at them for needing docs.
4. **No emoji, no exclamation marks, no "fun" formatting.** The humor comes from the words.
5. **If you're not sure it's funny, cut it.** Unfunny attempts at humor are worse than no humor at all.

### Examples That Work

> "The timeout defaults to 30 seconds, which is generous for a database query and insufficient for a government API."

> "Setting `DEBUG=true` in production is not recommended, though it does make the logs more entertaining."

> "This module has no dependencies, a fact it is quietly proud of."

### Examples That Don't Work

> "Happy coding! 🎉" — corporate cheerfulness
> "LGTM! Ship it! 🚀" — Slack energy in a document
> "As the great philosopher once said..." — trying too hard
> Puns in headings — just don't

## Common Mistakes

| Instead of | Write |
|-----------|-------|
| "In order to" | "To" |
| "It should be noted that" | (delete, just state the thing) |
| "At this point in time" | "Now" |
| "Due to the fact that" | "Because" |
| "In the event that" | "If" |
| "A number of" | (use the actual number, or "several") |
| "Leverage" | "Use" |
| "Utilize" | "Use" |
| "Facilitate" | (say what it actually does) |
| "Robust" | (say what makes it robust) |

## Formatting Conventions

- Use `backticks` for: file paths, command names, function names, variable names, config keys
- Use **bold** for: UI elements, first use of a defined term, warnings
- Use *italics* sparingly: emphasis on a single word, book/document titles
- Use > blockquotes for: callouts, warnings, notes (prefix with **Note:** or **Warning:**)
