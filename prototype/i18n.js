(() => {
  const dictionaries = {
    en: {
      today:"Today", journey:"Research Journey", opportunities:"Opportunities", evidence:"Evidence Explorer", evolution:"Knowledge Evolution", review:"Human Review", coverage:"Research Coverage", profile:"Profile", profiles:"Profiles & Projects", project:"Project", admin:"Admin Copilot", research:"Research Copilot", language:"Language", dark:"Dark", light:"Light", viewAll:"View all", searchPlaceholder:"Search papers, concepts, gaps…",
      todayTitle:"Today", todaySubtitle:"What changed, why it matters, and where HUMAN attention is useful.", recentChanges:"Recent Important Changes", stageGuide:"Research Stage Guide", topOpportunities:"Top Research Opportunities", latestPapers:"Latest Papers", radar:"Telegram Research Radar", persistedPapers:"Persisted Papers", humanDecisions:"HUMAN Decisions", knowledgeChanges:"Knowledge Changes", coverageContext:"Coverage Context", radarItems:"Radar Items", inspectMembers:"Inspect members →", canonicalMembers:"Canonical members", selectMetric:"Select a metric to inspect its exact members.", close:"Close", persistedWorksDetail:"Persisted works in selected project", humanDecisionsDetail:"Explicit persisted HUMAN decisions", knowledgeChangesDetail:"Persisted canonical ChangeEvents", radarDetail:"Read-only projections from ChangeEvent", loadingCoverage:"Loading persisted coverage context…", workflowGuideOnly:"Workflow guide only · no canonical stage status persisted", showRemainingStages:"Show R7–R16 guide", stageStatusReversible:"Status is reversible", allStages:"All stages", illustrativeBoundary:"ILLUSTRATIVE / NON-CANONICAL: every stage status, count, identifier, evidence trace, and suggested action below is demonstration data. Do not use it as scientific state."
    },
    id: {
      today:"Hari Ini", journey:"Perjalanan Riset", opportunities:"Peluang Riset", evidence:"Penjelajah Bukti", evolution:"Evolusi Pengetahuan", review:"Tinjauan HUMAN", coverage:"Cakupan Riset", profile:"Profil", profiles:"Profil & Proyek", project:"Proyek", admin:"Admin Copilot", research:"Research Copilot", language:"Bahasa", dark:"Gelap", light:"Terang", viewAll:"Lihat semua", searchPlaceholder:"Cari paper, konsep, gap…",
      todayTitle:"Hari Ini", todaySubtitle:"Apa yang berubah, mengapa penting, dan di mana perhatian HUMAN diperlukan.", recentChanges:"Perubahan Penting Terkini", stageGuide:"Panduan Tahap Riset", topOpportunities:"Peluang Riset Utama", latestPapers:"Paper Terbaru", radar:"Radar Riset Telegram", persistedPapers:"Paper Tersimpan", humanDecisions:"Keputusan HUMAN", knowledgeChanges:"Perubahan Pengetahuan", coverageContext:"Konteks Cakupan", radarItems:"Item Radar", inspectMembers:"Periksa anggota →", canonicalMembers:"Anggota canonical", selectMetric:"Pilih metrik untuk melihat anggota persisnya.", close:"Tutup", persistedWorksDetail:"Karya tersimpan dalam proyek yang dipilih", humanDecisionsDetail:"Keputusan HUMAN eksplisit yang tersimpan", knowledgeChangesDetail:"ChangeEvent canonical yang tersimpan", radarDetail:"Proyeksi read-only dari ChangeEvent", loadingCoverage:"Memuat konteks cakupan yang tersimpan…", workflowGuideOnly:"Hanya panduan alur kerja · belum ada status tahap canonical yang tersimpan", showRemainingStages:"Tampilkan panduan R7–R16", stageStatusReversible:"Status dapat berubah kembali", allStages:"Semua tahap", illustrativeBoundary:"ILUSTRATIF / NON-CANONICAL: setiap status tahap, angka, identifier, jejak bukti, dan tindakan yang disarankan di bawah adalah data demonstrasi. Jangan gunakan sebagai status ilmiah."
    }
  };
  const normalize = value => value === "id" ? "id" : "en";
  const current = () => "id";
  const t = key => dictionaries[current()][key] || dictionaries.en[key] || key;

  const stageNames = {
    en:["Research Intent","Research Landscape","Evidence Mapping","Problem Formulation","Gap Formation","Gap Falsification","Theory Positioning","Research Question","Conceptualization","Method Intelligence","Research Design","Contribution Formation","Novelty Challenge","Evidence & Argument Audit","Adversarial Review","Scholarly Positioning","Research Readiness"],
    id:["Tujuan Riset","Lanskap Riset","Pemetaan Bukti","Perumusan Masalah","Pembentukan Gap","Falsifikasi Gap","Penempatan Teori","Pertanyaan Riset","Konseptualisasi","Inteligensi Metode","Desain Riset","Pembentukan Kontribusi","Uji Kebaruan","Audit Bukti & Argumen","Tinjauan Adversarial","Penempatan Keilmuan","Kesiapan Riset"]
  };
  const stageName = index => stageNames[current()][index] || stageNames.en[index] || `R${index}`;
  function apply(root=document) {
    document.documentElement.lang=current();
    root.querySelectorAll("[data-i18n]").forEach(el => { el.textContent=t(el.dataset.i18n); });
    root.querySelectorAll("[data-i18n-placeholder]").forEach(el => { el.placeholder=t(el.dataset.i18nPlaceholder); });
    root.querySelectorAll("[data-language-select]").forEach(el => { el.value=current(); });
  }
  function setLanguage(value) { localStorage.setItem("gfprojclaw-language",normalize(value)); apply(); window.dispatchEvent(new CustomEvent("gfprojclaw-language-change",{detail:{language:current()}})); }
  window.GF_I18N={t,apply,setLanguage,current,stageName};
})();
