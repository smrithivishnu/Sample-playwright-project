def extract_elements(page):
    return page.evaluate("""
    () => {
        return Array.from(document.querySelectorAll('*')).map(el => ({
            tag: el.tagName.toLowerCase(),
            text: el.innerText,
            id: el.id,
            class: el.className,
            name: el.getAttribute('name'),
            placeholder: el.getAttribute('placeholder'),
            aria: el.getAttribute('aria-label')
        }));
    }
    """)