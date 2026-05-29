---
name: Friendly Social Native
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daef'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e9edff'
  surface-container-high: '#e1e8fd'
  surface-container-highest: '#dce2f7'
  on-surface: '#141b2b'
  on-surface-variant: '#3d4947'
  inverse-surface: '#293040'
  inverse-on-surface: '#edf0ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#585f6c'
  on-secondary: '#ffffff'
  secondary-container: '#dce2f3'
  on-secondary-container: '#5e6572'
  tertiary: '#924628'
  on-tertiary: '#ffffff'
  tertiary-container: '#b05e3d'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#dce2f3'
  secondary-fixed-dim: '#c0c7d6'
  on-secondary-fixed: '#151c27'
  on-secondary-fixed-variant: '#404754'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#370e00'
  on-tertiary-fixed-variant: '#773215'
  background: '#f9f9ff'
  on-background: '#141b2b'
  surface-variant: '#dce2f7'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
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
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 16px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
  max-width-desktop: 640px
---

## Brand & Style

This design system centers on a friendly, native mobile experience that prioritizes content clarity and helpful interactions. The aesthetic blends **Minimalism** with **Modern Corporate** sensibilities, utilizing generous whitespace and soft edges to reduce cognitive load in high-density social feeds.

The target audience seeks a reliable, "calm" social environment. The UI evokes a sense of openness and accessibility through its breathable layout and approachable rounded forms. Visual cues are straightforward and functional, avoiding unnecessary decorative elements to ensure the user's content remains the focal point.

## Colors

The palette is anchored by a deep teal primary color, chosen for its balance of professional stability and energetic freshness. 

- **Primary (#0D9488):** Used for key actions, active states, and brand-touch points.
- **Surface (#FFFFFF):** All content cards and interactive components sit on pure white to distinguish them from the background.
- **Background (#F9FAFB):** A subtle off-white that provides enough contrast to make white surfaces "pop" without creating harsh glare.
- **Typography:** Charcoal (#111827) is used for high-readability body text and headers, while muted gray (#6B7280) handles metadata and secondary information.

## Typography

This design system utilizes **Inter** across all levels to maintain a clean, systematic, and utilitarian feel. 

Headlines use a tighter letter-spacing and heavier weights to create a strong visual anchor for content blocks. Body text is optimized for long-form reading in feeds with a generous line height. The `label-sm-caps` style is specifically reserved for metadata like "Sponsored" tags or category labels to differentiate them from interactive text.

## Layout & Spacing

The layout follows a **fluid grid** model optimized for mobile devices, transitioning to a centered **fixed grid** on larger screens to maintain readability.

- **Mobile:** A single-column feed with 16px horizontal margins.
- **Desktop:** The main feed is constrained to a 640px max-width to prevent line lengths from becoming tiring.
- **Vertical Rhythm:** A strict 4px/8px incremental system ensures consistency. Content within cards uses 16px padding for internal breathing room, while cards themselves are separated by 12px to 16px gaps.

## Elevation & Depth

Depth is conveyed through **ambient shadows** and **tonal layering**. 

Surfaces use a "Shadow-SM" approach: a very soft, diffused shadow (0px 1px 3px rgba(0,0,0,0.05), 0px 1px 2px rgba(0,0,0,0.03)) that suggests the card is hovering slightly above the off-white background. This creates a tactile feel without the heaviness of traditional skeuomorphism. Interactive elements like buttons may lift slightly (increased shadow) on hover or press to provide haptic-like visual feedback.

## Shapes

The shape language is defined by **large, pill-shaped curves**. 

Containers and feed cards use a 1.5rem (24px) corner radius to evoke a friendly and modern personality. Interactive elements like primary buttons and the persona switcher utilize a fully rounded (pill) style. This consistent "softness" across the interface makes the product feel approachable and reduces the "clinical" feel often associated with minimalist corporate designs.

## Components

### Buttons
Buttons are **rounded-full** (pill-shaped). 
- **Primary:** Deep Teal background with white text. 
- **Secondary:** Light gray or transparent background with Teal or Charcoal text. 
- **Sizing:** Minimum height of 48px for mobile tap targets.

### Feed Cards
Feed cards are the primary vessel for content. 
- **Header:** User avatar (rounded) and name/timestamp.
- **Media:** Full-width images or videos at the top with no top-radius (clipping to the card's top 24px radius).
- **Body:** 16px padding on sides and bottom for text content, reactions, and comments.

### Persona Switcher
A compact, pill-shaped dropdown. It features a small avatar and the current username, surrounded by a subtle border or a soft gray background. When tapped, it reveals a clean list of accounts with 8px spacing between items.

### Sponsored Tag
Small, uppercase text using the `label-sm-caps` style. It is rendered in muted gray (#6B7280) to remain visible but secondary to user-generated content.

### Input Fields
Inputs use a 24px corner radius to match cards. They feature a 1px border in a soft gray, which shifts to Teal on focus. Placeholder text uses the muted gray color.