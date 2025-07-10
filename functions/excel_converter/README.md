# Lovable Excel Converter

**Edge Function** voor Supabase om grote Excel-bestanden te verwerken:
- Houdt alleen de gewenste kolommen.
- Geeft foutmelding bij ontbrekende kolommen.
- Hernoemt `Email (FullEnrich)` naar `Email`.
- Maakt extra sheet `JEX2` met `Company` & `Domain`.
- Uploadt resultaat naar Supabase Storage en geeft publieke download-URL.
