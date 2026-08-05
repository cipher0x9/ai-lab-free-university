# Contributing

Thank you for helping learners worldwide.

1. Keep changes **additive** and educational.  
2. **No** production secrets, API keys, customer data, or private chats.  
3. Prefer small, reviewable PRs (one topic per PR).  
4. Curriculum sections: edit `curriculum/corpus.py`, then run:

```bash
python3 scripts/build_university.py
bash scripts/verify_slice.sh
```

5. Labs must run without cloud keys by default (mock/local ok).  
6. Default free HTML must stay browser-friendly (target ≤ 20 MB).  
7. Be kind. Free for learning.

Questions: open an issue on the public repo when published (`ai-lab-free-university`).

## Engineering contribution gate

Keep every contribution additive and evidence-bearing:

1. Preserve existing lesson IDs, paths, and public wording unless fixing a proven defect.
2. Add the vendor-neutral mechanism before provider-specific instructions.
3. Include a failure fixture, falsifier, RTMA fields, and rollback note.
4. For prompt/model/index changes, compare the same golden set before and after.
5. Keep the public surface English-only and every runtime dependency offline-safe.
6. Run `bash scripts/verify_slice.sh`; include the exact GREEN/RED evidence in review.

Useful additions include small zero-key labs, synthetic eval fixtures, retrieval
ablations, approval-boundary tests, and diagrams that make a real data path clearer.
Do not add secrets, customer data, copied private chats, model weights, generated
run artifacts, or autonomous external actions.
