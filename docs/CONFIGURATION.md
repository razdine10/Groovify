# Configuration Guide for Groovify

## 📁 Configuration Files Overview

Groovify uses **two separate configuration systems** with distinct purposes:

### 1. `.streamlit/config.toml` - Streamlit UI Configuration
**Purpose**: Controls the visual appearance of the Streamlit interface
**Format**: TOML (Streamlit's official format)
**Scope**: UI theming, layout, and Streamlit-specific settings

```toml
[theme]
backgroundColor = "#F5EEEF"          # Main background color
secondaryBackgroundColor = "#EFC0E3" # Sidebar/widget background
textColor = "#2D3748"                # Text color
primaryColor = "#B53E84"             # Accent color (buttons, links)
```

### 2. `config.py` - Application Business Configuration
**Purpose**: Contains application logic, database settings, and business rules
**Format**: Python module
**Scope**: Database connection, modules configuration, file paths, metadata

```python
DATABASE_CONFIG = {
    "host": "localhost",
    "database": "chinook",
    # ... other DB settings
}

MODULES = {
    "music": {"name": "Music Analytics", ...},
    # ... other modules
}
```

## 🎨 Theme Synchronization

Both configurations are **synchronized** to use the same color scheme:
- **Primary Color**: `#B53E84` (Rose)
- **Background**: `#F5EEEF` (Light Rose)
- **Secondary Background**: `#EFC0E3` (Light Purple)
- **Text Color**: `#2D3748` (Dark Gray)

## 🔧 When to Edit Which File

### Edit `.streamlit/config.toml` when:
- Changing colors/theme
- Adjusting Streamlit UI behavior
- Modifying layout defaults

### Edit `config.py` when:
- Adding new modules
- Changing database settings
- Updating application metadata
- Adding business logic constants

## 🚀 Environment Variables

Database settings in `config.py` can be overridden using environment variables:
- `DB_HOST`
- `DB_PORT` 
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

## ✅ Best Practices

1. **Keep colors synchronized** between both files
2. **Use environment variables** for sensitive data in production
3. **Document changes** when modifying either configuration
4. **Test changes** in both development and production environments 