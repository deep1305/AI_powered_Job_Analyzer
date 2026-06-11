import streamlit as st

class JobAnalyzerUI:

    def header(self):
        st.title("Evolvue Job Analyzer")
        st.caption("Resume vs JD Analyzer")
        st.divider()

    def sidebar(self):
        with st.sidebar:
            st.header("API Key configuration")
            return st.text_input("Open AI API Key Here" , type="password")
        
    def upload_resume(self):
        st.subheader("Upload Resume")
        return st.file_uploader("Upload your Resume here" , type=["pdf"])
    
    def upload_jd(self):
        st.subheader("Upload Job Description")
        return st.file_uploader("Upload your Job Description here" , type=["pdf"])
    
    def show_results(self, result:dict):
        st.divider()
        st.subheader("Anlayis Results")

        st.write(f'### Score: {result["overall_score"]}/100')  

        if result["selected"]:
            st.success("Candidate is shortlisted")
        else:
            st.error("Candidate rejected..")

        st.subheader("Strengths")
        if result["strengths"]:
            for s in result["strengths"]:
                st.write(f"- {s} ({result['skill_scores'][s]}/10)")
        else:
            st.write("No strong skills in the resume")

        st.subheader("Areas of Improvements")
        if result["missing_skills"]:
            for s in result["missing_skills"]:
                st.write(f"- {s} ({result['skill_scores'][s]}/10)")
        else:
            st.write("No major skill gaps found")

        



    