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
    with st.container(border=True):
        display_question_parts(question)

def save_mark(key):
    st.session_state.results[key] = st.session_state[key]

def display_question_parts(question, prefix="mark",level=0):

    current_prefix = f"{prefix}_{question.identifier}"

    for index, item in enumerate(question._subparts):
        if level == 0:
            st.markdown(f"### {item.identifier})")
        if not item.marks:
            display_question_parts(item,current_prefix, level+1)
        else:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    if not level ==0:
                        st.markdown(f"**{item.identifier})**")
                with col2:
                    res_key = f"{current_prefix}_{item.identifier}"
                    if res_key not in st.session_state.results:
                        st.session_state.results[res_key] = 0
                    saved_value = st.session_state.results.get(res_key, 0)
                    options = list(range(item.marks + 1))
                    try:
                        current_index = options.index(saved_value)
                    except ValueError:
                        print("ValueError")
                        current_index = 0
                    st.radio(
                        "Marks", 
                        options = options, 
                        horizontal=True, 
                        key=res_key, 
                        label_visibility="collapsed",
                        index=current_index,
                        on_change=save_mark,
                        args=(res_key,)
                        )
                st.markdown('<div class="sub-part-line"></div>', unsafe_allow_html=True)


def Create_form(paper):

    local_css("style.css")

    if 'step' not in st.session_state:
        st.session_state.step=0
    if "results" not in st.session_state:
        st.session_state.results = {}

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    with st.container():
        if st.session_state.step ==0:
            class_index=None
            if st.session_state.results.get('class'):
                class_index = classes.index(st.session_state.results.get('class'))
            print(st.session_state.get('class'))
            print(class_index)
            st.title(f"{paper.identifier}")
            st.markdown("---")
            std_name = st.text_input("Full Name:",value =st.session_state.results.get('name')  )
            std_class = st.selectbox ("class", options = classes,index = class_index )

        if 0 <= st.session_state.step <= paper.get_length()-1:
            st.markdown(
            """ 
            Enter your marks below, question by question. 
            """
            )
            display_questions(st.session_state.step,paper)

        if 0 == st.session_state.step:
            col1, col2, col3 = st.columns([1,2,1])
            with col3:
                # Determine if we are on the last question
                if st.button( "Next ➡", type="primary"):
                    if std_name and std_class:
                        st.session_state.results['name'] = std_name
                        st.session_state.results['class'] = std_class
                        next_step()
                        st.rerun()
                    else:
                        st.error("Please enter your name and class to continue.")

        if 1 <= st.session_state.step <= paper.get_length()-1:
            
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("⬅ Back"):
                    st.session_state.step -= 1
                    st.rerun()
            with col3:
                # Determine if we are on the last question
                is_last = st.session_state.step == len(paper._questions)
                if st.button("Next ➡", type="primary"):
                    st.session_state.step += 1
                    st.rerun()




        # --- FINAL STEP: Submit ---
        if st.session_state.step == paper.get_length():
            st.title("Review & Submit")
            st.write(f"Name: {st.session_state.results.get('name')}")
            st.write(f"Your Answers: {st.session_state.results}")
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("⬅ Back"):
                    st.session_state.step -= 1
            with col3:
                if st.button("Submit", disabled=st.session_state.submitted):
                # This is where you would call your SQL/SharePoint save function
                    st.session_state.submitted = True
                    st.success("Results submitted successfully!")
                    st.balloons()
                    st.rerun()


     

