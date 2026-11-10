import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL", "http://127.0.0.1:8000"
).rstrip("/")

st.set_page_config(
    page_title="Continuum Resource Navigator",
    page_icon="🧭",
)

st.title("Continuum Resource Navigator")
st.write("Find potential support resources based on individual need.")
st.caption(
    "Demo uses fictional resources. Enter fictional information only. "
    "Recommendations require staff review."
)

with st.form("inquiry_form"):
    inquiry = st.text_area(
        "What support does the individual need?",
        placeholder=(
            "An adult in Example County needs groceries "
            "because they cannot afford enough food."
        ),
        max_chars=3000,
        height=150,
    )

    submitted = st.form_submit_button("Find resources")

if submitted:
    if not inquiry.strip():
        st.warning("Enter a support need before submitting.")
        st.stop()

    try:
        with st.spinner("Reviewing available resources..."):
            response = requests.post(
                f"{API_BASE_URL}/ask",
                json={"inquiry": inquiry},
                timeout=45,
            )

        if response.status_code != 200:
            st.error(
                "The request could not be completed. "
                "Check the details below or try again."
            )
            st.write(response.json().get("detail", "Unexpected API error."))
            st.stop()

        result = response.json()
        # st.json(result)
        answer = result["answer"]

        st.subheader("Result")
        st.write(answer["message"])

        if answer["matches"]:
            st.subheader("Potential matches")

            for match in answer["matches"]:
                st.markdown(f"**{match['resource_id']}**")
                st.write(match["reason"])

        if answer["follow_up_questions"]:
            st.subheader("Information to clarify")

            for question in answer["follow_up_questions"]:
                st.write(f"• {question}")

        st.caption(
            f"Tokens used: {result['tokens_used']} |"
            f"Estimated cost: ${result['cost_usd']:.8f}"
        )

    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the resource navigator API.")
    except (requests.exceptions.RequestException, ValueError, KeyError):
        st.error("The service returned an unexpected response.")
