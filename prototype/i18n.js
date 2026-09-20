(() => {
  const dictionaries = {
    en: {
      today:"Today", journey:"Research Journey", opportunities:"Opportunities", evidence:"Evidence Explorer", evolution:"Knowledge Evolution", review:"Human Review", coverage:"Research Coverage", profile:"Profile", profiles:"Profiles & Projects", project:"Project", admin:"Admin Copilot", research:"Research Copilot", language:"Language", dark:"Dark", light:"Light", viewAll:"View all",
      todayTitle:"Today", todaySubtitle:"What changed, why it matters, and where HUMAN attention is useful.", recentChanges:"Recent Important Changes", stageGuide:"Research Stage Guide", topOpportunities:"Top Research Opportunities", latestPapers:"Latest Papers", radar:"Telegram Research Radar", persistedPapers:"Persisted Papers", humanDecisions:"HUMAN Decisions", knowledgeChanges:"Knowledge Changes", coverageContext:"Coverage Context", radarItems:"Radar Items", inspectMembers:"Inspect members →", canonicalMembers:"Canonical members", selectMetric:"Select a metric to inspect its exact members.", close:"Close"
    },
    id: {
      today:"Hari Ini", journey:"Perjalanan Riset", opportunities:"Peluang Riset", evidence:"Penjelajah Bukti", evolution:"Evolusi Pengetahuan", review:"Tinjauan HUMAN", coverage:"Cakupan Riset", profile:"Profil", profiles:"Profil & Proyek", project:"Proyek", admin:"Admin Copilot", research:"Research Copilot", language:"Bahasa", dark:"Gelap", light:"Terang", viewAll:"Lihat semua",
      todayTitle:"Hari Ini", todaySubtitle:"Apa yang berubah, mengapa penting, dan di mana perhatian HUMAN diperlukan.", recentChanges:"Perubahan Penting Terkini", stageGuide:"Panduan Tahap Riset", topOpportunities:"Peluang Riset Utama", latestPapers:"Paper Terbaru", radar:"Radar Riset Telegram", persistedPapers:"Paper Tersimpan", humanDecisions:"Keputusan HUMAN", knowledgeChanges:"Perubahan Pengetahuan", coverageContext:"Konteks Cakupan", radarItems:"Item Radar", inspectMembers:"Periksa anggota →", canonicalMembers:"Anggota canonical", selectMetric:"Pilih metrik untuk melihat anggota persisnya.", close:"Tutup"
    }
  };
  const normalize = value => value === "id" ? "id" : "en";
  const current = () => normalize(localStorage.getItem("gfprojclaw-language") || "en");
  const t = key => dictionaries[current()][key] || dictionaries.en[key] || key;
  function apply(root=document) {
    document.documentElement.lang=current();
    root.querySelectorAll("[data-i18n]").forEach(el => { el.textContent=t(el.dataset.i18n); });
    root.querySelectorAll("[data-i18n-placeholder]").forEach(el => { el.placeholder=t(el.dataset.i18nPlaceholder); });
    root.querySelectorAll("[data-language-select]").forEach(el => { el.value=current(); });
  }
  function setLanguage(value) { localStorage.setItem("gfprojclaw-language",normalize(value)); apply(); window.dispatchEvent(new CustomEvent("gfprojclaw-language-change",{detail:{language:current()}})); }
  window.GF_I18N={t,apply,setLanguage,current};
})();
