import os
import streamlit as st
from src.core.agents import ResumeAnalysisAgent
from src.ui.ui import JobAnalyzerUI

st.set_page_config(
    page_title="Job anlayzer",
    layout="wide"
)


class JobAnlayzerApp:
    def __init__(self):
        self.ui = JobAnalyzerUI()
        self.agent = ResumeAnalysisAgent()

    def run(self):
        self.ui.header()

        api_key = self.ui.sidebar()
        if not api_key:
            st.warning("Please enter the OpenAI API key first")
            st.stop()

        os.environ["OPENAI_API_KEY"] = api_key

        resume = self.ui.upload_resume()
        jd = self.ui.upload_jd()


        if st.button("Analyze Resume and JD"):
            if not resume or not jd:
                st.error("Please upload both Resume and JD")

            with st.spinner("Analyzing Resume...."):
                result=self.agent.analyze(resume,jd)
                self.ui.show_results(result)


if __name__=="__main__":
    JobAnlayzerApp().run()
