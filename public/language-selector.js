/**
 * QualiLearn Language Selector Logic
 * Manages language preferences across all pages without requiring full page reloads.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Get initial language
    const currentLang = localStorage.getItem('ql_lang') || 'en';
    
    // 2. Initial translation pass
    applyLanguage(currentLang);

    // 3. Setup listeners for any language dropdown items
    // We target items with onclick="setLanguage(...)"
    const langLinks = document.querySelectorAll('[onclick^="setLanguage"]');
    langLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            // Extraction happens in the onclick or we rely on the onclick itself
        });
    });
});

/**
 * Updates the saved language and triggers a UI update
 */
async function setLanguage(langCode) {
    // Save to local storage
    localStorage.setItem('ql_lang', langCode);
    
    // Sync with server if logged in (optional/background)
    if (localStorage.getItem('ql_token')) {
        apiUpdateProfile({ language: langCode }).catch(err => console.warn("Profile sync skipped:", err));
    }

    // Apply translation without reloading for a premium feel
    applyLanguage(langCode);
    
    // Provide a small visual confirmation if possible
    if (typeof showToast === 'function') {
        const langNames = { 'en': 'English', 'ha': 'Hausa', 'yo': 'Yoruba', 'ig': 'Igbo', 'pi': 'Pidgin' };
        showToast(`Language set to ${langNames[langCode]}`);
    }
}

/**
 * Updates all data-i18n elements on the page
 */
function applyLanguage(langCode) {
    if (typeof translations === 'undefined') {
        console.error("Translations dictionary not found!");
        return;
    }

    const dict = translations[langCode] || translations['en'];

    // Update Language Dropdown Text in Navbar/Sidebar
    const langDisplays = document.querySelectorAll('.dropdown-toggle span, .profile-bubble span');
    langDisplays.forEach(span => {
        // Only update if it looks like a language code (2 chars uppercase)
        if (span.textContent.length === 2 && span.textContent === span.textContent.toUpperCase()) {
            span.textContent = langCode.toUpperCase();
        }
    });

    // Core Translation Loop
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translatedText = dict[key];

        if (translatedText) {
            // Check if element has an icon (i tag)
            const icon = el.querySelector('i');
            if (icon) {
                // Preserve the icon and update only the text node
                // Clear all except icon
                Array.from(el.childNodes).forEach(node => {
                    if (node !== icon) el.removeChild(node);
                });
                // Add translated text
                el.appendChild(document.createTextNode(' ' + translatedText));
            } else {
                // Direct replacement
                el.textContent = translatedText;
            }
        }
    });

    // Placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) el.setAttribute('placeholder', dict[key]);
    });

    // Titles (tooltips)
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (dict[key]) el.setAttribute('title', dict[key]);
    });

    // Update HTML lang attribute for accessibility
    document.documentElement.lang = langCode;
}

/**
 * Helper to get current language for API calls
 */
function getCurrentLang() {
    return localStorage.getItem('ql_lang') || 'en';
}
