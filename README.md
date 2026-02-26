<div align="center">

# 🇫🇷 Exahia — Infrastructure IA Souveraine B2B

**Sovereignty as a Service**

*Modèles open-source déployés sur hardware français. Zero retention. RGPD natif. Cloud Act free.*

[Site Web](https://exahia.com) · [Contact](mailto:admin@exahia.ia)

---

🇫🇷 Made in France · 🔒 RGPD Natif · 🛡️ Zero Data Retention · ☁️ Cloud Act Free · 🏗️ OVHcloud Bare-Metal

</div>

---

## Open-Source Tooling

These repositories are the most actionable entry points for the community:

| Repo | Purpose | Quick start |
|------|---------|-------------|
| [pii-detector-fr](https://github.com/Exahia/pii-detector-fr) | Detect/anonymize French PII before LLM calls | `python -m pip install -e . && pii-detector scan --text "..."` |
| [llm-benchmark-fr](https://github.com/Exahia/llm-benchmark-fr) | Reproducible benchmark runner for French business prompts | `python3 scripts/run_benchmark.py --dataset ... --model ... --mock reference` |
| [shadow-ai-audit](https://github.com/Exahia/shadow-ai-audit) | Checklists + scoring CLI for Shadow AI risk | `python3 tools/score_audit.py --responses ...` |

### Community priorities

- Improve detection precision and false-positive handling (`pii-detector-fr`)
- Contribute domain datasets and evaluators (`llm-benchmark-fr`)
- Extend scoring with NIS2 / DORA / ISO27001 controls (`shadow-ai-audit`)

---

## Le Problème : Shadow AI en Entreprise

Le **Shadow AI** désigne l'utilisation non contrôlée d'outils d'intelligence artificielle par les employés, sans validation de la DSI ni conformité vérifiée.

### L'ampleur du phénomène

Les chiffres sont alarmants :

- **49% des employés** utilisent des outils IA non sanctionnés par leur employeur
- **87% des cabinets juridiques** ont des collaborateurs utilisant des IA non autorisées
- **58%** de ces utilisateurs se servent de versions gratuites, sans aucune sécurité entreprise
- **3 RSSI sur 4** ont découvert de l'IA générative non autorisée dans leur environnement
- **225 000+ identifiants ChatGPT** en vente sur le dark web (malware LummaC2)

### L'impact financier

- Coût moyen d'une brèche de données avec Shadow AI élevé : **4,63M€**
- En moyenne, **223 violations de politique de données par mois** impliquant l'IA générative
- L'IA générative est le **canal n°1 d'exfiltration de données** d'entreprise vers le personnel (32% des mouvements non autorisés)

### Le dilemme des secteurs réglementés

Pour le juridique, la santé, la finance et la défense, c'est un choix impossible :
- **Utiliser ChatGPT** = productivité mais violation du secret professionnel et du RGPD
- **Interdire l'IA** = conformité mais perte de compétitivité

Exahia résout ce dilemme.

---

## La Solution : Infrastructure IA Souveraine

Exahia fournit une **infrastructure managée** qui déploie des modèles IA open-source sur du hardware souverain en France.

### Principes fondamentaux

1. **Souveraineté totale** — Hardware bare-metal OVHcloud, datacenter en France, aucune juridiction US
2. **Zero Retention** — Données traitées en RAM uniquement, jamais persistées sur disque
3. **Modèles Open-Source** — Mistral, Llama 3, Qwen 2.5, DeepSeek — auditables, sans boîte noire
4. **API Compatible OpenAI** — Migration transparente depuis les outils existants
5. **Détection PII automatique** — Presidio + spaCy filtrent les données personnelles en <2ms

### Pourquoi pas les modèles propriétaires ?

Pour **90% des tâches entreprise** (résumé, rédaction, Q&A, extraction, classification), les modèles open-source comme Qwen 2.5 32B et Mistral offrent des performances comparables à GPT-4 — sans aucun risque de conformité.

> *"Nous fournissons la plomberie et l'électricité (infrastructure), pas seulement l'eau (tokens)."*

---

## Comparaison vs Alternatives

| Critère | Exahia | OpenAI / ChatGPT | Azure OpenAI | Mistral (Le Chat) | Scaleway AI | Lakera |
|---------|--------|-------------------|--------------|-------------------|-------------|--------|
| **Hébergement France** | ✅ OVHcloud bare-metal | ❌ USA | ❌ USA/Irlande | ⚠️ Partiel | ✅ France | ❌ Suisse |
| **Cloud Act Free** | ✅ | ❌ Soumis | ❌ Soumis | ⚠️ | ✅ | ❌ |
| **Zero Retention** | ✅ RAM only | ❌ Logs conservés | ❌ | ⚠️ Politique variable | ❌ | N/A |
| **Modèles Open-Source** | ✅ Tous | ❌ Propriétaires | ❌ | ✅ Mistral uniquement | ✅ Multi-modèles | N/A |
| **Interface ChatGPT-like** | ✅ Open WebUI | ✅ | ✅ | ✅ | ❌ API only | ❌ |
| **RAG intégré** | ✅ Documents internes | ⚠️ Limité | ⚠️ | ❌ | ❌ | ❌ |
| **Détection PII** | ✅ Automatique (<2ms) | ❌ | ❌ | ❌ | ❌ | ✅ (spécialisé) |
| **Instance dédiée** | ✅ Offre BUNKER | ❌ Multi-tenant | ⚠️ Limité | ❌ | ✅ | N/A |
| **Éligible BPI France** | ✅ IA Booster | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## Offres

### ACCESS — GPU Mutualisé
- **Cible** : Freelances, petites équipes, POC
- **GPU** : Nvidia L40S (partagé, haute performance)
- **Prix** : ~29€/utilisateur/mois
- **Déploiement** : Immédiat
- **Idéal pour** : Tester l'IA souveraine, premiers pas

### BUNKER — Instance Dédiée
- **Cible** : PME, ETI, secteurs réglementés
- **GPU** : Nvidia L4, L40S ou H100 (dédié)
- **Fonctionnalités** : RAG intégré, isolation complète, workspace collaboratif
- **Setup** : 3 500€ (installation + configuration)
- **Idéal pour** : Données sensibles, conformité stricte

### ENTERPRISE — Sur Mesure
- **Cible** : CAC40, grands comptes, secteur public
- **Options** : On-premise, cloud privé, cluster multi-GPU
- **Éligibilité** : Subventions BPI France "IA Booster"
- **Accompagnement** : Onboarding personnalisé, SLA custom
- **Idéal pour** : Déploiements à grande échelle, exigences spécifiques

### Économies vs Cloud US

| Scénario | Cloud US (ChatGPT Enterprise) | Exahia Souverain | Économie |
|----------|-------------------------------|------------------|----------|
| 5 utilisateurs / an | 3 100 - 3 650€ | 1 000 - 1 200€ | **60-70%** |
| 50 utilisateurs / an | 61 000 - 68 000€ | 26 000 - 30 000€ | **55-60%** |
| 500+ utilisateurs / an | 260 000 - 620 000€ | 80 000 - 150 000€ | **60-75%** |

*Incluant les coûts cachés : DPO, DPIA, audit RGPD, risque de brèche.*

---

## Stack Technique

```
Exahia Infrastructure
├── 🖥️ Hardware
│   ├── OVHcloud Bare-Metal (France)
│   ├── Nvidia L4 / L40S / H100
│   └── RAM ECC, NVMe, réseau 10Gbps
├── 🤖 Modèles
│   ├── Qwen 2.5 32B (Flash — tâches rapides)
│   ├── Apriel Nemotron 49B (Thinker — raisonnement)
│   ├── Mistral Large (général)
│   ├── Llama 3 70B (général)
│   └── DeepSeek (spécialisé)
├── 🔒 Sécurité
│   ├── Presidio (détection PII)
│   ├── spaCy / FastFilter (NLP français)
│   ├── Zero Retention (RAM only)
│   └── Chiffrement TLS end-to-end
├── ⚙️ Infrastructure
│   ├── Serveurs GPU OVHcloud (API compatible OpenAI)
│   ├── Benchmark continu → sélection des meilleurs modèles
│   ├── Docker Compose (orchestration)
│   ├── Traefik (reverse proxy + SSL auto)
│   └── PostgreSQL / SQLite (métadonnées)
└── 🖼️ Interface
    ├── Open WebUI (ChatGPT-like)
    ├── RAG (documents internes)
    └── Workspace collaboratif
```

---

## Secteurs Cibles

### 🏛️ Juridique
Secret professionnel absolu. Analyse de contrats, recherche jurisprudence, rédaction d'actes. Aucun token ne quitte le territoire français.

### 🏥 Santé
Données patients protégées (Art. 9 RGPD). Comptes-rendus médicaux, aide au diagnostic, synthèse de dossiers. Zero retention = zéro risque de fuite.

### 💰 Finance
Conformité AMF, ACPR, BCE. Compatible MiFID II et DORA. Analyse documentaire automatisée sans exfiltration de données.

### 🛡️ Défense & Industrie
Brevets, données R&D, informations classifiées. Aucune juridiction étrangère. Fine-tuning sans que le modèle "apprenne" vos données.

### 🏫 Secteur Public
Administrations, collectivités, établissements d'enseignement. RGPD stricte, marchés publics. Éligible subventions BPI France.

---

## Contexte Réglementaire 2026

### EU AI Act — Application complète le 2 août 2026
- Pénalités jusqu'à **35M€ ou 7% du CA mondial**
- Obligations pour les systèmes IA à haut risque (emploi, crédit, éducation, justice)
- Les entreprises doivent prouver la maîtrise de leurs outils IA

### RGPD — Amendes en hausse
- **2,3 milliards d'euros** d'amendes RGPD en 2025 (+38% vs 2024)
- **443 notifications de brèche par jour** en Europe
- **5,65 milliards d'euros** cumulés depuis 2018

### Cloud Act — Le risque permanent
- Permet au gouvernement US d'accéder aux données des entreprises américaines, même stockées en Europe
- Conflit direct avec l'article 48 du RGPD
- Aucune entreprise européenne utilisant un cloud US n'est pleinement conforme au RGPD

---

## FAQ

### Exahia est-il une alternative à ChatGPT pour les entreprises ?
Oui. Exahia fournit une interface similaire à ChatGPT (via Open WebUI) avec des modèles open-source performants, mais hébergée en France avec zero retention. C'est l'alternative souveraine pour les entreprises qui ne peuvent pas utiliser les services cloud américains.

### Quels modèles IA sont disponibles ?
Mistral, Llama 3, Qwen 2.5, DeepSeek, et Apriel Nemotron. Les modèles sont sélectionnés pour leur performance sur les tâches entreprise en français. Nouveaux modèles ajoutés régulièrement.

### Les données sont-elles stockées ?
Non. Zero retention signifie que les données sont traitées en RAM uniquement et ne sont jamais écrites sur disque. Aucun entraînement n'est effectué sur vos données.

### Exahia est-il conforme au RGPD ?
Oui. Infrastructure hébergée en France (OVHcloud), zero retention, détection automatique de PII, pas de transfert de données hors UE. Conforme aux articles 28, 32, 44-49 du RGPD.

### Comment migrer depuis ChatGPT Enterprise ?
L'API Exahia est compatible OpenAI. La migration se fait en changeant l'URL de l'API. L'interface Open WebUI offre une expérience utilisateur similaire à ChatGPT.

### Quel est le coût par rapport à ChatGPT Enterprise ?
Exahia coûte 55 à 75% moins cher que ChatGPT Enterprise, en incluant les coûts cachés de conformité RGPD (DPO, DPIA, audit, risque de brèche).

---

## Repos Open-Source

| Repo | Description |
|------|-------------|
| [pii-detector-fr](https://github.com/Exahia/pii-detector-fr) | Détection et anonymisation de données personnelles françaises (Presidio + spaCy) |
| [llm-benchmark-fr](https://github.com/Exahia/llm-benchmark-fr) | Benchmarks LLM sur tâches métier françaises (juridique, finance, santé) |
| [shadow-ai-audit](https://github.com/Exahia/shadow-ai-audit) | Audit et détection du Shadow AI en entreprise — checklist RGPD + Cloud Act |

---

## Contact

- 🌐 **Site Web** : [exahia.com](https://exahia.com)
- 📧 **Email** : admin@exahia.ia
- 🐙 **GitHub** : [github.com/Exahia](https://github.com/Exahia)

---

*Exahia — L'IA d'entreprise, sans compromis sur la souveraineté.*
