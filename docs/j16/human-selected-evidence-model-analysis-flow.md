# GFPROJCLAW — HUMAN Selected Evidence → Model Analysis Flow

**Status:** PINNED acceptance direction  
**Date:** 2026-09-24  
**Principle:** GFPROJCLAW mengarahkan perhatian dan membantu analisis; HUMAN menentukan relevance, evidence set, gap/novelty, dan arah riset.

## 1. Posisi flow

Flow yang disepakati:

**Initial HUMAN Query → Research Universe → Landscape → progressive context (contoh: governance → smart → cities) → Candidate Papers → Screening Advice → HUMAN memilih screening lens → HUMAN memilih evidence set → Model Analysis → Compare & Contrast → Tension / Contradiction / Uncertainty → Investigation / Gap Opportunity Advice → HUMAN memilih arah → Research Copilot.**

Jangan melompat dari landscape langsung ke research gap atau Copilot.

## 2. Screening sebelum analysis

Contoh konteks kerja:

- Path: `governance → smart → cities`
- Candidate set: misalnya 36 paper
- Screening lens dipilih HUMAN, misalnya `Governance mechanism`, `Citizen / public outcome`, `Implementation`, `Policy & institution`, `Technology governance`, `Comparative/context`, atau `Contrasting evidence`.
- Sistem memberi WHY/signal untuk membantu screening, tetapi tidak menetapkan relevance.
- HUMAN memilih `INCLUDE / MAYBE / EXCLUDE` dan membentuk evidence set.

Tombol transisi eksplisit setelah selection:

**`Analisis N paper terpilih →`**

Jika belum ada paper dipilih, tombol analysis disabled.

## 3. Model Analysis pada paper terpilih

Model Analysis hanya bekerja pada evidence set yang telah dipilih HUMAN. Untuk setiap paper, ekstrak bila evidence mendukung:

| Dimensi | Isi yang dicari |
|---|---|
| Research focus | Apa yang sebenarnya diteliti |
| Context | Negara, kota, sektor, setting |
| Methodology | Quantitative, qualitative, case study, review, SEM, DID, dsb. |
| Data / sample | Sumber data, responden, jumlah kota, periode |
| Unit of analysis | Citizen, city, government, institution, project, dsb. |
| Governance construct | Bentuk governance yang diteliti |
| Mechanism | Bagaimana governance diduga/ditunjukkan bekerja |
| Outcome | Participation, trust, public value, QoL, sustainability, dsb. |
| Main finding | Temuan yang dilaporkan paper |
| Limitation | Keterbatasan yang dapat diverifikasi |
| Evidence level | Metadata / abstract / full text |

**Invariant:** jangan mengarang. Field yang tidak didukung evidence harus `BELUM TERVERIFIKASI`.

## 4. Evidence Comparison Table

Setelah extraction, tampilkan paper-to-paper analytical table. Tujuannya bukan bibliografi, tetapi membantu HUMAN melihat siapa meneliti apa, dengan metode apa, pada konteks apa, menemukan apa, dan melalui mekanisme apa.

Tabel harus readable sebagai wide research workspace dan tetap mempertahankan judul paper asli.

## 5. Compare & Contrast

Compare & Contrast adalah inti setelah extraction. Model membandingkan selected evidence set dan menyajikan secara terpisah:

### Common Patterns
Pola yang konsisten atau berulang pada beberapa paper.

### Differences
Perbedaan context, methodology, data/sample, unit analysis, governance construct, mechanism, outcome, dan findings.

### Contradictions / Tensions
Evidence yang tampak berbeda atau berlawanan. Sistem tidak boleh menganggap perbedaan keyword sebagai contradiction. Periksa apakah paper sebenarnya mengukur hal, unit, konteks, atau outcome yang berbeda.

### Uncertainties
Hal yang belum dapat dijawab oleh selected evidence set atau belum dapat diverifikasi dari evidence level yang tersedia.

## 6. Cross-dimensional Analysis

Model kemudian membantu HUMAN memeriksa hubungan lintas dimensi, minimal:

- **Methodology × Finding** — apakah metode berbeda terkait pola temuan berbeda?
- **Context × Finding** — apakah pola berubah menurut negara/kota/institusi?
- **Unit Analysis × Outcome** — apakah city/government-level outcome sejalan dengan citizen-level outcome?
- **Mechanism × Outcome** — mechanism apa dikaitkan dengan outcome apa?
- **Evidence × Contradiction** — contradiction substantif atau hanya perbedaan desain/context?

Semua hasil tetap berupa observation/advice yang traceable, bukan scientific verdict otomatis.

## 7. Investigation / Gap Opportunity Advice

Gap Opportunity hanya muncul **setelah** HUMAN memilih evidence set dan Model Analysis/Compare & Contrast dilakukan.

Setiap opportunity minimal berisi:

- **Observation** — apa yang terlihat pada selected evidence.
- **WHY** — mengapa pola/tension tersebut layak diperiksa.
- **Supporting evidence** — paper yang mendukung observation.
- **Contrasting evidence** — paper yang mungkin menantang atau memberi konteks berbeda.
- **Uncertainty** — apa yang masih belum diketahui.
- **Verification needed** — evidence apa yang perlu diperiksa berikutnya.
- **Evidence level** — metadata / abstract / full text.
- **Status** — `CANDIDATE INVESTIGATION OPPORTUNITY`, bukan validated research gap.

Boleh ada beberapa opportunity. **Tidak ada ranking/best choice. HUMAN memilih.**

## 8. Research Copilot handoff

Research Copilot baru menerima konteks setelah HUMAN memilih arah investigasi. Handoff harus membawa jejak reasoning, misalnya:

- Research path: `governance → smart → cities`
- HUMAN screening lens
- Candidate corpus count
- HUMAN-selected paper IDs/count
- Evidence extraction/matrix
- Common patterns
- Differences
- Contradictions/tensions
- Uncertainties
- Cross-dimensional observations
- HUMAN-selected investigation opportunity
- Evidence limitations/provenance

Copilot tidak memulai dari prompt kosong dan tidak menerima sekadar kata `cities`.

## 9. HUMAN authority

GFPROJCLAW boleh:

- memetakan candidate evidence;
- memberi Screening Advice;
- menjelaskan WHY;
- mengekstrak evidence yang tersedia;
- melakukan descriptive Compare & Contrast;
- menunjukkan tension, contradiction candidate, uncertainty;
- menawarkan beberapa investigation opportunities;
- membantu menyusun pertanyaan verifikasi berikutnya.

HUMAN tetap memutuskan:

- paper mana relevan;
- evidence set final;
- apakah observation substantif;
- apakah sesuatu merupakan research gap;
- novelty/significance;
- opportunity mana yang dilanjutkan;
- research question dan arah penelitian.

## 10. Acceptance target berikutnya

Implementasi/review berikutnya harus berfokus pada experience ini, bukan hardening engine:

**HUMAN selesai screening → tombol `Analisis N paper terpilih →` → evidence extraction dari paper pilihan → Evidence Comparison Table → Compare & Contrast → Cross-dimensional Analysis → Investigation Opportunities → HUMAN memilih → Research Copilot.**

Prioritas UI terdekat: perbesar/readable-kan teks penjelasan Screening Advice dan buat selected lens/paper state jelas sebelum masuk Analysis.
