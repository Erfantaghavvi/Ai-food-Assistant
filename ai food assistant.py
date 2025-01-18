import streamlit as st
from huggingface_hub import InferenceClient

# راه‌اندازی InferenceClient
client = InferenceClient(api_key="your api key")


def get_recipe(food_name):
    # ارسال درخواست به مدل Qwen2.5 برای دریافت دستور پخت به زبان فارسی
    messages = [
        {"role": "user", "content": f"لطفاً دستور پخت {food_name} را به زبان فارسی برای من فراهم کن."}
    ]

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        recipe = response['choices'][0]['message']['content']
        return recipe
    except Exception as e:
        return f"خطا در دریافت دستور پخت: {str(e)}"


def extract_ingredients(recipe):
    # ارسال درخواست به مدل Qwen2.5 برای استخراج مواد لازم به زبان فارسی
    messages = [
        {"role": "user", "content": f"لطفاً مواد لازم برای دستور پخت زیر را به زبان فارسی استخراج کن:\n{recipe}"}
    ]

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=messages,
            temperature=0.5,
            max_tokens=2024
        )
        ingredients = response['choices'][0]['message']['content']
        return ingredients.split('\n')
    except Exception as e:
        return f"خطا در استخراج مواد لازم: {str(e)}"


def search_snapp_food(ingredients):
    # جستجو در اسنپ‌فود (لینک‌های فرضی)
    links = []
    for ingredient in ingredients:
        links.append(f"https://snappfood.ir/search?query={ingredient}")
    return links


def main():
    st.title("🧑‍🍳 دستیارآشپزی هوشمند")
    st.write("به دستیار آشپزی  خوش آمدید! اسم غذایی که می‌خواهید دستور پخت آن را دریافت کنید وارد کنید.")

    # دریافت نام غذا از کاربر
    food_name = st.text_input("اسم غذا را وارد کنید (به فارسی یا انگلیسی):")

    if st.button("📋 دریافت اطلاعات غذا"):
        if food_name.strip():
            with st.spinner("در حال دریافت اطلاعات..."):
                recipe = get_recipe(food_name)
                if recipe and not recipe.startswith("خطا"):
                    st.subheader("🍲 دستور پخت")
                    st.write(recipe)

                    # استخراج مواد لازم
                    ingredients = extract_ingredients(recipe)
                    if ingredients:
                        st.subheader("🛒 مواد لازم")
                        for ingredient in ingredients:
                            st.write(f"- {ingredient}")

                        # نمایش لینک‌های خرید
                        st.subheader("📦 لینک‌های خرید از اسنپ‌فود")
                        links = search_snapp_food(ingredients)
                        for ingredient, link in zip(ingredients, links):
                            st.markdown(f"- [{ingredient}]({link})")
                    else:
                        st.warning("مواد لازم یافت نشد.")
                else:
                    st.error("خطایی در دریافت دستور پخت رخ داده است!")
        else:
            st.error("لطفاً اسم غذا را وارد کنید.")


if __name__ == "__main__":
    main()
