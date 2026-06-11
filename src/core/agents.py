import json
from typing import List,Dict
from concurrent.futures import ThreadPoolExecutor

from pypdf import PdfReader
from langchain_openai import ChatOpenAI

from src.common.logger import get_logger
from src.common.custom_exception import CustomException

class ResumeAnalysisAgent:
    def __init__(self,cutoff_score:int = 75):
        self.logger= get_logger(__name__)
        self.cutoff_score = cutoff_score
        self.resume_text=""
        self.jd_text=""

        self.extracted_skills:List[str] = []

        self.logger.info("Resume Anlaysis Agents has been intilaized..")

    def _read_pdf(self,file) -> str:
        try:
            self.logger.info("Reading text from a PDF file")
            reader = PdfReader(file)

            text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            )

            self.logger.info("PDf read success")

            return text
        
        except Exception as e:
            self.logger.error("Failed to read PDf file" , exc_info=True)
            raise CustomException("Failed to read PDF file" , e)
        
    def _read_txt(self,file) -> str:
        try:
            self.logger.info("Reading a TXT file")

            text = (
                file.getvalue().decode("utf-8")
                if hasattr(file,"getvalue")
                else file.read().decode("utf-8")
            )

            self.logger.info("TXT file read sucesfully")
            return text
        
        except Exception as e:
            self.logger.error("Failed to read TXT file" , exc_info=True)
            raise CustomException("Failed to read TXT file" , e)
        

    def extract_text(self,file) -> str:
        try:
            self.logger.info("Extracting Content from a PDF/TXT file")
            
            ext = file.name.split(".")[-1].lower()

            if ext=="pdf":
                return self._read_pdf(file)
            if ext=="txt":
                return self._read_txt(file)
            else:
                self.logger.warning("Unsupported file type")
                return ""
        except Exception as e:
            self.logger.error("Extraction failed" , exc_info=True)
            raise CustomException("Extraction failed" , e)
        

    def extract_skills_from_jd(self,jd_text:str) -> List[str]:
        try:
            self.logger.info("Extracting skills from JD")

            llm = ChatOpenAI(model="gpt-4.1-mini" , temperature=0)

            prompt = """
                Extract only technical skills from the given job description.
                
                Rules:
                1. Return only in valid JSON format
                2. No markdown
                3. No explanation

                Example:
                ["Python","Docker","AWS"]
                """
            response=llm.invoke(prompt+"\n\n"+jd_text)

            skills = json.loads(response.content)

            if isinstance(skills,list):
                self.logger.info(f"Extracted skills from JD {skills}")
                return skills
            
            else:
                self.logger.warning("Skill extraction failed due to non compaitable types")
                return []
            
        except Exception as e:
            self.logger.error("Extraction from JD failed" , exc_info=True)
            raise CustomException("Extraction from JD failed" , e)
        
    def _evaluate_skill(self,skill:str) -> Dict:
        try:
            self.logger.info(f"Evaluating skill {skill}")

            llm = ChatOpenAI(model="gpt-4.1-mini" , temperature=0)

            prompt=f"""
                Evaluate how clearly the resume shows proficiency in "{skill}".

                Resume:
                {self.resume_text[:2500]}

                Return ONLY with valid JSON
                {{ "skill":"{skill}","score":0-10 }}

            """

            response = llm.invoke(prompt)

            result = json.loads(response.content)

            return result
        
        except Exception as e:
            self.logger.error("Evaluation of skills failed" , exc_info=True)
            return {"skill": skill, "score": 0}
        
    
    def evaluate_skils(self) -> Dict:
        try:
            self.logger.info("Evluation of all skills started")

            with ThreadPoolExecutor(max_workers=3) as executor:
                results = list(
                    executor.map(self._evaluate_skill,self.extracted_skills)
                )

            scores = {r["skill"] : r["score"] for r in results}

            strengths = [k for k , v in scores.items() if v>=7]

            missing = [k for k , v in scores.items() if v<=5]

            total_score = (
                int((sum(scores.values()) / (10*len(scores)))*100)
                if scores
                else 0
            )

            self.logger.info("evaluation of skills completed")

            return {
                "overall_score" : total_score,
                "selected" : total_score>=self.cutoff_score,
                "skill_scores" : scores,
                "strengths" : strengths,
                "missing_skills":missing
            }
        
        except Exception as e:
            self.logger.error("Evaluation of all skills failed" , exc_info=True)
            raise CustomException("Evaluation of all skills failed" , e)
        
    
    def analyze(self,resume_file,jd_file) -> Dict:
        try:
            self.resume_text = self.extract_text(resume_file)
            self.jd_text = self.extract_text(jd_file)


            self.extracted_skills = self.extract_skills_from_jd(self.jd_text)

            result= self.evaluate_skils()

            return result
        
        except Exception as e:
            self.logger.error("Anlaysis failed" , exc_info=True)
            raise CustomException("Anlaysis failed" , e)
        






        
        
    

        












