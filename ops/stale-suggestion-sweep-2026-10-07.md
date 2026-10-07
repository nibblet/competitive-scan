# Stale suggestion sweep, 2026-10-07

Paul approved clearing suggestions older than 30 days. 41 tasks in `readvise.readvise_tasks` were archived (`archived_at = now()`), the same soft delete the app uses for dismiss. Nothing was deleted.

**Undo** (Supabase SQL):

```sql
update readvise.readvise_tasks set archived_at = null, updated_at = now() where id in ('8b9ee867-41d5-48c8-a270-ae7e80a522c5','8395fc52-ec6d-4a8c-af3d-293e634117ad','72e736a6-f976-4277-8dbe-996249bdda63','221579ed-87c4-4a3f-a67a-24828f957764','57946552-8afd-444a-bc45-7dc0f68c945d','2b413ce4-38e0-4e20-96a8-2533be42d735','6a9c36ab-2469-4ba8-ba6d-380b5dc1b0f8','85c0fd23-d116-485d-8f54-7326848ee130','40729180-bbfd-4792-b90c-f449c72475a5','403ba263-5471-470d-8b6f-b72f5603897e','f05f5029-f993-49e7-b522-9f4419daed3b','cd02fa14-fa72-48ce-a613-32d0d2fff5cf','8d3210cf-e8be-4e83-bd4c-4218efcc7724','7e654d9b-1880-408d-bb71-5ec1ab409627','4a255d21-fb18-4958-8233-3d6b9daa9b57','d8d40bc9-644e-47c5-9266-6be0148380c0','9598908c-6fa3-4f89-b3e0-6cf7ee6e61f2','7eca0543-be84-4edf-a4a0-b202424defd8','12ee4e29-d9b6-4c69-857a-32cc01eee1b9','0d61a0fd-ac04-4407-b489-90f01c78004e','3230d922-8943-41ae-b3d9-9d57088443af','e0d58c38-e72c-4340-9b0e-5d4b97c97879','3e80a0d5-1b4c-49b7-99bc-1690bea2759f','823a12fe-5639-46e6-865a-2d8b86f551e6','89846f7d-dab9-4d6d-9264-54665710ab89','2649beff-12ae-433d-97b1-802e26a7bc7e','099a9e0a-b90b-491c-a122-7b8ccc2943dc','e768a2ac-ae5c-48c1-892d-812d3d6a8007','c55a95c9-ff7e-447d-b448-c35bd4e9e74d','c18a6d79-cd4b-4043-a35a-ddfc602847f5','e5431efd-41c5-4980-88f1-4c328ff8d2bd','ba09d9be-25c7-42cb-a04a-bff336830939','01aedbc3-2e20-4bae-aee7-bdaa9f8208b3','c3317c16-7b8b-46f3-85f2-33f7f0c82b5b','78873639-5e88-4639-a98b-0bffc57be0b0','b09be22a-ccf0-4623-bdb1-e52374ea5d6c','529f788b-7b67-4990-9600-7eb4f6735d3f','b4c9fa22-ce09-47a6-ab5a-310c94e9418c','9195da7a-5eec-4f44-a09f-40c75b473696','96c41e16-3938-40a1-b59c-9af6b506753c','25e3a4d4-0a16-458e-8813-ce72903b389d');
```

| Age (days) | Source | Label |
|---|---|---|
| 355 | advisor | Calculate financial implications of wholesaling vs. rehabbing. |
| 355 | advisor | Address operational issues leading to missed callbacks and no-shows. |
| 353 | advisor | Adjust lead management strategies as needed based on feedback and market conditions |
| 353 | advisor | Gather detailed information on each lead for initial assessment |
| 353 | advisor | Document every interaction in a CRM tool |
| 350 | advisor | Discuss refinancing options for new rentals with the bank. |
| 350 | advisor | Plan a strategic review session for portfolio growth and risk management. |
| 350 | advisor | Confirm rental demand and calculate cash flow for new rentals. |
| 349 | advisor | Engage the seller further to gauge their motivation and potential for commitment |
| 349 | advisor | Re-evaluate the property's priority post-seller engagement |
| 346 | advisor | Adjust the business website for brand guideline compliance. |
| 345 | advisor | Gather relevant documents for the compliance review meeting. |
| 345 | advisor | Schedule training sessions on document management and compliance |
| 344 | advisor | Collect detailed seller motivation and urgency information. |
| 272 | advisor | Monitor lead generation flow closely |
| 99 | ai | Offboard coordinator cleanly tomorrow via HR agent |
| 99 | ai | 1860 E Deb Dr: line up contractors this week (closes tomorrow, 2-week tenant runway) |
| 99 | ai | 258 Fortney: ping seller tomorrow and confirm the real close date (Jul 12 is a Sunday) |
| 99 | ai | 1860 Baxter + 113 Stevenson both listed on MLS by this weekend (realtor working disclosures/paperwork) |
| 99 | ai | Submit PFS to the bank by Friday — unlocks the Longfellow refi and the Garland/Penway debt retirement |
| 99 | ai | 1805 Blanca critical path: electrician + handyman on site tomorrow, work Tues AM and Thurs AM blocks, contractors finish paint to 100% by Friday, flooring scheduled for next week, plumbing contracted  |
| 35 | manual | Check title on 206 ALGER AVE LOUISVILLE KY 40214 |
| 35 | manual | Check title on 600 LA FONTENAY CT LOUISVILLE KY 40223 |
| 35 | manual | Check title on 1125 E SAINT CATHERINE ST LOUISVILLE KY 40204 |
| 35 | manual | Check title on 545 RAWLINGS ST LOUISVILLE KY 40217 |
| 35 | manual | Check title on 10918 OAK HARBOR DR LOUISVILLE KY 40299 |
| 35 | manual | Check title on 837 DRESDEN AVE LOUISVILLE KY 40215 |
| 35 | manual | Check title on 102 CLOVER DR LOUISVILLE KY 40175 |
| 35 | manual | Check title on 343 ROGERSVILLE RD RADCLIFF KY 40160 |
| 35 | manual | Check title on 169 FOREST DR JEFFERSONVILLE IN 47130 |
| 35 | manual | Check title on 1033 SPRINGDALE DR JEFFERSONVILLE IN 47130 |
| 35 | manual | Check title on 3512 BANNER DR JEFFERSONVILLE IN 47130 |
| 35 | manual | Check title on 410 HAMLET DR NEW ALBANY IN 47150 |
| 35 | manual | Check title on 527 S 3RD ST LOUISVILLE KY 40202 |
| 35 | manual | Check title on 1709 VALLEY FORGE WAY LOUISVILLE KY 40215 |
| 35 | manual | Check title on 1027 BLUEGRASS AVE LOUISVILLE KY 40215 |
| 35 | manual | Check title on 7910 WINDGATE DR LOUISVILLE KY 40291 |
| 35 | manual | Check title on 4213 FINAL DR LOUISVILLE KY 40219 |
| 35 | manual | Check title on 340 S 43RD ST LOUISVILLE KY 40212 |
| 35 | manual | Check title on 7417 RAINBOW DR LOUISVILLE KY 40272 |
| 35 | manual | Check title on 1932 W MADISON ST LOUISVILLE KY 40203 |
