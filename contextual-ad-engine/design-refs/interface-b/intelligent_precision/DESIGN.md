---
name: Intelligent Precision
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#3d4947'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#216963'
  on-secondary: '#ffffff'
  secondary-container: '#a8ece5'
  on-secondary-container: '#266d68'
  tertiary: '#545c72'
  on-tertiary: '#ffffff'
  tertiary-container: '#6c748b'
  on-tertiary-container: '#fefcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#abefe8'
  secondary-fixed-dim: '#8fd3cc'
  on-secondary-fixed: '#00201e'
  on-secondary-fixed-variant: '#00504b'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-stat:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1440px
  gutter: 24px
  margin-desktop: 32px
  margin-mobile: 16px
  stack-xs: 4px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style
The design system is built on the pillars of **Intelligent Precision** and **Calm Authority**. It targets enterprise-level marketing teams and data scientists who require a workspace that minimizes cognitive load while maximizing data clarity. 

The aesthetic follows a **Modern Corporate** approach—drawing inspiration from industry leaders like Linear and Vercel. It prioritizes high-quality typography, intentional whitespace, and a "function-first" hierarchy. The visual tone is professional and trustworthy, designed to instill confidence in AI-driven decision-making for high-stakes advertising campaigns.

## Colors
The palette is rooted in a "Clean Tech" philosophy. 
- **Primary (#0D9488):** A deep teal used for primary actions, success states, and key data visualizations. It conveys growth and intelligence.
- **Secondary (#115E59):** A darker shade of teal used for hover states and secondary emphasis to maintain monochromatic harmony.
- **Neutral Background (#FAFAFA):** A very light gray that reduces eye strain compared to pure white, providing a sophisticated canvas for data.
- **Border Neutral (#E5E5E5):** Used for hair-line borders to define structure without adding visual noise.
- **Text & UI Surface (#0F172A):** A deep slate used for high-contrast text and dark-mode elements (like sidebars) to ground the interface.

## Typography
**Inter** is the sole typeface, utilized for its exceptional legibility in data-dense environments. 

### Key Implementation Rules:
- **Confident Numbers:** For ROI, CTR, and budget figures, use the `display-stat` style with `tabular-nums` enabled. This ensures vertical alignment in tables and dashboard widgets.
- **Hierarchy:** Use weight (Medium/SemiBold) rather than size to create distinction in dense views.
- **Negative Tracking:** Apply subtle negative letter spacing (-0.01em to -0.02em) on headlines above 24px to give them a premium, "tight" editorial feel.

## Layout & Spacing
The design system utilizes a **12-column fluid grid** for the main content area, constrained to a maximum width of 1440px. 

### Spacing Philosophy:
- **8px Baseline:** All margins, paddings, and height increments must be multiples of 8px.
- **Data Density:** In analytical views, use `stack-sm` (8px) between related inputs and `stack-md` (16px) between grouped content.
- **Sectioning:** Use `stack-lg` (24px) for major vertical gaps between dashboard cards.
- **Sidebars:** Navigation sidebars should be fixed at 240px or 280px, while the main content area remains fluid.

## Elevation & Depth
Depth is created through **Tonal Layering** and soft, ambient shadows. We avoid heavy shadows to maintain the "Clean Tech" aesthetic.

- **Level 0 (Background):** #FAFAFA. The lowest surface.
- **Level 1 (Cards/Surfaces):** Pure #FFFFFF with a 1px border of #E5E5E5. This is the primary work surface.
- **Level 2 (Dropdowns/Modals):** Pure #FFFFFF with a more pronounced shadow: `0px 10px 15px -3px rgba(0, 0, 0, 0.05)`.
- **Interaction:** On hover, cards may lift slightly by transitioning to a border color of #D4D4D4 or by increasing shadow spread by 2px.

## Shapes
The shape language is modern and approachable without being overly playful. 
- **Standard Radius:** 12px (`rounded-lg`) is the default for cards, input fields, and primary buttons.
- **Small Radius:** 6px-8px for smaller components like tags, chips, or inner nested elements.
- **Pill:** Reserved exclusively for status indicators (e.g., "Active," "Pending") and toggle switches.

## Components
Consistent component styling ensures the dashboard feels like a singular, integrated tool.

- **Buttons:**
  - *Primary:* Solid Teal (#0D9488) with white text. 12px radius.
  - *Secondary:* White background with #E5E5E5 border and #0F172A text.
  - *Ghost:* No background, teal text, used for tertiary actions.
- **Cards:** White background, 1px border (#E5E5E5), 12px rounded corners. Padding should be a consistent 24px (`stack-lg`).
- **Input Fields:** 1px #E5E5E5 border, 12px radius. On focus, use a 2px teal (#0D9488) ring with a 20% opacity offset.
- **Chips/Badges:** Subtle background tints (e.g., 10% opacity of the status color) with 12px radius or pill-shape for statuses.
- **Lists:** Rows should have a minimum height of 48px, with hair-line dividers (#F5F5F5) and generous horizontal padding.
- **Icons:** Use 20px or 24px stroke-based icons (Lucide/Feather style). Ensure stroke weight is consistent (1.5px or 2px).