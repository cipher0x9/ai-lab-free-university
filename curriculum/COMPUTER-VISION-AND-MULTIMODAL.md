# Computer Vision and Multimodal AI
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** CV-MM-401 · **Level:** Intermediate→Advanced  
> **Outcome:** Master CNNs → ViTs → CLIP-style embeddings → diffusion → video → multimodal fusion → production CV systems.

---

## 0. Vision Problem Map

| Task | Output | Metrics |
|------|--------|---------|
| Classification | class label | top-1/5, F1 |
| Detection | boxes + labels | mAP |
| Segmentation | masks | IoU / mIoU |
| Pose | keypoints | PCK |
| OCR | text | CER/WER |
| VQA | answer | accuracy / VQA score |
| Retrieval | ranked images | R@k |
| Generation | image/video | FID, CLIPScore, human |
| Depth / 3D | maps / meshes | AbsRel, etc. |

```text
pixels → backbone → task head(s) → postprocess → product action
```

---

## 1. CNN Foundations

### 1.1 Convolution

Local receptive fields + weight sharing → translation-friendly features.

| Hyperparam | Effect |
|------------|--------|
| Kernel size | context vs cost |
| Stride | downsample |
| Padding | preserve size |
| Dilation | larger field w/o params |
| Groups / depthwise | efficiency (MobileNet) |

### 1.2 Classic stacks

```text
LeNet → AlexNet → VGG → Inception → ResNet → EfficientNet → ConvNeXt
```

**ResNet insight:** residual connections enable deep optimization.

```python
def residual_block(x, conv_path):
    return relu(x + conv_path(x))
```

### 1.3 Modern practical backbone choice

| Need | Direction |
|------|-----------|
| Edge mobile | MobileNet/ConvNeXt-T, quantized |
| Accuracy server | ViT/ConvNeXt large, ensembles |
| Detection | multi-scale FPN-style necks |
| Few data | strong aug + transfer |

---

## 2. Vision Transformers (ViT)

### 2.1 Patchify

```text
Image H×W×3 → patches P×P → flatten → linear embed + pos → Transformer encoder
```

### 2.2 Inductive bias tradeoff

| CNN | ViT |
|-----|-----|
| Strong locality bias | Weaker; needs data/reg |
| Efficient small data | Shines large scale |
| Translation friendly | Global attention early |

### 2.3 Hybrids & efficient variants

- Hierarchical ViTs (window attention)  
- Conv stem + transformer  
- MobileViT-style for edge  

### 2.4 Training recipe notes

- Strong augmentation (RandAugment, Mixup, CutMix)  
- AdamW + cosine  
- Higher resolution fine-tune after pretrain  
- MAE / self-supervised pretrain for labels-scarce  

---

## 3. CLIP-Style Multimodal Embeddings

### 3.1 Contrastive idea

Train image encoder \(f\) and text encoder \(g\) so matched pairs have high cosine similarity:

\[
\mathcal{L} = \mathrm{InfoNCE}(f(i), g(t))
\]

### 3.2 Capabilities unlocked

- Zero-shot classification via text prompts  
- Image-text retrieval  
- Semantic search over image corpora  
- Rerank / filter for gen models  

```python
# Zero-shot classification sketch
image_emb = normalize(image_encoder(img))
text_embs = normalize(text_encoder(class_prompts))
scores = image_emb @ text_embs.T
pred = scores.argmax()
```

### 3.3 Prompt engineering for CLIP

```text
"a photo of a {class}"
"a satellite image of {class}"
"a close-up medical photo of {class}"  # domain prompts matter
```

Ensemble multiple prompt templates for gains.

### 3.4 Limitations

- Fine-grained attributes (counts, exact text in image) weak  
- Spurious correlations from web data  
- Not a replacement for specialized detectors when precision-critical  

---

## 4. Image Generation — Diffusion

### 4.1 Intuition

Forward: add noise until isotropic Gaussian.  
Reverse: neural net predicts noise (or velocity) to denoise step-by-step.

```text
x0 → x1 → … → xT ~ N(0,I)
xT → … → x0_hat  (generate)
```

### 4.2 Latent diffusion

Encode image to latent with VAE; diffuse in latent space → huge compute win (Stable Diffusion family).

```text
Image → VAE enc → latent → denoise conditioned on text → VAE dec → Image
```

### 4.3 Conditioning

| Conditioner | Use |
|-------------|-----|
| Text (CLIP/T5) | prompts |
| Class labels | controllable cats |
| Depth / canny / pose | ControlNet-style |
| Image embeds | img2img, IP-Adapter |
| Masks | inpainting |

### 4.4 Sampling

- DDPM (many steps)  
- DDIM / Euler / DPM-Solver (fewer steps)  
- Guidance scale: adherence vs diversity/artifacts  
- Seed for reproducibility  

### 4.5 Eval for gen

| Metric | Notes |
|--------|-------|
| FID | distribution distance; imperfect |
| CLIPScore | text alignment proxy |
| Human prefs | gold for product |
| Safety filters | NSFW, IP policy |
| Task success | e.g. usable product shot |

---

## 5. Video Models

### 5.1 Challenges

- Temporal consistency  
- Compute ∝ frames  
- Motion + audio sync (multimodal)  
- Long-horizon narrative  

### 5.2 Approaches

| Approach | Idea |
|----------|------|
| 2D CNN + late fusion | cheap baseline |
| 3D CNN / (2+1)D | spatiotemporal filters |
| Tubelet ViT | patch over space-time |
| Diffusion video | denoise frame sequences / latent tubes |
| Autoregressive tokens | discrete visual tokens |

### 5.3 Practical product path

1. Keyframe understanding with image VLM  
2. Short clip captioning  
3. Specialized action recognition  
4. Gen video only if product needs it (costly)

---

## 6. Multimodal Fusion & VLMs

### 6.1 Fusion strategies

| Strategy | Description |
|----------|-------------|
| Early | joint tokenizer from start |
| Late | combine decisions |
| Cross-attention | text attends image tokens |
| Dual encoder | CLIP-like separate |
| Projector + LLM | map vision tokens into LLM space |

### 6.2 LLaVA-style recipe (conceptual)

```text
Vision encoder (frozen or partial) → MLP/projector → LLM embedding space
Train: image-text instruct data (caption, VQA, OCR-heavy)
```

### 6.3 Token budget reality

High-res images → many visual tokens → cost. Use:

- Adaptive resolution  
- Token merging / pooling  
- Crop + zoom agent tools for detail  

---

## 7. OCR & Document Intelligence

### 7.1 Pipeline

```text
detect text regions → recognize → order/readpath → layout (tables) → LLM extract
```

### 7.2 Metrics

- CER / WER  
- Field accuracy (key-value)  
- End-to-end form F1  

### 7.3 Hard cases

- Handwriting, skew, stamps, multi-column  
- Low light mobile photos  
- Multilingual mixed scripts  

**Production tip:** hybrid — OCR engine for text + VLM for ambiguous layout; verify critical fields with rules.

---

## 8. VQA & Visual Reasoning

### 8.1 Failure modes

- Language prior bias (answer without looking)  
- Hallucinated objects  
- Counting / spatial errors  
- Reading small text  

### 8.2 Mitigations

- Balanced datasets  
- Require pointing / crops  
- Tool use: zoom, OCR tool  
- Faithfulness evals with region evidence  

---

## 9. Production CV Systems

### 9.1 Architecture

```text
Capture → quality gate (blur/exposure)
  → model(s) ensemble
  → business rules
  → human review if low conf
  → action + audit image store
```

### 9.2 Latency budgets

| App | Typical |
|-----|---------|
| Mobile lens | on-device ms–tens ms |
| Web upload | 100ms–2s |
| Batch video | throughput oriented |

### 9.3 MLOps for CV

- Dataset versioning (images + labels + license)  
- Train/serve preprocess parity (color, resize, norm)  
- Slice metrics: lighting, device, geo  
- Drift: camera sensor changes  
- Active learning for hard examples  

### 9.4 Safety & privacy

- Faces/PII blurring policies  
- Biometric legal constraints  
- Deepfake / abuse detection if UGC  
- EXIF stripping  

---

## 10. Data Engine for Vision

```text
collect → dedup → label (auto+human) → QA → train → error mine → collect more
```

| Label type | Cost |
|------------|------|
| Class tags | low |
| Boxes | med |
| Polygons | high |
| Video tracks | very high |

Use weak supervision and synthetic data carefully; always real-world holdout.

---

## 11. Multimodal RAG

```text
Index: image embeds + OCR text + captions
Query: text or image
Retrieve: hybrid
Generate: VLM with citations to asset ids
```

Eval: retrieval R@k + answer faithfulness to image evidence.

---

## 12. RTMA Labs

### Lab C1 — CNN vs ViT transfer

- **Run:** fine-tune both on small dataset  
- **Trace:** train curves  
- **Metric:** val top-1 + latency  
- **Artifact:** `c1_backbone.csv`

### Lab C2 — Zero-shot CLIP

- **Run:** classify with prompt templates ensemble  
- **Metric:** accuracy vs linear probe  
- **Artifact:** `c2_clip.md`

### Lab C3 — Diffusion param sweep

- **Run:** vary steps & guidance on fixed prompts  
- **Metric:** CLIPScore + human notes  
- **Artifact:** `c3_diffusion.json`

### Lab C4 — OCR field extract

- **Run:** OCR + regex/LLM on forms  
- **Metric:** field F1  
- **Artifact:** `c4_ocr_report.md`

### Lab C5 — Preprocess parity

- **Run:** intentionally break mean/std; measure drop  
- **Metric:** Δ accuracy  
- **Artifact:** `c5_skew.md`

---

## 13. Interview Sketch: Photo Moderation System

1. Problem: NSFW + spam + illegal  
2. Models: multi-label classifier + ensemble + hash matching  
3. Human review queue for gray zone  
4. Latency SLO + abuse adversarial  
5. Eval: precision at high recall; fairness slices  
6. Privacy: retention, access control  
7. Feedback: appeal process  

---

## 14. Production Checklist

- [ ] Task metrics match business cost  
- [ ] Train/serve preprocess identical  
- [ ] Dataset licenses documented  
- [ ] Slice evaluation (device/light/locale)  
- [ ] Confidence + human fallback  
- [ ] Drift monitors  
- [ ] Safety/privacy review  
- [ ] Cost per image/video  
- [ ] RTMA on model promote  

---

## 15. CYPHER0X9 Proof Seal

```text
PACK: COMPUTER-VISION-AND-MULTIMODAL
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF: RTMA labs C1–C5
```

**Teach-back:** Explain residual learning; ViT patchify; CLIP contrastive loss; latent diffusion; train/serve vision skew.

---

*End of pack · UC AI Free University · Pixels are data — treat them like production data.*
