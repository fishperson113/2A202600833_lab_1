import os
import sys
import streamlit as st

# Import functions từ template.py
sys.path.insert(0, os.path.dirname(__file__))
from template import (
    call_openai, call_openai_mini, compare_models,
    batch_compare, format_comparison_table,
    OPENAI_MODEL, OPENAI_MINI_MODEL,
)
from openai import OpenAI

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Day 1 — LLM Lab", layout="wide")
st.title("🤖 Day 1 — LLM API Lab")


def show_api_error(action: str, error: Exception) -> None:
    st.error(f"{action} failed. Please try again.")
    st.caption(f"{type(error).__name__}: {error}")

# (Parameters removed from global UI — per-tab controls are used instead)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_single, tab_chat, tab_compare, tab_batch = st.tabs(["🧪 Single Call", "💬 Chat", "⚖️ Compare Models", "📋 Batch Compare"])


# ── Tab 0: Single call with model switcher ──────────────────────────────────
with tab_single:
    st.subheader("Single API Call")

    model_label = st.selectbox(
        "Model",
        ["GPT-4o", "GPT-4o-mini"],
        index=0,
    )
    prompt = st.text_area(
        "Prompt",
        "Explain the difference between temperature and top_p in one sentence.",
        height=120,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, key="single_temperature")
    with col_b:
        top_p = st.slider("Top-p", 0.0, 1.0, 0.9, 0.05, key="single_top_p")
    max_tokens = st.slider("Max tokens", 64, 1024, 256, 64, key="single_max_tokens")

    if st.button("🚀 Run Single Call", key="btn_single"):
        try:
            with st.spinner("Calling model..."):
                if model_label == "GPT-4o-mini":
                    response_text, latency = call_openai_mini(
                        prompt,
                        temperature=temperature,
                        top_p=top_p,
                        max_tokens=max_tokens,
                    )
                    model_name = OPENAI_MINI_MODEL
                else:
                    response_text, latency = call_openai(
                        prompt,
                        model=OPENAI_MODEL,
                        temperature=temperature,
                        top_p=top_p,
                        max_tokens=max_tokens,
                    )
                    model_name = OPENAI_MODEL

            st.markdown(f"**Model:** `{model_name}`")
            st.markdown("**Response:**")
            st.write(response_text)
            st.metric("Latency", f"{latency:.2f}s")
        except Exception as error:
            show_api_error("Single call", error)


# ── Tab 1: Streaming chatbot ─────────────────────────────────────────────────
with tab_chat:
    st.subheader("Streaming Chatbot (GPT-4o · short-term memory in RAM)")

    # Chat-specific controls (local params and clear history)
    col_t, col_p, col_m, col_btn = st.columns([1, 1, 1, 1])
    with col_t:
        chat_temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, key="chat_temperature")
    with col_p:
        chat_top_p = st.slider("Top-p", 0.0, 1.0, 0.9, 0.05, key="chat_top_p")
    with col_m:
        chat_max_tokens = st.slider("Max tokens", 64, 1024, 256, 64, key="chat_max_tokens")
    with col_btn:
        if st.button("🗑️ Clear chat history", key="clear_chat"):
            st.session_state.history = []
            st.rerun()

    if "history" not in st.session_state:
        st.session_state.history = []   # simple array — short-term memory

    # Render history
    for msg in st.session_state.history:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Type a message..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # perform streaming call immediately in the same run (no rerun)
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            stream = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=st.session_state.history,
                temperature=chat_temperature,
                top_p=chat_top_p,
                max_tokens=chat_max_tokens,
                stream=True,
            )
            response = st.write_stream(stream)

            st.session_state.history.append({"role": "assistant", "content": response})
            # Keep last 3 turns (6 messages)
            st.session_state.history = st.session_state.history[-6:]
        except Exception as error:
            show_api_error("Chat streaming", error)


# ── Tab 2: Compare GPT-4o vs Mini ────────────────────────────────────────────
with tab_compare:
    st.subheader("Compare GPT-4o vs GPT-4o-mini")

    compare_prompt = st.text_area("Prompt", "Explain the difference between temperature and top_p in one sentence.", height=100)

    if st.button("🚀 Run Comparison", key="btn_compare"):
        try:
            with st.spinner("Calling both models..."):
                result = compare_models(compare_prompt)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### GPT-4o")
                st.info(result["gpt4o_response"])
                st.metric("Latency", f"{result['gpt4o_latency']:.2f}s")
                st.metric("Cost estimate", f"${result['gpt4o_cost_estimate']:.5f}")

            with col2:
                st.markdown(f"### GPT-4o-mini")
                st.info(result["mini_response"])
                st.metric("Latency", f"{result['mini_latency']:.2f}s")
                st.metric("Cost estimate", "~$0.00006 est.")

            # Latency bar chart
            st.divider()
            st.bar_chart({"GPT-4o": result["gpt4o_latency"], "GPT-4o-mini": result["mini_latency"]})
        except Exception as error:
            show_api_error("Model comparison", error)


# ── Tab 3: Batch Compare ─────────────────────────────────────────────────────
with tab_batch:
    st.subheader("Batch Compare — multiple prompts at once")

    default_prompts = "What is 2+2?\nName one planet.\nWhat color is the sky?"
    raw = st.text_area("Prompts (one per line)", default_prompts, height=150)

    if st.button("🚀 Run Batch", key="btn_batch"):
        prompts = [p.strip() for p in raw.splitlines() if p.strip()]
        if not prompts:
            st.warning("Enter at least one prompt.")
        else:
            try:
                with st.spinner(f"Running {len(prompts)} comparisons..."):
                    results = batch_compare(prompts)

                # Table via streamlit dataframe
                import pandas as pd
                df = pd.DataFrame([{
                    "Prompt":          r["prompt"],
                    "GPT-4o Response": r["gpt4o_response"][:80],
                    "Mini Response":   r["mini_response"][:80],
                    "GPT-4o Latency":  f"{r['gpt4o_latency']:.2f}s",
                    "Mini Latency":    f"{r['mini_latency']:.2f}s",
                    "Cost Estimate":   f"${r['gpt4o_cost_estimate']:.5f}",
                } for r in results])
                st.dataframe(df, use_container_width=True)

                # Raw text table (format_comparison_table)
                with st.expander("📄 Raw text table"):
                    st.code(format_comparison_table(results), language="text")
            except Exception as error:
                show_api_error("Batch compare", error)
