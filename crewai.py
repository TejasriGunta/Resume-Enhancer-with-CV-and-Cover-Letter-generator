import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()
os.environ['GEMINI_API_KEY'] = os.getenv("GEMINI_API_KEY")

# Set up the Language Model
llm = LLM(
    model=os.getenv("GEMINI_LLM_MODEL"),
    verbose=True,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Define Agents
agents = {
    "Resume Analyzer": Agent(
        name="Resume Analyzer",
        role="Analyzes resumes for strengths, weaknesses, and ATS compatibility.",
        goal="Provide feedback on content quality, grammatical error if present and keyword usage in the input text-{resume}.",
         backstory="An AI-powered HR specialist with expertise in resume evaluation.",
         allow_delegation=False,
        llm=llm
),
    "CV generator": Agent(
        name="CVGeneratorAgent",
        role="Generate customized CVs based on resume text-{resume} and job description-{job_description}.",
        goal="Provide a proffesional CV based on the resume text-{resume}",
        backstory="An AI writing expert for drafting proffesional CV for jobs.",
        allow_delegation=False,
        llm=llm
),
    "Cover Letter Generator": Agent(
        name="Cover Letter Generator",
        role="Generates a personalized cover letter based on job description.",
        goal="A cover letter is a short, professional letter that you send along with your resume when applying for a job. It's a way to introduce yourself to the employer and convince them to interview you. Create a compelling cover letter tailored to the job description and input resume text-{resume},{job_description}.",
        backstory="An AI writing expert for compelling cover letters.",
        allow_delegation=False,
        llm=llm
    )
}
tasks = {
    "Resume Review": Task(
        description="Analyze the following resume text for strengths, weaknesses, and grammar of resume text-{resume}",
        agent=agents["Resume Analyzer"],
        expected_output="Detailed review with actionable feedback.Steps to improve the resume text-{resume}"
    ),
    "CV": Task(
        description="Create a proffessional CV based on the resume text-{resume} and job description-{job_description}.",
        agent=agents["CV generator"],
        expected_output="A professionally formatted CV with sections for personal info, education, experience, skills, and detailed information about the projects(project information text in paragraph for CV) based on the resume text-{resume}.Text type-Proffessional to increase recruitment chances"
    ),
    "Cover Letter": Task(
        description="Generate a personalized cover letter.",
        agent=agents["Cover Letter Generator"],
        expected_output="Well-crafted cover letter(with formal letter format with human text) tailored to the job description-{job_description}.include the following: Header-begin with a header that includes your contact details,then formal greeting with manager's name,Then Introduction-The opening paragraph of the cover letter should aim to introduce who you are and explain why you are interested in the role,After your introduction, focus on your qualifications and skills.Mention about the variety in the projects in one line(keep it short and precise).At the end conclusion. The full letter should be less than 450 words.text should be proffessional to increase chances of recruitment" 
    )
}

# Assemble the Crew
resume_enhancer_crew = Crew(
    agents=list(agents.values()),
    tasks=list(tasks.values())
)

