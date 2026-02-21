# Rockart.sk — Architektúra projektu

## Prehľad projektu

**Rockart** je firma špecializujúca sa na profesionálne dláždenie dvorov, chodníkov a terás. Pracuje s betónovou dlažbou aj prírodným kameňom. Pôsobí v Komárňanskom regióne.

**Cieľová skupina:** Majitelia rodinných domov a firmy v Komárňanskom regióne, ktorí hľadajú kvalitné dláždenie a kamenárske práce. Dvojjazyčná komunita (slovenčina + maďarčina).

**Účel stránky:** Prezentačná webová stránka s cieľom získať nových zákazníkov, predstaviť služby a poskytnúť kontaktné informácie.

## Štruktúra stránky

| # | Sekcia | ID | Popis |
|---|--------|----|-------|
| 1 | Header | — | Logo, navigácia, jazykový prepínač SK/HU |
| 2 | Hero | `#hero` | Hlavný banner s nadpisom a CTA tlačidlom |
| 3 | O nás | `#about` | Predstavenie firmy, skúsenosti, hodnoty |
| 4 | Služby | `#services` | Zoznam poskytovaných služieb (dláždenie, kameň, príprava podkladu) |
| 5 | Galéria | `#gallery` | Ukážky realizovaných prác (placeholder obrázky) |
| 6 | Kontakt | `#contact` | Kontaktné údaje + kontaktný formulár |
| 7 | Footer | — | Copyright, kontakt, odkazy |

## Dizajnový systém

### Farby

| Úloha | Farba | Hex |
|-------|-------|-----|
| Primárna | Tmavá bridlica | `#2d3436` |
| Sekundárna | Teplá šedá (kameň) | `#636e72` |
| Akcent | Bronzová/zlatá | `#b8860b` |
| Akcent svetlá | Svetlá zlatá | `#d4a843` |
| Pozadie hlavné | Biela | `#ffffff` |
| Pozadie alternatívne | Svetlo šedá | `#f5f5f0` |
| Pozadie tmavé | Antracit | `#1a1a2e` |
| Text primárny | Tmavá | `#2d3436` |
| Text sekundárny | Stredná šedá | `#636e72` |
| Text na tmavom | Svetlá | `#e0e0e0` |
| Text biely | Biela | `#ffffff` |

### Fonty

- **Nadpisy:** Montserrat (Google Fonts), bold/semibold
- **Text:** Open Sans (Google Fonts), regular/light
- **Fallback:** system-ui, -apple-system, sans-serif

### Spacing

- Sekcia padding: 80px (desktop), 48px (mobile)
- Container max-width: 1200px
- Grid gap: 32px
- Komponenty border-radius: 8px

## Technické rozhodnutia

- **Pure HTML5 + CSS3 + Vanilla JS** — žiadne frameworky, žiadny Tailwind
- **Google Fonts** — Montserrat + Open Sans (jediná externá závislosť)
- **Mobile-first** responsive dizajn
- **Breakpointy:** 768px (tablet), 1024px (desktop)
- **Dvojjazyčnosť:** Samostatné HTML súbory (index.html = SK, index-hu.html = HU)
- **SEO:** Meta description, Open Graph tagy, sémantický HTML
- **Docker:** Nginx:alpine kontajner pre produkciu
- **Vanilla JS** len pre: hamburger menu toggle, smooth scroll, gallery lightbox

## Súborová štruktúra

```
rockart-web/
├── index.html          # Slovenská verzia stránky
├── index-hu.html       # Maďarská verzia stránky
├── style.css           # Kompletný styling (CSS custom properties)
├── nginx.conf          # Nginx server konfigurácia
├── Dockerfile          # Docker image pre deployment
├── ARCHITECTURE.md     # Tento súbor — dizajn a architektúra
├── CLAUDE.md           # Pravidlá pre AI asistenta
├── README.md           # Základný popis projektu
├── .gitignore          # Git ignore pravidlá
└── images/             # Priečinok pre obrázky (budúce)
    ├── hero-bg.jpg     # Pozadie hero sekcie
    ├── gallery-1.jpg   # Galéria — realizácia 1
    ├── gallery-2.jpg   # Galéria — realizácia 2
    ├── gallery-3.jpg   # Galéria — realizácia 3
    ├── gallery-4.jpg   # Galéria — realizácia 4
    ├── gallery-5.jpg   # Galéria — realizácia 5
    ├── gallery-6.jpg   # Galéria — realizácia 6
    └── favicon.ico     # Ikona stránky
```
