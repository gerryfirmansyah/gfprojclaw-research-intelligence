from pathlib import Path
s=Path('prototype/app.js').read_text()
for x in ['Kondisi saat ini — dalam bahasa manusia','Apa yang berubah?','Yang perlu HUMAN periksa:','Evidence yang tercatat sebagai pemicu perubahan','Detail teknis / canonical','gap ini masih kandidat yang perlu diperiksa lebih lanjut oleh HUMAN','bukan bukti bahwa research gap sudah terbukti','bukan keputusan penerimaan ilmiah','Tidak ada asesmen sebelumnya yang dapat dibandingkan secara canonical','change_event_evidence']:
    assert x in s,x
assert 'JSON.stringify(r.current_state_jsonb ?? null)' not in s
print('CHANGE_EVENT_HUMAN_EXPLANATION_PASS')
