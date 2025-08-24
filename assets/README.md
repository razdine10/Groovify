# Assets Directory

This directory contains all the static assets used in the Groovify application.

## Directory Structure

```
assets/
├── img/                    # Images and visual assets
│   └── groovify-logo.png  # Main application logo
└── README.md              # This documentation file
```

## Images (`img/`)

### Logo Files
- **groovify-logo.png**: Main application logo (1.39MB)
  - Used in the sidebar navigation
  - Used in the home page header
  - Format: PNG with transparency
  - Dimensions: High resolution for crisp display

## Usage in Code

The logo is referenced in:
- `utils.py`: Sidebar logo display function
- `pages/home/home.py`: Home page header

## Adding New Assets

When adding new assets:
1. Place images in the `img/` subdirectory
2. Use descriptive, lowercase filenames with hyphens
3. Update this README with new asset descriptions
4. Consider file size optimization for web performance

## File Naming Convention

- Use lowercase letters
- Separate words with hyphens (kebab-case)
- Include file format in extension
- Example: `company-logo.png`, `background-image.jpg` 