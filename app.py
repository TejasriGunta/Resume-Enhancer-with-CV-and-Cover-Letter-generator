import streamlit as st
from docx import Document
from crewai import resume_enhancer_crew


st.title("🚀 AI Resume Enhancer with CV and Cover letter generator")
st.markdown("Enhance your resume and generate personalized cover letters using AI.")

uploaded_resume = st.file_uploader("📄 Upload Resume (Text or Docx)", type=["txt", "docx"])
job_description = st.text_area("📝 Enter your Job Description")

@st.cache_data
def read_resume(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return None


if st.button("🚀 Enhance Resume & Generate Cover Letter"):
    if uploaded_resume and job_description:
        resume_text = read_resume(uploaded_resume)
        st.info("⏳ Processing... Please wait.")

        # Kickoff the Crew
        result = resume_enhancer_crew.kickoff(inputs={
            "resume": resume_text,
            "job_description": job_description
        })

        result_str = str(result)
        
        st.header("AI Resume Enhancement Results")
        st.subheader("Analysis")
        tasks_output=result.tasks_output
        st.write(tasks_output[0].raw)   

        st.subheader("CV")
        st.write(tasks_output[1].raw) 

        st.subheader("Cover Letter")
        st.write(result.raw)
        
    else:
        st.warning("⚠️ Please upload a resume and provide a job description.")
