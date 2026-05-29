---
name: Vibrant Marketplace
colors:
  surface: '#fbf9f9'
  surface-dim: '#dbdad9'
  surface-bright: '#fbf9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f3'
  surface-container: '#efeded'
  surface-container-high: '#e9e8e7'
  surface-container-highest: '#e4e2e2'
  on-surface: '#1b1c1c'
  on-surface-variant: '#5a3f45'
  inverse-surface: '#303031'
  inverse-on-surface: '#f2f0f0'
  outline: '#8e6f75'
  outline-variant: '#e3bdc4'
  surface-tint: '#bb0055'
  primary: '#ac004d'
  on-primary: '#ffffff'
  primary-container: '#d70f64'
  on-primary-container: '#ffeff0'
  inverse-primary: '#ffb1c2'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e4e2e1'
  on-secondary-container: '#656464'
  tertiary: '#545757'
  on-tertiary: '#ffffff'
  tertiary-container: '#6d6f6f'
  on-tertiary-container: '#f2f3f3'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd9df'
  primary-fixed-dim: '#ffb1c2'
  on-primary-fixed: '#3f0018'
  on-primary-fixed-variant: '#8f003f'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474747'
  tertiary-fixed: '#e1e3e3'
  tertiary-fixed-dim: '#c5c7c7'
  on-tertiary-fixed: '#191c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#fbf9f9'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e2'
  surface-muted: '#F7F8F8'
  text-primary: '#333333'
  text-secondary: '#707070'
  brand-pink-light: '#FFECF3'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
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
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1200px
  gutter: 24px
  margin-desktop: 48px
  margin-mobile: 16px
---

## Brand & Style

This design system is built on a foundation of high-energy efficiency and consumer delight. It balances a professional, corporate structure with an approachable, friendly aesthetic suitable for a high-frequency food and grocery delivery service. 

The style is **Corporate / Modern** with a focus on high-quality visual content. It leverages significant whitespace to allow vibrant food photography to take center stage, while the signature magenta provides a strong visual thread that guides the user through the conversion funnel. The interface should feel fast, reliable, and deeply localized to the urban energy of Dhaka.

## Colors

The palette is dominated by the primary brand magenta, used strategically for calls-to-action, active states, and brand identifiers. 

- **Primary (#D70F64):** The core brand color. Use for "order" buttons, price highlights, and primary navigation.
- **Surface & Background:** The primary background is pure white (#FFFFFF) to maintain a clean aesthetic. Use the muted off-white (#F7F8F8) for section backgrounds and container fills to separate content areas.
- **Typography:** Use the dark charcoal (#333333) for all primary headings and body text to ensure high legibility. The neutral grey (#707070) is reserved for secondary information like meta-data, breadcrumbs, and disabled states.

## Typography

The design system utilizes a single-font strategy using **Inter** to ensure maximum clarity and a systematic, modern appearance. 

The typographic hierarchy is bold and direct. Headlines use tighter letter spacing and heavy weights to create a sense of urgency and importance. Body text is kept clean with generous line heights to ensure readability during fast browsing. For localized content (Bengali script), the line-height should be increased by 15% to accommodate character heights and flourishes without crowding.

## Layout & Spacing

The layout follows a **Fixed Grid** model on desktop, centered within the viewport with a maximum width of 1200px. This ensures a consistent viewing experience on larger monitors.

- **Grid System:** A 12-column grid is used for desktop layouts, transitioning to a 4-column grid for mobile devices.
- **Rhythm:** An 8px base unit drives all spacing decisions. Standard component padding is 16px (2 units), while section vertical spacing is typically 64px (8 units) or 80px (10 units).
- **Responsive Behavior:** On tablet, margins reduce to 32px. On mobile, margins drop to 16px, and components like horizontal restaurant lists become side-scrolling carousels to save vertical space.

## Elevation & Depth

Visual hierarchy is achieved through a combination of **Tonal Layers** and **Ambient Shadows**. 

The design avoids heavy gradients. Depth is instead conveyed by:
- **Level 0 (Base):** Pure white background for the main canvas.
- **Level 1 (Card):** White surfaces with a very soft, diffused shadow (`0px 4px 16px rgba(0, 0, 0, 0.06)`) and a subtle 1px border in `#EEEEEE`.
- **Level 2 (Interaction):** Hover states on cards should increase the shadow spread and lift the element slightly (y-axis offset) to provide tactile feedback.
- **Level 3 (Sticky/Floating):** Navigation bars and floating "View Cart" buttons use a more pronounced shadow and a backdrop blur (glassmorphism) if appearing over photographic backgrounds.

## Shapes

The shape language is approachable and modern, defined by **Rounded** corners that mirror the friendly nature of the brand.

Standard buttons and input fields utilize a `0.5rem` (8px) radius. Larger containers, such as restaurant cards and promotional banners, use `rounded-lg` at `1rem` (16px) to create a softer, more consumer-friendly frame for food photography. Iconic elements like category chips or price tags may use a full pill-shape (32px+) to distinguish them from standard buttons.

## Components

### Buttons
- **Primary:** Solid #D70F64 background with white text. High-contrast, bold weight.
- **Secondary:** White background with #D70F64 border and text.
- **Ghost:** No background or border, magenta text. Used for less critical actions like "See all."

### Cards
Restaurant and grocery cards are the primary units of the UI. They must feature a high-aspect-ratio image at the top with a 16px corner radius. Content below the image includes the name (bold), delivery time (with an icon), and rating. Use white space between text elements rather than dividers.

### Inputs & Search
The main search bar is a critical component. It should be large, featuring a 16px corner radius, a subtle inner shadow or light grey border, and a prominent pink "Search" button or magnifying glass icon.

### Chips & Tags
Used for cuisine types (e.g., "Bengali," "Pizza") and delivery status. These use the `#F7F8F8` background with `#333333` text and a pill-shaped radius.

### Navigation
Desktop navigation is sticky at the top, featuring a simplified logo, location picker (Dhaka specific), and user account/cart icons. The location picker should be visually distinct to emphasize the localized nature of the service.