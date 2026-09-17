import streamlit as st
from main import process_entry
from db import init_db

st.set_page_config(page_title="Mood Companion", page_icon="📓")
st.title("📓 Pattern-Aware Journal")
st.caption("A journaling companion that notices recurring patterns in how you're feeling — and reflects them back to you.")

init_db()

entry_text = st.text_area("What's on your mind today?", height=150)

if st.button("Save entry"):
    if entry_text.strip():
        with st.spinner("Thinking..."):
            result = process_entry(entry_text)

        if result["type"] == "crisis":
            st.error(result["message"])

        elif result["type"] == "pattern":
            st.success("Entry saved.")
            st.markdown("### 💭 A pattern I noticed")
            st.write(result["message"])

            with st.expander("See the related past entries"):
                for m in result["matches"]:
                    st.markdown(f"- *{m['text']}*")

        else:
            st.success("Entry saved.")
    else:
        st.warning("Write something first.")