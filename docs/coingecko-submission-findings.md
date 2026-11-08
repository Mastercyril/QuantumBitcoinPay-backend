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
> - Website: https://13thchamberllc.com (Wix is a CoinGecko rejection reason — this site must move to Vercel before applying).
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
| Website URL | https://github.com/Mastercyril/QSAM-quantum-token |
| Submitter Role | Founder |
| Asset Type | Token (SPL on Solana) |
| Contract Address | 5nHg43TTkmCafvUPpjnvu57hWMRXUheN3CFdDuzdQM9x |
| Contract Decimal Places | 9 |

### Project Description (Third Person, 400+ chars)
QSAM (Quantum Secure Authentication Matrix) is a quantum-backed SPL token on the Solana blockchain developed by 13th Chamber LLC. It serves as the native utility token for a quantum computing ecosystem that includes drug discovery simulations, a Universal Codex Calculator, quantum stock prediction, and quantum-resistant cryptographic operations. QSAM operates on a proof-of-quantum-work model where each classical bit is replaced with a quantum bit (qbis) using the formula θᵢ = bitᵢ × π/2 + gravitational_factor × π/8. The token has a fixed supply of 350 million with 9 decimals and was launched via fair distribution on Pump.fun. QSAM integrates with IBM Quantum hardware (ibm_torino 133-qubit Heron r1) and achieves 348x error suppression using SCORE-ESCORT+ architecture.

---

## Step 2: Supply Information (Prepared)

### Token Supply
- Max Supply: 350,000,000 QSAM
- Total Supply: 350,000,000 QSAM
- Circulating Supply: ~340,000,000 QSAM (350M minus 10M founder lockup)

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
QSAM has a total supply of 350,000,000 tokens with 9 decimals. 97% was distributed via fair launch on Pump.fun with no lockup or vesting restrictions. The remaining 3% (10,000,000 QSAM) is allocated to the founder (Joseph Dougherty, 13th Chamber LLC) with a 12-month cliff followed by 48 months of linear vesting, with 0% released at TGE. No tokens were burned. Daily mining rewards of 10 QSAM per wallet are distributed from the fair launch allocation.

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
