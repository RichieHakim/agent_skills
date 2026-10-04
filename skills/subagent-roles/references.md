# Models

Choose within a provider family. The rows below are directional dispatch tiers, not cross-provider equivalences. Prices are standard API rates checked 2026-10-04; recheck before cost-sensitive dispatches.

## Anthropic

| Tier | Model | Price / 1M tokens | Use | Example tasks |
|---|---|---|---|---|
| Frontier | `fable` | $10 in / $50 out | Hardest problems | Long-horizon work, subtle bugs, final review |
| Heavy | `opus` | $4 in / $20 out | High trust | Refactors, architecture, ambiguous bugs |
| Standard | `sonnet` | $2 in / $10 out | Strong default | Features, tests, codebase research |
| Light | `haiku` | $1 in / $5 out | Cheap, fast | Mechanical edits, grep reports |

## OpenAI

| Tier | Model | Price / 1M tokens | Use | Example tasks |
|---|---|---|---|---|
| Frontier | `gpt-6-astra` | $10 in / $50 out | Hardest problems | Long-horizon work, subtle bugs, final review |
| Standard | `gpt-6.1-sol` | $2 in / $10 out | Strong default, near-Astra | Refactors, features, tests, codebase research |
| Light | `gpt-6-luna` | $0.10 in / $0.50 out | Cheap, fast | Mechanical edits, grep reports |
