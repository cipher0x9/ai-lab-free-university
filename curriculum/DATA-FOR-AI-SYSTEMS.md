# Data for AI Systems

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT**

---

## 1) Data is the real model

Garbage in → confident garbage out. Treat datasets like production configs.

---

## 2) Dataset classes

| Class | Use |
|-------|-----|
| Golden eval | Regression forever |
| Train / SFT | Behavior shaping |
| Preference | DPO/RLAIF style |
| RAG corpus | Retrieval truth |
| Red team | Safety |

Never mix without labels.

---

## 3) Lineage fields (minimum)

`source`, `license`, `pii_class`, `time_collected`, `transform_version`, `owner`.

---

## 4) PII & secrets

- Default local for sensitive  
- Synthetic fixtures for public repos  
- Scrub before cloud  

This free university ships **synthetic** fixtures only.

---

## 5) Versioning

Pin dataset hashes in eval reports. If data moves under you, scores are lies.

---

## 6) Drill

Build a 25-row golden set for your domain. Run it twice. Diff.

**Educational only · MIT**
