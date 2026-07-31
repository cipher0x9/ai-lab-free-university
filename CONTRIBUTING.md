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
