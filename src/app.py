import pymongo
import random
import streamlit as st
from datetime import datetime
from pipelines import KgRagPipeline, TextRagPipeline

title = "RAG Arena"

about = """La RAG Arena est un outil d'évaluation d'assistants IA fondés sur la génération augmentée de récupération.
Elle a été élaborée dans le cadre de la thèse de Marion Schaeffer (Wikit/LITIS/INSA Rouen)."""

explanation_label = "Explications"
explanation = """Cette arène permet de comparer les performances de deux assistants IA en évaluant leurs réponses à des questions concernant les [services et dispositifs du Pôle Handicap de Villeneuve-la-Garenne](https://villeneuve92.com/services/sante-solidarites-prevention/centre-communal-daction-sociale/handicap-2/).

Posez vos questions sur les services proposés, les associations partenaires, les démarches administratives ou tout autre aspect lié au handicap à Villeneuve-la-Garenne.
Vous pourrez ensuite évaluer quelle réponse vous semble la plus pertinente et utile.

Vos évaluations doivent porter sur deux critères :

- La qualité formelle : clarté, structure et facilité de compréhension
- L'exactitude factuelle : conformité aux informations fournies via le lien précédent.
"""

chat_input_label = "Votre message..."

answer_a_label = "Réponse de l'assistant A"
answer_b_label = "Réponse de l'assistant B"

eval_button_a_label = "👈 A est meilleure"
eval_button_b_label = "👉 B est meilleure"
eval_button_tie_label = "🤝 Match nul"
eval_button_both_bad_label = "👎 Aucune des deux"


def save_eval(eval: str):
    """
    Saves user evaluation and query execution details to MongoDB and updates session state.
    
    Args:
        eval (str): Evaluation result ('A', 'B', 'TIE', or 'BOTH_BAD')
    """
    # Connect to MongoDB
    client = pymongo.MongoClient(st.secrets.mongo.uri)
    db = client[st.secrets.mongo.db_name]
    collection = db[st.secrets.mongo.collection_name]

    query_execution = st.session_state.query_execution
    query_execution["eval"] = eval

    # Save query execution in database
    collection.insert_one(query_execution)

    st.session_state.eval_count = st.session_state.eval_count + 1
    st.session_state.query_execution = None


def save_eval_a():
    save_eval("A")


def save_eval_b():
    save_eval("B")


def save_eval_tie():
    save_eval("TIE")


def save_eval_both_bad():
    save_eval("BOTH_BAD")


# Init Streamlit app
st.set_page_config(
    page_title=title, page_icon="🏟️", layout="centered", menu_items={"About": about}
)
st.title(title)

# Setup progress bar for slight gamification 🏆
eval_count_target = st.secrets.eval.eval_count_target
if "eval_count" not in st.session_state:
    st.session_state.eval_count = 0

if st.session_state.eval_count < eval_count_target:
    st.progress(st.session_state.eval_count / eval_count_target)
else:
    st.progress(1.0)  # 100% 🎯
    st.snow()

# Display explanation
with st.expander(explanation_label, icon="ℹ️"):
    st.markdown(explanation)

# Chat input
user_input = st.chat_input(chat_input_label)

if user_input:
    rag_pipelines = [KgRagPipeline(), TextRagPipeline()]
    random.shuffle(rag_pipelines)
    response_a = rag_pipelines[0].generate(user_input)
    response_b = rag_pipelines[1].generate(user_input)

    st.session_state.query_execution = {
        "query": user_input,
        "pipeline_a": rag_pipelines[0].name,
        "pipeline_b": rag_pipelines[1].name,
        "response_a": response_a,
        "response_b": response_b,
        "eval": None,
        "timestamp": datetime.now(),
    }

    # Display chat messages
    left_column, right_column = st.columns(2, gap="small")

    with left_column:
        with st.container(border=True):
            st.text(answer_a_label)
            with st.chat_message("user"):
                st.write(user_input)
            with st.chat_message("assistant"):
                st.write(response_a["answer"])

    with right_column:
        with st.container(border=True):
            st.text(answer_b_label)
            with st.chat_message("user"):
                st.write(user_input)
            with st.chat_message("assistant"):
                st.write(response_b["answer"])

    # Display evaluation buttons
    col1, col2, col3, col4 = st.columns(4, vertical_alignment="center")
    with col1:
        st.button(eval_button_a_label, use_container_width=True, on_click=save_eval_a)
    with col2:
        st.button(eval_button_b_label, use_container_width=True, on_click=save_eval_b)
    with col3:
        st.button(
            eval_button_tie_label, use_container_width=True, on_click=save_eval_tie
        )
    with col4:
        st.button(
            eval_button_both_bad_label,
            use_container_width=True,
            on_click=save_eval_both_bad,
        )
