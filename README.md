# product-plugins

Official Tessl plugins published to the [`tessl` workspace](https://tessl.io/registry/tessl/) on the Tessl registry.

These are R&D-maintained plugins intended for production use.

## Plugins

| Plugin | Description | Badge |
| --- | --- | --- |
| [`skill-optimizer`](skill-optimizer/) | Optimize your skills and plugins: review SKILL.md quality, generate eval scenarios, run evals, compare across models, diagnose gaps, and re-run until scores improve | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftesslio%2Fproduct-plugins%2Fmain%2Fskill-optimizer%2F.tessl-plugin%2Fplugin.json&query=%24.version&label=tessl&color=blue&prefix=v)](https://tessl.io/registry/tessl/skill-optimizer) [![](https://img.shields.io/endpoint?url=https%3A%2F%2Fapi.tessl.io%2Fv1%2Fbadges%2Ftessl%2Fskill-optimizer)](https://tessl.io/registry/tessl/skill-optimizer/evals) |
| [`review-plugin-creator`](review-plugin-creator/) | Create a custom `tessl review` rubric – fork the default rubric, build one from scratch, or derive it from evidence (existing skills, PR feedback, agent logs) | [![review-plugin-creator version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftesslio%2Fproduct-plugins%2Fmain%2Freview-plugin-creator%2F.tessl-plugin%2Fplugin.json&query=%24.version&label=tessl&color=blue&prefix=v)](https://tessl.io/registry/tessl/review-plugin-creator) [![review-plugin-creator evals](https://img.shields.io/endpoint?url=https%3A%2F%2Fapi.tessl.io%2Fv1%2Fbadges%2Ftessl%2Freview-plugin-creator)](https://tessl.io/registry/tessl/review-plugin-creator/evals) |
| [`default-skill-review`](default-skill-review/) | The default `tessl review` rubric – an agentic reviewer that scores a skill's description and content, the same reviewer `tessl review` uses out of the box. Score skills against it, or fork it into a custom rubric | [![default-skill-review version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftesslio%2Fproduct-plugins%2Fmain%2Fdefault-skill-review%2F.tessl-plugin%2Fplugin.json&query=%24.version&label=tessl&color=blue&prefix=v)](https://tessl.io/registry/tessl/default-skill-review) [![default-skill-review evals](https://img.shields.io/endpoint?url=https%3A%2F%2Fapi.tessl.io%2Fv1%2Fbadges%2Ftessl%2Fdefault-skill-review)](https://tessl.io/registry/tessl/default-skill-review/evals) |
| [`api`](api/) | Find and call Tessl API endpoints token-efficiently, without loading the whole `openapi.json` spec into context | [![api version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftesslio%2Fproduct-plugins%2Fmain%2Fapi%2F.tessl-plugin%2Fplugin.json&query=%24.version&label=tessl&color=blue&prefix=v)](https://tessl.io/registry/tessl/api) [![api evals](https://img.shields.io/endpoint?url=https%3A%2F%2Fapi.tessl.io%2Fv1%2Fbadges%2Ftessl%2Fapi)](https://tessl.io/registry/tessl/api/evals) |

## Install

```bash
tessl install tessl/skill-optimizer
```
