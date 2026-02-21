# Rockart Web — CLAUDE.md

## Projekt
Statická dvojjazyčná webová stránka pre firmu Rockart — profesionálne dláždenie dvorov, chodníkov a terás (SK/HU).

## Technológia
- Čistý HTML5 + CSS3 + Vanilla JS
- Google Fonts (Montserrat + Open Sans) — jediná externá závislosť
- Nginx:alpine Docker kontajner
- Žiadny JavaScript framework, žiadny Tailwind, žiadny build step

## Štruktúra
- index.html — slovenská verzia
- index-hu.html — maďarská verzia
- style.css — kompletný styling s CSS custom properties
- ARCHITECTURE.md — dizajnový systém a architektúra
- nginx.conf — Nginx konfigurácia
- Dockerfile — Docker image definícia
- images/ — priečinok pre obrázky (hero-bg, galéria, favicon)

## Pravidlá
- Všetky texty musia byť v oboch jazykoch (SK + HU)
- Zachovaj rovnakú štruktúru v oboch HTML súboroch
- Kontaktné údaje musia byť identické v oboch verziách
- Farby definované cez CSS custom properties v :root
- Mobile-first responsive dizajn
- Git: commit messages v angličtine
