# GitHub publish plan

**Public repo:** `ai-lab-free-university`  
**Account:** https://github.com/cipher0x9  
**When:** after `bash scripts/verify_slice.sh` is green and you can teach RTMA cold to a stranger.

## Pre-publish checklist

- [ ] No `.env`, keys, customer data, private chats  
- [ ] `university/v2-UNIVERSITY.html` opens offline &lt; 20 MB  
- [ ] `bash scripts/verify_slice.sh` exits 0  
- [ ] README download section obvious for non-git users  
- [ ] LICENSE · CONTRIBUTING · SECURITY · DOWNLOADS  
- [ ] `share-post/` ready  
- [ ] Linktree button only after Release zip exists  

## Suggested first release tag

`v2.0-free`

### Assets

1. **`v2-UNIVERSITY.html.zip`** — main free share (primary)  
2. `v1-SLICE.html.zip` — compact path  
3. Optional: source pack zip (md + labs)

## Ship sequence (match/exceed UC discipline)

1. Secret scrub: `rg -i 'api[_-]?key|sk-|BEGIN |password\\s*='`  
2. Init git **only inside AI-LAB-FREE-SHARE**  
3. Create public repo `ai-lab-free-university`  
4. Push main  
5. Create Release + attach zips  
6. Pin on profile next to UC free university  
7. Linktree button → release download  
8. LinkedIn post from `share-post/`  

## What NOT to publish

- Local model weights  
- UC private topologies / customer dial plans  
- Hermes private configs with tokens  
- Any file &gt; ~50 MB without optional/ + warning  

## Relationship to UC free pack

| Pack | Repo |
|------|------|
| UC Lab Free University | already public |
| AI Lab Free University | this project, separate repo |

**Siblings.** Cross-link. Never delete UC. AI pack should win on runnable labs + evals + rebuildable curriculum.
