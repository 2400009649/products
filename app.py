import streamlit as st
from products import products
from translate import translations

def main():
    st.sidebar.title(get_translation("en", "Settings"))  # Example, defaulting to English for sidebar title
    lang_options = list(translations.keys())
    lang = st.sidebar.radio(get_translation("en", "Choose your language:"), lang_options)

    categories = list(set([product["category"] for product in products]))
    categories.sort()
    selected_category = st.sidebar.selectbox(get_translation(lang, "Choose a category:"), ['All'] + categories)

    st.title(get_translation(lang, "title"))

    if selected_category == 'All':
        for category in categories:
            st.header(category)
            category_products = [product for product in products if product["category"] == category]
            if category_products:
                paginate_products(category_products, lang, 10, category)  # Pass lang to pagination
            else:
                st.write(get_translation(lang, "no_products"))
    else:
        filtered_products = [product for product in products if product["category"] == selected_category]
        if filtered_products:
            paginate_products(filtered_products, lang, 10, selected_category)
        else:
            st.write(get_translation(lang, "no_products"))

def paginate_products(filtered_products, lang, max_per_page, key_prefix):
    total_pages = max(1, len(filtered_products) // max_per_page + (1 if len(filtered_products) % max_per_page > 0 else 0))
    
    if total_pages > 1:
        page = st.select_slider(get_translation(lang, "select_page"), options=list(range(1, total_pages + 1)), value=1, key=f"{key_prefix}_page")
        start_index = (page - 1) * max_per_page
        end_index = start_index + max_per_page
        products_to_display = filtered_products[start_index:end_index]
        display_products(products_to_display, lang)
    else:
        display_products(filtered_products, lang)

def get_translation(lang, text):
    # Function to handle missing translations more gracefully
    return translations[lang].get(text, f"Missing translation: {text}")


def display_products(products_to_display, lang):
    num_columns = 5
    cols = st.columns(num_columns)
    index = 0
    for product in products_to_display:
        with cols[index % num_columns]:
            st.image(product['image'], caption=product['name'], use_container_width=True)
            # Fetch the description in the selected language, fallback to English if not available
            description = product['description'].get(lang, product['description']['en'])
            st.caption(description)
            st.markdown(f"[{get_translation(lang, 'buy_now')}]({product['link']})", unsafe_allow_html=True)
        index += 1


if __name__ == "__main__":
    main()
