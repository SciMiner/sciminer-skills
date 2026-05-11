# Drug Naming Conventions by Region

## Naming Hierarchy (search in this order)

1. **INN** — International Nonproprietary Name (WHO-assigned; universal)
2. **rINN** — recommended INN (same thing, just confirms WHO adoption)
3. **USAN** — US Adopted Name (almost always = INN for modern drugs)
4. **JAN** — Japanese Accepted Name (may differ slightly)
5. **Brand name** — varies by market and licensee
6. **CAS number** — Chemical Abstracts Service; best for patent searches
7. **WHO ATC code** — anatomical/therapeutic/chemical hierarchy

---

## Chinese Drug Name Transliteration Rules

Foreign drugs approved in China receive an official Chinese transliteration
assigned by NMPA/CDE. These are used in all official CN documents.

**Key transliteration patterns:**
- Small molecule drugs: phonetic transliteration (音译) + type suffix
  - 替尼 (-tinib, kinase inhibitors), e.g., 伊马替尼 (imatinib)
  - 西布 (-cib, CDK inhibitors), e.g., 帕博西利 (palbociclib)
  - 珠单抗 (-zumab), 利单抗 (-limab), 单抗 (monoclonal antibody)
  - 替雷利珠单抗 (tislelizumab)

**Common antibody suffixes in Chinese:**
| Suffix class | CN convention | Example |
|---|---|---|
| -mab (monoclonal Ab) | 单抗 | nivolumab → 纳武利尤单抗 |
| -zumab (humanized) | 珠单抗 | bevacizumab → 贝伐珠单抗 |
| -umab (human) | 尤单抗 | adalimumab → 阿达木单抗 |
| -limab (PD-1 class) | 利单抗 | sintilimab → 信迪利单抗 |

**Search tip:** Use INN + "单抗" or INN + "替尼" in CNKI/Wanfang/CDE for
better recall. Also search the full Chinese INN in NMPA databases.

---

## Japanese Drug Name Rules (JAN)

Japanese names follow INN closely but use katakana (カタカナ) transcription:
- imatinib → イマチニブ
- trastuzumab → トラスツズマブ
- pembrolizumab → ペムブロリズマブ

**Search tip:** In J-PlatPat and jRCT, always search katakana form.
PMDA approval database accepts both INN and brand name in Japanese.

---

## Brand Name Variations by Market (Examples)

| INN | US Brand | EU Brand | JP Brand | CN Brand |
|-----|----------|----------|----------|----------|
| imatinib | Gleevec | Glivec | グリベック | 格列卫 |
| rituximab | Rituxan | MabThera | リツキサン | 美罗华 |
| pembrolizumab | Keytruda | Keytruda | キイトルーダ | 可瑞达 |
| nivolumab | Opdivo | Opdivo | オプジーボ | 欧狄沃 |
| osimertinib | Tagrisso | Tagrisso | タグリッソ | 泰瑞沙 |
| palbociclib | Ibrance | Ibrance | イブランス | 爱博新 |
| trastuzumab | Herceptin | Herceptin | ハーセプチン | 赫赛汀 |

> Brand names for biosimilars diverge significantly — always confirm
> the specific biosimilar product when researching CN/JP markets.

---

## China-Specific Drug Classification Numbers

NMPA approval numbers follow this format: 国药准字 + [category letter] + 8 digits

| Letter | Category |
|--------|----------|
| H | 化学药品 — Chemical drugs |
| Z | 中药 — Traditional Chinese medicine |
| B | 生物制品 — Biological products |
| S | 兽药 — Veterinary drugs |
| J | 进口药品 — Imported drugs (registered in CN) |

Example: 国药准字H20050001 = Chemical drug, approved ~2005

---

## ATC Code System (WHO)

Use ATC codes for systematic indication-based searching:

```
Level 1 (Anatomical main group):    L = Antineoplastic
Level 2 (Therapeutic subgroup):     L01 = Antineoplastics
Level 3 (Pharmacological subgroup): L01X = Other antineoplastics
Level 4 (Chemical subgroup):        L01XE = Protein kinase inhibitors
Level 5 (Chemical substance):       L01XE01 = Imatinib
```

ATC lookup: https://www.whocc.no/atc_ddd_index/

---

## CAS Number Resources

For chemical identity across patents and literature:
- PubChem: https://pubchem.ncbi.nlm.nih.gov (free, comprehensive)
- ChemSpider: https://www.chemspider.com (cross-reference)
- SciFinder: (subscription) most authoritative for patents

**When to use CAS:** Patent landscape searches, when INN not yet assigned
(investigational drugs), structure-activity relationship research.
