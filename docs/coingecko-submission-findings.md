# CoinGecko Listing Submission Findings — August 26, 2026

> **⚠️ UPDATE (Nov 8, 2026): DO NOT SUBMIT WITH THE 5nHg MINT.**
> The fields below list contract `5nHg...M9x` (350M, 9 decimals) — that mint has **no liquidity pool and no trading**.
> CoinGecko auto-rejects any token that is not actively trading on a tracked exchange.
>
> **Submit with the TRADING mint instead:**
> - Contract address: `48YZxAUXFcEG14kEWHyBBaEx1gabprkXxQsz2ViuPZPN`
> - Decimals: 6 | Total supply: 1,000,000,000 | Standard: Solana Token-2022
> - Market: pump.fun AMM, QSAM/SOL pair — https://dexscreener.com/solana/DmmDdbYs3SzWhopJ4D7kt3mpo6HV9u8B8vuk97YBcVQn
> - Explorer: https://solscan.io/token/48YZxAUXFcEG14kEWHyBBaEx1gabprkXxQsz2ViuPZPN
> - Already indexed on DexScreener and GeckoTerminal (CoinGecko's own DEX tracker).
> - Website: https://13thchamberllc.com/qryptocurrency/
> - Portal (replaces the retired quantumbitcoinpay.com host): https://qsam.13thchamberllc.com
> - Supply/price facts to pull live at submission time: https://api.dexscreener.com/latest/dex/tokens/48YZxAUXFcEG14kEWHyBBaEx1gabprkXxQsz2ViuPZPN
>
> Naming correction: QSAM = "Quantum System Access Module" (per whitepaper v2.0). The description below says
> "Quantum Secure Authentication Matrix" — fix that before submitting; inconsistent naming causes rejections.
> Also: the description says "launched via fair distribution on Pump.fun" for the 5nHg mint — that is the 48YZ mint's story.

## Status: In Progress (Manual Completion Required)

### Form URL
https://partner.coingecko.com/request-form/coins/new

---

## Step 1: Basic Coin/Token Information ✅

| Field | Value |
|---|---|
| Listing Type | Active Listing |
| Coin/Token Name | QSAM Quantum Token |
| Coin/Token Symbol | QSAM |
| Website URL | https://13thchamberllc.com/qryptocurrency/ |
| Submitter Role | Founder |
| Asset Type | Token (Token-2022 on Solana) |
| Contract Address | 48YZxAUXFcEG14kEWHyBBaEx1gabprkXxQsz2ViuPZPN |
| Contract Decimal Places | 6 |

### Project Description (Third Person, 400+ chars)
QSAM (Quantum System Access Module) is the canonical Solana Token-2022 utility token of 13th Chamber LLC. Fixed supply is 1,000,000,000 with 6 decimals. Mint authority and freeze authority are revoked. The token launched on pump.fun. Contract: 48YZxAUXFcEG14kEWHyBBaEx1gabprkXxQsz2ViuPZPN. Post-quantum cryptography for the wallet is on the roadmap and is not implemented. Do not submit legacy mint 5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x.

---

## Step 2: Supply Information (Prepared)

### Token Supply (canonical mint — submit these figures)
- Max Supply: 1,000,000,000 QSAM
- Total Supply: 1,000,000,000 QSAM
- Decimals: 6
- Mint authority: revoked
- Freeze authority: revoked
- Circulating supply: read it live at submission time. Do not submit a hard-coded number.

The allocation tables below describe the non-canonical legacy mint (350,000,000 supply, 9 decimals, `5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x`). Do not submit them for the canonical token.

### Allocation 1 — Fair Launch / Public
| Field | Value |
|---|---|
| Percentage | 97% |
| TGE Percentage | 100% |
| Cliff Period | 0 months |
| Vesting Period | 0 months |
| Release Schedule | Linear |

### Allocation 2 — Founder Allocation
| Field | Value |
|---|---|
| Percentage | 3% (10,000,000 QSAM) |
| TGE Percentage | 0% |
| Cliff Period | 12 months |
| Vesting Period | 48 months |
| Release Schedule | Linear |
| Wallet | Treasury wallet (10M QSAM locked) |
| Owned By | Joseph Dougherty (13th Chamber LLC) |

### Additional Supply Information
Canonical QSAM has a fixed supply of 1,000,000,000 tokens with 6 decimals on Token-2022. Mint and freeze authority are revoked. It launched on pump.fun. The 350,000,000 / 9-decimal allocation notes in this section apply only to the legacy mint and must not be copied into the CoinGecko form.

---

## Step 3: Additional Information (Fields to Fill)

1. **What is the project about?** — Third-person description (400+ chars, prepared above)
2. **What can your coin/token be used for?** — Utility description (400+ chars)
3. **What's next for your project?** — Roadmap description (400+ chars)
4. **Whitepaper URL** — https://github.com/Mastercyril/QuantumBitcoinPay-backend
5. **Twitter/X** — (to be provided by founder)
6. **Telegram** — (to be provided by founder)

---

## Next Steps Checklist

- [ ] Log into CoinGecko partner portal
- [ ] Fill Step 1 (Basic Info) — data prepared above
- [ ] Fill Step 2 (Supply Info) — both allocations prepared above
- [ ] Fill Step 3 (Additional Info) — description, utility, roadmap fields
- [ ] Submit form and save confirmation reference

---

## Browser Automation Log

Attempted to fill the CoinGecko form via Browserbase browser automation on Aug 26, 2026.

### Issues Encountered
- React form inputs did not register programmatic typing after browser context reset
- Browser iteration limit (tool call cap) hit twice during the session
- Cookie consent banner needed to be dismissed each session
- All form data has been preserved in Notion for manual submission

### Recommendation
Complete the form manually using the data above, or retry browser automation with a fresh session using click-then-type pattern for React inputs.

### Note
CoinGecko requires the token to be listed on at least one exchange before approval. Consider listing on Raydium or another DEX first to meet this requirement.
