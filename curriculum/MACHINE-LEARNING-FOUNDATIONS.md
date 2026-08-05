# Machine Learning Foundations
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** ML-201 · **Level:** Foundation → Intermediate  
> **Outcome:** Own the math+practice loop from linear models through deep nets, with eval discipline that transfers to LLMs.

---

## 0. The Learning Problem

Given dataset \(\mathcal{D}=\{(x_i,y_i)\}_{i=1}^n\), learn function \(f_\theta\) that generalizes to unseen \(x\).

```text
Data → Features/Reps → Model → Loss → Optimizer → Eval → Deploy → Monitor
```

| Problem type | Target \(y\) | Examples |
|--------------|--------------|----------|
| Regression | continuous | price, latency |
| Binary class | {0,1} | spam |
| Multiclass | {1..K} | intent |
| Multilabel | bit vector | tags |
| Ranking | order | search |
| Generative | density / sample | LM, diffusion |
| RL | reward via actions | agents, games |

---

## 1. Linear Regression

### 1.1 Model

\[
\hat{y} = w^\top x + b
\]

### 1.2 Squared loss (MSE)

\[
\mathcal{L} = \frac{1}{n}\sum_i (y_i - \hat{y}_i)^2
\]

Closed form (when \(X^\top X\) invertible):

\[
\hat{w} = (X^\top X)^{-1} X^\top y
\]

Prefer **gradient methods** for large/high-dim.

### 1.3 Assumptions & failures

- Linearity in parameters (features can be nonlinear)  
- Outliers dominate MSE → try Huber  
- Multicollinearity → unstable weights → regularization  

```python
import numpy as np

def fit_ridge(X, y, l2=1.0):
    # X: [n,d], with bias column optional
    d = X.shape[1]
    A = X.T @ X + l2 * np.eye(d)
    return np.linalg.solve(A, X.T @ y)
```

---

## 2. Classification

### 2.1 Logistic regression

\[
p(y=1|x)=\sigma(w^\top x+b),\quad \sigma(z)=\frac{1}{1+e^{-z}}
\]

Loss: binary cross-entropy (BCE).

### 2.2 Multiclass softmax

\[
p(y=k|x)=\frac{e^{z_k}}{\sum_j e^{z_j}}
\]

### 2.3 Decision thresholds

Default 0.5 is rarely optimal. Choose threshold on validation for precision/recall tradeoff.

| Metric | Formula intuition | Use |
|--------|-------------------|-----|
| Accuracy | correct / n | balanced |
| Precision | TP/(TP+FP) | costly FP |
| Recall | TP/(TP+FN) | costly FN |
| F1 | harmonic mean | balance |
| AUROC | rank quality | threshold-free |
| AUPRC | precision-recall curve | rare positives |
| Log loss | probabilistic | calibration |

---

## 3. Gradient Descent Family

### 3.1 Vanilla GD

\[
\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}
\]

### 3.2 SGD / Mini-batch

Noise helps escape sharp minima; mini-batch is the practical default.

### 3.3 Momentum / Adam

- **Momentum:** velocity smooths gradients  
- **Adam:** adaptive per-param rates (common default)  
- **AdamW:** decoupled weight decay (preferred for transformers)

### 3.4 Learning rate schedules

| Schedule | Shape |
|----------|-------|
| Constant | flat |
| Step decay | drop at epochs |
| Cosine | smooth anneal |
| Warmup + cosine | transformers |
| One-cycle | fast practical |

**LR find heuristic:** loss explosion → LR too high; flat forever → too low / dead features.

### 3.5 Gradient clipping

Hard clip or global norm clip stabilizes RNNs/transformers.

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

---

## 4. Regularization & Generalization

| Method | Mechanism |
|--------|-----------|
| L2 / weight decay | shrink weights |
| L1 | sparsity |
| Early stopping | stop at val best |
| Dropout | noise on units |
| Data aug | expand support |
| Label smoothing | softer targets |
| Ensemble | reduce variance |
| Batch/Layer norm | stabilize train |

### 4.1 Bias–variance intuition

- High bias: underfit (train error high)  
- High variance: overfit (train≪val error)  

### 4.2 Overfitting checklist

- [ ] More data / better data  
- [ ] Simpler model / more reg  
- [ ] Early stop on val  
- [ ] Leakage audit (see §9)  
- [ ] Stronger augmentation  

---

## 5. Model Progression: Classical → Deep → Transformers

### 5.1 Classical toolbox

| Model | Strength |
|-------|----------|
| Linear / logistic | strong baseline |
| Trees / RF / GBM | tabular kings |
| SVM | margins, kernels |
| kNN | simple nonparametric |
| Naive Bayes | text baseline |
| GMM / clustering | unsupervised |

**Always ship a strong classical baseline** on tabular before deep.

### 5.2 Neural nets (MLP)

```text
x → Linear → Act → … → Linear → loss
```

Activations: ReLU, GELU, SiLU. Depth + residual helps optimization.

### 5.3 CNNs (vision)

Inductive bias: local connectivity + weight sharing.

```text
Conv → BN → ReLU → Pool → … → GAP → FC
```

Key ideas: receptive field, stride, dilation, residual blocks (ResNet).

### 5.4 RNNs / LSTM / GRU (sequence)

Hidden state carries past; LSTM gates fix vanishing somewhat. Parallelism poor → largely replaced by transformers for language.

### 5.5 Transformers

Self-attention = content-based routing over sequence; scales with data/compute. See `LLM-ARCHITECTURE-DEEP.md`.

```text
era: bag-of-words → word2vec → RNN/LSTM → Transformer → LLM/VLM
```

---

## 6. Loss Functions Map

| Task | Loss |
|------|------|
| Regression | MSE, MAE, Huber |
| Binary | BCE |
| Multiclass | CE |
| Imbalanced | focal, class weights |
| Metric learning | contrastive, triplet, InfoNCE |
| Ranking | pairwise / listwise |
| Generative LM | CE next-token |
| Diffusion | noise prediction MSE |
| Preference | DPO / reward CE |

**Match loss to metric approximately** — optimizing MSE ≠ optimizing MAPE.

---

## 7. Feature Engineering

### 7.1 Tabular

- Missingness indicators  
- Log transforms for heavy tails  
- Interactions / polynomials (careful)  
- Target encoding with CV (leakage-safe)  
- Datetime cycles (sin/cos hour)  
- Categorical: one-hot, hashing, embeddings  

### 7.2 Text (pre-LLM)

- Token counts / TF-IDF  
- n-grams  
- Character features for noisy text  

### 7.3 Scaling

StandardScaler / robust scalers for linear models & nets; trees often OK without.

---

## 8. Cross-Validation & Data Splits

### 8.1 Rules

```text
Train — fit params
Val   — select model / hparams / early stop
Test  — touch ONCE for final report
```

### 8.2 CV types

| Type | When |
|------|------|
| K-fold | i.i.d. small data |
| Stratified | class imbalance |
| GroupKFold | same user/doc leakage |
| TimeSeriesSplit | temporal |
| Nested CV | honest model selection |

### 8.3 Leakage hall of shame

1. Scale on full data then split  
2. Target encoding without folds  
3. Random split on time series  
4. Duplicate near-identical rows across splits  
5. Feature computed with future info  
6. LLM eval set in pretrain (decontamination)  

---

## 9. Model Evaluation Practice

### 9.1 Protocol

1. Freeze metric + splits **before** experiments  
2. Log every run (params, seed, metrics)  
3. Multiple seeds for variance  
4. Significance: bootstrap CIs when possible  
5. Error analysis by slice (length, class, locale)  

### 9.2 Calibration

Reliability diagrams; temperature scaling for probabilities.

### 9.3 Slice metrics

Overall accuracy can hide failure on minority languages, rare intents, long inputs.

```python
def slice_recall(y_true, y_pred, mask):
    yt, yp = y_true[mask], y_pred[mask]
    return (yt & yp).sum() / max(yt.sum(), 1)
```

---

## 10. Optimization Numerics

| Issue | Symptom | Fix |
|-------|---------|-----|
| Exploding grad | NaN | clip, lower LR |
| Vanishing | no learning | residuals, norm |
| Dead ReLU | zero grads | Leaky/GELU |
| Class collapse | predicts majority | weights, resample |
| Batch size | gen gap | tune LR scaling |

**Effective batch:** LR warmups often needed when scaling batch size.

---

## 11. Unsupervised & Self-supervised (bridge to modern AI)

| Method | Idea |
|--------|------|
| PCA / SVD | linear compress |
| Clustering | structure discovery |
| Autoencoders | reconstruct |
| Contrastive (SimCLR, CLIP) | pull positives |
| Masked LM | BERT-style |
| Causal LM | GPT-style |

Self-supervision turns unlabeled data into pretext tasks → representations for transfer.

---

## 12. From Classical ML to LLM Systems

| Classical skill | LLM analogue |
|-----------------|--------------|
| Features | prompts, tools, chunks |
| Regularization | prefer SFT quality, KL/DPO |
| CV | golden sets + holdouts |
| Calibration | confidence, refusal |
| Feature stores | memory / RAG indexes |
| A/B tests | prompt/model canaries |
| Drift | embedding + output drift |

**Do not skip foundations** — debugging LLM systems reuses these instincts.

---

## 13. Worked Mini-Lab: Intent Classifier

```python
# Pseudocode pipeline
# 1) load labeled intents
# 2) split stratified 70/15/15
# 3) baseline: TF-IDF + LogisticRegression
# 4) neural: mini embedding + MLP
# 5) report macro-F1 + confusion + slices
# 6) threshold per-class if needed
```

**Acceptance:** macro-F1 ≥ baseline + 2% with CI overlap noted; error analysis written.

---

## 14. RTMA Labs

### Lab M1 — Regression baseline

- **Run:** linear vs ridge on synthetic + real CSV  
- **Trace:** coeffs, condition number  
- **Metric:** RMSE train/val  
- **Artifact:** `m1_regression.json`

### Lab M2 — Classification metrics

- **Run:** imbalanced dataset; plot PR curve; pick threshold  
- **Metric:** F1 at best threshold vs 0.5  
- **Artifact:** `m2_thresholds.csv`

### Lab M3 — Overfit demo

- **Run:** deep MLP on small n without reg vs with dropout+early stop  
- **Metric:** gap train-val  
- **Artifact:** `m3_curves.md`

### Lab M4 — Leakage hunt

- **Run:** time series with random vs temporal split  
- **Metric:** inflated accuracy delta  
- **Artifact:** `m4_leakage.md`

### Lab M5 — Tree vs linear tabular

- **Run:** GBM vs logistic on same features  
- **Metric:** logloss + inference latency  
- **Artifact:** `m5_tabular.csv`

---

## 15. Interview-Ready Formula Sheet

- MSE, BCE, Softmax+CE  
- Precision/Recall/F1  
- Gradient step \(\theta-\eta g\)  
- L2 objective \(\mathcal{L}+\lambda\|w\|^2\)  
- Bias-variance qualitative  
- Train/val/test discipline  
- ROC vs PR when to use  

---

## 16. Master Checklist

- [ ] Problem type named  
- [ ] Baseline shipped  
- [ ] Split strategy justified  
- [ ] Metric matches product cost  
- [ ] Leakage reviewed  
- [ ] Error slices analyzed  
- [ ] Seeds logged  
- [ ] Model complexity justified  
- [ ] Deployment metric monitored  

---

## 17. CYPHER0X9 Proof Seal

```text
PACK: MACHINE-LEARNING-FOUNDATIONS
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF: RTMA labs M1–M5
BRIDGE: classical ML → LLM/RAG/agents
```

**Teach-back:** Derive logistic loss intuition; explain why time split ≠ random; pick metric for rare fraud; sketch CNN vs transformer inductive biases.

---

*End of pack · UC AI Free University · Foundations before fireworks.*
