# Rockart Web — CLAUDE.md

## Projekt
Statická dvojjazyčná webová stránka pre firmu Rockart (SK/HU).

## Technológia
- Čistý HTML + Tailwind CSS (CDN)
- Nginx:alpine Docker kontajner
- Žiadny JavaScript framework, žiadny build step

## Štruktúra
- index.html — slovenská verzia
- index-hu.html — maďarská verzia
- style.css — spoločné štýly
- nginx.conf — Nginx konfigurácia
- Dockerfile — Docker image definícia

## Pravidlá
- Všetky texty musia byť v oboch jazykoch (SK + HU)
- Tailwind len cez CDN (<script src="https://cdn.tailwindcss.com"></script>)
- Zachovaj rovnakú štruktúru v oboch HTML súboroch
- Kontaktné údaje musia byť identické v oboch verziách
- Git: commit messages v angličtine
