import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import smtplib
from email.mime.text import MIMEText

from database import insert_results, search_reviews, clear_table ,insert_filtered_results,create_filtered_table
create_filtered_table()

# ---------------- SESSION ----------------
if "processed" not in st.session_state:
    st.session_state.processed = False

# ---------------- PAGE ----------------
st.set_page_config(page_title="Parallel Text Processing", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
# MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    max-width: 1000px;
    margin: auto;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #6C63FF;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 25px;
}

.stButton>button {
    background: linear-gradient(45deg, #6C63FF, #00C9A7);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚀 Parallel Text Processing</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Advanced Text Analyzer with Parallel Processing</div>", unsafe_allow_html=True)

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("📂 Upload TXT,csv,xlsx,json File", type=["txt","csv","xlsx","json"])

col1, col2 = st.columns(2)

with col1:
    start = st.button("⚡ Start Processing")
    if start and uploaded_file is None:
        st.warning("please upload the file first.")

with col2:
    if st.button("🧹 Clear Database"):
        clear_table()
        st.success("Database Cleared")

# ---------------- SENTIMENT FUNCTION ----------------
def process_text(text):
    t = text.lower()

    positive_words = [
        "good","excellent","amazing","awesome","great",
        "happy","satisfied","perfect","love","nice"
    ]

    negative_words = [
        "bad","worst","poor","terrible","awful",
        "hate","issue","problem","delay","broken"
    ]

    pos = sum(word in t for word in positive_words)
    neg = sum(word in t for word in negative_words)

    if pos == 0 and neg == 0:
        return 0, "Neutral"
    elif pos > neg:
        return pos, "Positive"
    elif neg > pos:
        return -neg, "Negative"
    else:
        return 0, "Neutral"

# ---------------- PROCESSING ----------------
if uploaded_file and start:

    clear_table()
    st.session_state.processed = False

    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "txt":
        content = uploaded_file.read().decode("utf-8")
        lines = [line.strip() for line in content.split("\n") if line.strip()]

    elif file_type == "csv":
        try:
            df_input=pd.read_csv(uploaded_file)
            if df_input.empty:
                st.error("File is empty")
                st.stop()
            
    
            lines = df_input.iloc[:, 0].dropna().astype(str).tolist()
        except Exception:
            st.error("Empty or invalid CSV file.")
            st.stop()

    elif file_type == "xlsx":
        try:
            df_input = pd.read_excel(uploaded_file)

            if df_input.empty:
                st.error("⚠ File is empty")
                st.stop()

            lines = df_input.iloc[:, 0].dropna().astype(str).tolist()

        except Exception:
            st.error("⚠ Empty or invalid Excel file")
            st.stop()

    elif file_type == "json":
        df_input = pd.read_json(uploaded_file)
        lines = df_input.iloc[:, 0].dropna().astype(str).tolist()

    else:
        st.error("Unsupported file type ❌")
        st.stop()
    if not lines or len(lines)==0:
        st.error("File is empty.")
    if all(str(line).strip()=="" for line in lines):
        st.error("File contains no valid data")
        st.stop()

    progress = st.progress(0)
    log = st.empty()

    # -------- NORMAL PROCESS --------
    start_n = time.time()
    for text in lines:
        process_text(text)
    normal_time = time.time() - start_n

    # -------- PARALLEL PROCESS --------
    def worker(text):
        score, sentiment = process_text(text)
        return {
            "review_text": text,
            "score": score,
            "sentiment": sentiment,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    start_p = time.time()

    results = []
    with ThreadPoolExecutor() as executor:
        for i, res in enumerate(executor.map(worker, lines)):
            results.append([res])
            if len(lines)<1000 or i%1000 ==0:
                progress.progress(min((i+1)/len(lines),1.0))
            # progress.progress((i+1)/len(lines))
            # log.text(f"Processing {i+1}/{len(lines)}")
            if i!=0 and i%5000==0:
                log.text(f"Processed {i} lines...")
    progress.progress(1.0)
    log.text(f"processed {len(lines)} lines...")

    parallel_time = time.time() - start_p

    # store times
    st.session_state.normal_time = normal_time
    st.session_state.parallel_time = parallel_time

    insert_results(results)

    st.session_state.processed = True
    st.success(f"✅ Completed {len(results)} lines")

# ---------------- DISPLAY ----------------
if st.session_state.processed:

    rows = search_reviews()

    if rows:
        df = pd.DataFrame(rows, columns=["Text","Score","Sentiment","Time"])

        st.subheader("📊 Dashboard")

        total = len(df)
        pos = len(df[df["Sentiment"]=="Positive"])
        neg = len(df[df["Sentiment"]=="Negative"])
        neu = len(df[df["Sentiment"]=="Neutral"])

        col1,col2,col3,col4 = st.columns(4)
        col1.metric("Total", total)
        col2.metric("Positive", pos)
        col3.metric("Negative", neg)
        col4.metric("Neutral", neu)

        # -------- PIE CHART --------
        col1,col2,col3 = st.columns([1,2,1])
        with col2:
            fig, ax = plt.subplots(figsize=(3,3))
            ax.pie([pos,neg,neu],
                   labels=["Positive","Negative","Neutral"],
                   autopct="%1.1f%%",
                   textprops={'fontsize':8})
            st.pyplot(fig)

        # -------- PERFORMANCE --------
        st.subheader("⚡ Performance Comparison")

        times = {
            "Normal": st.session_state.normal_time,
            "Parallel": st.session_state.parallel_time
        }

        st.bar_chart(times)

        st.write(f"Normal: {times['Normal']:.4f}s")
        st.write(f"Parallel: {times['Parallel']:.4f}s")

        # -------- DOWNLOAD --------
        csv = df.to_csv(index=False).encode()
        st.download_button("📥 Download CSV", csv, "results.csv")

        # -------- SEARCH --------
        # -------- SEARCH --------

        # -------- SESSION --------
        import re 
        if "filtered" not in st.session_state:
            st.session_state.filtered = None

        # -------- SEARCH --------
        keyword = st.text_input("🔍 Search")
        search_btn = st.button("Search")

        if search_btn:

            if keyword.strip() == "":
                st.warning("Please enter a keyword.")
                st.stop()

            stop_words = {"this","is","the","and","a","an"}
            words = {w for w in keyword.lower().split() if w not in stop_words}

            import time
            start_time=time.time()
            
            filtered = df[df["Text"].apply(
                lambda text: any(word in text.lower() for word in words)
            )]
            end_time=time.time()
            st.write(f"Search time:{round(end_time-start_time,4)}seconds")
            

            st.session_state.filtered = filtered   # ✅ STORE RESULT

        # -------- DISPLAY --------
        if st.session_state.filtered is not None:

            st.write(f"Results: {len(st.session_state.filtered)}")
            st.dataframe(st.session_state.filtered)
            st.write(f"Total records:{len(df)}")
            st.write(f"Filtered records:{len(st.session_state.filtered)}")

            # -------- STORE BUTTON --------
            if st.button("💾 Store Filtered Data"):

                filtered_data = []

                for _, row in st.session_state.filtered.iterrows():
                    filtered_data.append((
                        row["Text"],
                        row["Sentiment"],
                        row["Time"]
                    ))

                # st.write("Rows to insert:", len(filtered_data))  # debug

                insert_filtered_results(filtered_data)

                st.success("Filtered data stored successfully ✅")
                
            # ---------------- SENTIMENT ANALYSIS ----------------

            positive_words = [
                "good","great","excellent","amazing","awesome","fantastic","wonderful",
                "perfect","nice","best","positive","happy","satisfied","love","liked",
                "enjoy","fast","smooth","easy","helpful","useful","friendly","clean",
                "beautiful","brilliant","super","cool","impressive","reliable","efficient","acceptable","fine","okay","average","satisfactory"
            ]

            negative_words = [
                "bad","worst","poor","terrible","awful","hate","issue","problem",
                "error","bug","fail","failed","slow","delay","broken","difficult",
                "hard","confusing","annoying","frustrating","disappointed",
                "unreliable","weak","boring","useless","waste","rude","dirty"
            ]

            intensifiers = ["very","extremely","too","highly"]

            words_in_line = re.findall(r'\b\w+\b', keyword.lower())
            if "but" in words_in_line:
                but_index=words_in_line.index("but")
            else:
                but_index=-1

            pos_count = 0
            neg_count = 0

            # -------- MAIN LOGIC --------
            for i, w in enumerate(words_in_line):
                weight=1
                if but_index!=-1 and i>but_index:
                    weight=2

                # NEGATION HANDLING
                if i > 0 and words_in_line[i-1] == "not":
                    if w in positive_words:
                        neg_count += 1
                        continue
                    elif w in negative_words:
                        pos_count += 1
                        continue

                # POSITIVE
                if w in positive_words:
                    if i > 0 and words_in_line[i-1] in intensifiers:
                        pos_count += 2
                    else:
                        pos_count += 1

                # NEGATIVE
                elif w in negative_words:
                    if i > 0 and words_in_line[i-1] in intensifiers:
                        neg_count += 2
                    else:
                        neg_count += 1

            total_words = len(words_in_line)
            neu_count = total_words - (pos_count + neg_count)

            # -------- DISPLAY --------
            st.write(f"🟢 Positive words: {pos_count}")
            st.write(f"🔴 Negative words: {neg_count}")
            st.write(f"⚪ Neutral words: {neu_count}")

            # -------- SCORE --------
            if total_words > 0:
                score = (pos_count - neg_count) / total_words
            else:
                score = 0

            st.write(f"⚖ Sentiment Score: {round(score, 2)}")

            # -------- FINAL RESULT --------
            if score > 0.1:
                st.success("Overall Sentiment: Positive 😊")
            elif score < -0.1:
                st.error("Overall Sentiment: Negative 😞")
            else:
                st.info("Overall Sentiment: Neutral 😐")
        # keyword = st.text_input("🔍 Search")
        # search_btn = st.button("Search")

        # if search_btn:

        #     if keyword.strip() == "":
        #         st.warning("Please enter a keyword.")
        #         st.stop()

        #     import re

        #     stop_words = ["this","is","the","and","a","an"]
        #     words = [w for w in keyword.lower().split() if w not in stop_words]

        #     filtered = df[df["Text"].apply(
        #         lambda text: any(word in text.lower() for word in words)
        #     )]

        #     st.write(f"Results: {len(filtered)}")

        #     if len(filtered) > 0:
        #         st.dataframe(filtered)
        #     else:
        #         st.warning("No results found ❌")

        #     # ✅ SENTIMENT ALWAYS RUNS (IMPORTANT)

        #     positive_words = [
        #         "good","excellent","amazing","awesome","great",
        #         "happy","satisfied","perfect","love","nice"
        #     ]

        #     negative_words = [
        #         "bad","worst","poor","terrible","awful",
        #         "hate","issue","problem","delay","broken"
        #     ]

        #     words_in_line = re.findall(r'\b\w+\b', keyword.lower())

        #     pos_count = 0
        #     neg_count = 0

        #     for w in words_in_line:
        #         if w in positive_words:
        #             pos_count += 1
        #         elif w in negative_words:
        #             neg_count += 1

        #     st.write(f"🟢 Total Positive words: {pos_count}")
        #     st.write(f"🔴 Total Negative words: {neg_count}")

        #     final_score = pos_count - neg_count
        #     st.write(f"⚖ Sentiment Score: {final_score}")

        #     if final_score > 0:
        #         st.success("Overall Sentiment: Positive")
        #     elif final_score < 0:
        #         st.error("Overall Sentiment: Negative")
        #     else:
        #         st.info("Overall Sentiment: Neutral")

        # -------- TABLE --------
        st.subheader("📄 Results")
        st.dataframe(df)

        # -------- EMAIL --------
        st.subheader("📧 Send Report")

        email = st.text_input("Enter email")

        if st.button("Send Email"):

            SENDER_EMAIL = "sathvikakasula2005@gmail.com"
            APP_PASSWORD = "jyumrnsgvrsazdgo"

            msg = MIMEText(f"""
            Total: {total}
            Positive: {pos}
            Negative: {neg}
            Neutral: {neu}
            """)

            msg["Subject"] = "Text Processing Report"
            msg["From"] = SENDER_EMAIL
            msg["To"] = email

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
                server.quit()

                st.success("Email sent ✅")
            except Exception as e:
                st.error("Email failed ❌")

    else:
        st.warning("No data available")