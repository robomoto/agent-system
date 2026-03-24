<!-- last_verified: 2026-03-06 -->
# Privacy and Visibility in Community Design

## The Privacy Paradox (Acquisti & Grossklags, 2005)

People say they value privacy highly but routinely share personal information when the social context encourages it. In small communities, social pressure to share is even stronger.

**Implications:**
- Members may share address, schedule, and personal details because neighbors do — then regret it
- Opt-in with gentle defaults is better than opt-out: don't pre-populate fields, let members choose
- Allow granular control: share with community but not with search engines

## Context Collapse (Marwick & boyd, 2011)

Online platforms flatten social contexts. Information shared for one audience becomes visible to another. In neighborhood communities, context collapse happens when:
- A venting post about neighborhood noise is seen by the person making the noise
- A request for help with a personal matter is visible to work colleagues who are also neighbors
- Event RSVPs reveal social preferences (who you do and don't want to spend time with)

**Design mitigations:**
- Default to less visibility, let members opt into more
- Consider who might see something before making it visible
- Private channels give members control over their audience
- Allow editing and deletion of posts to fix context collapse after the fact

## Information Asymmetry and Trust

Trust requires appropriate information sharing, not maximum transparency. Research on organizational trust (Mayer et al., 1995) identifies three factors:
1. **Ability**: Do they know what they're doing?
2. **Benevolence**: Do they care about my interests?
3. **Integrity**: Do they follow principles I find acceptable?

**For community platforms:**
- Admin actions should be somewhat transparent (builds integrity trust) but not exhaustively public
- User profiles should signal benevolence (bio, neighborhood connection) not just ability
- Moderation logs build institutional trust but individual privacy must be preserved

## The Neighborhood Map Problem

Putting member addresses on a map creates a powerful community tool with significant privacy risks:

**Benefits:**
- Visualizes community geography
- Helps members find nearby neighbors
- Makes the community feel tangible and local

**Risks:**
- Scrapers can harvest a complete list of names + addresses
- Domestic abuse situations where address must be hidden
- Burglary risk (public knowledge that a house is occupied by a community member)
- Data becomes stale and misleading when members move

**Mitigation strategies:**
- Display approximate location only (block level, not exact address)
- Require authentication + community membership to view
- No public API — server-rendered map only
- Allow members to opt out entirely or show neighborhood-only
- robots.txt + rate limiting + session-based rendering (no static image to scrape)
- Consider: is the benefit worth the risk? A member directory without a map may be sufficient.

## Visibility of Social Actions

Every feature choice about visibility shapes community behavior:

| Feature | Visible to all | Visible to involved | Private | Effect |
|---------|---------------|-------------------|---------|--------|
| Post | Default | - | - | Encourages participation |
| Block | Harmful | Less harmful | Best | See ostracism research |
| Mute | N/A | N/A | Inherently private | Low social cost |
| RSVP | Social pressure | Less pressure | Defeats purpose | Context-dependent |
| Profile view | Stalking risk | Moderate | Safest | Consider whether view counts are needed at all |
| Read receipts | High pressure | Moderate | No pressure | Probably don't add these |
| Online status | Surveillance feel | Moderate | Best for small communities | Avoid — creates obligation to respond |

**General principle:** In small communities, default to less visibility. Members can always choose to share more, but they can't un-share.
