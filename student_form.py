import streamlit as st

classes = ["O1","O2","O3","O4","O5"]

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def next_step():
    st.session_state.step += 1

def previous_step():
    st.session_state.step -= 1

def display_questions(step, paper):

    question = paper.get_question(step)
    st.markdown(
       f"## Question {question.identifier}"
    )
    display_question_parts(question)

def display_question_parts(question):
    for item in question._subparts:
        if item.marks:
                st.radio(f" {item.identifier}:", range(item.marks),horizontal =True)
        else:
            st.markdown(f"{item.identifier}")
            display_question_parts(item)




def Create_form(paper):

    local_css("style.css")

    if 'step' not in st.session_state:
        st.session_state.step=0
    if "results" not in st.session_state:
        st.session_state.results = {}
    with st.container():
        if st.session_state.step ==0:
            st.title(f"{paper.identifier}")
            st.markdown("---")
            std_name = st.text_input("Full Name:")
            std_class = st.selectbox ("class", classes)

        display_questions(st.session_state.step,paper)

        if st.button("Next", type="primary"):
            if std_name:
                st.session_state.results['name'] = std_name
                next_step()
                st.rerun()
            else:
                st.error("Please enter your name to continue.")

        elif 1 <= st.session_state.step <= paper.get_length():
            step = st.session_state.step
            st.title(f"Question {step}")
            
            # Unique key for session state based on question number
            q_key = f"q_{step}"
            val = st.number_input(f"Enter marks for Q{step}", 
                                min_value=0, max_value=10, 
                                value=st.session_state.results.get(q_key, 0))
            
            st.session_state.results[q_key] = val

            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("⬅ Back"):
                    st.session_state.step -= 1
                    st.rerun()
            with col3:
                # Determine if we are on the last question
                is_last = st.session_state.step == len(paper._questions)
                if st.button("Submit 🚀" if is_last else "Next ➡", type="primary"):
                    st.session_state.step += 1
                    st.rerun()

        # --- FINAL STEP: Submit ---
        elif st.session_state.step == 3:
            st.title("Review & Submit")
            st.write(f"Name: {st.session_state.results.get('name')}")
            st.write(f"Your Answers: {st.session_state.results}")
            
            if st.button("Confirm and Submit"):
                # This is where you would call your SQL/SharePoint save function
                st.success("Results submitted successfully!")
                # Reset the form
                if st.button("Start New Entry"):
                    st.session_state.step = 0
                    st.session_state.results = {}
                    st.rerun()
            st.markdown(
            """ 
            Enter your marks below, question by question. 
            """
            )

