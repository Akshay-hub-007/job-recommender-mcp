from mcp.server import FastMCP
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs
from src.helper import ask_gemini

mcp = FastMCP("AI Job Recommender - Your Career Intelligence Assistant")

# ==================== TOOLS ====================

@mcp.tool()
async def fetch_linkedin_jobs(keywords: str, location: str = "india", max_results: int = 60):
    """
    Fetch job listings from LinkedIn based on search keywords and location.
    
    Args:
        keywords: Job search keywords (e.g., "Python Developer, Software Engineer")
        location: Job location (default: "india")
        max_results: Maximum number of jobs to return (default: 60)
    
    Returns:
        List of job listings with title, company, location, and link
    """
    return fetch_linkedin_jobs(keywords, location, max_results)


@mcp.tool()
async def fetch_naukri_jobs(keywords: str, location: str = "india", max_results: int = 60):
    """
    Fetch job listings from Naukri.com based on search keywords.
    
    Args:
        keywords: Job search keywords (e.g., "Python Developer, Data Scientist")
        location: Job location (default: "india")
        max_results: Maximum number of jobs to return (default: 60)
    
    Returns:
        List of job listings with title, company, location, and URL
    """
    return fetch_naukri_jobs(keywords, location, max_results)


@mcp.tool()
async def analyze_resume_summary(resume_text: str):
    """
    Generate a comprehensive resume summary highlighting skills, experience, and education.
    
    Args:
        resume_text: Full text content of the resume
    
    Returns:
        AI-generated professional summary
    """
    prompt = f"""Analyze this resume and provide a comprehensive summary highlighting:
    - Key skills and technical expertise
    - Educational background
    - Professional experience and achievements
    - Notable projects or certifications
    
    Resume:
    {resume_text}
    
    Provide a well-structured, professional summary."""
    
    return ask_gemini(prompt, max_tokens=600)


@mcp.tool()
async def identify_skill_gaps(resume_text: str):
    """
    Analyze resume to identify missing skills, certifications, and areas for improvement.
    
    Args:
        resume_text: Full text content of the resume
    
    Returns:
        Detailed skill gap analysis with recommendations
    """
    prompt = f"""Based on this resume, conduct a thorough skill gap analysis:
    - Identify in-demand skills that are missing
    - Suggest relevant certifications that would enhance the profile
    - Highlight areas where experience could be strengthened
    - Recommend tools or technologies to learn
    
    Resume:
    {resume_text}
    
    Provide actionable insights organized by priority."""
    
    return ask_gemini(prompt, max_tokens=600)


@mcp.tool()
async def create_career_roadmap(resume_text: str):
    """
    Generate a personalized career development roadmap based on current skills and experience.
    
    Args:
        resume_text: Full text content of the resume
    
    Returns:
        12-month career roadmap with actionable steps
    """
    prompt = f"""Create a personalized 12-month career development roadmap based on this resume:
    - Month 1-3: Immediate actions and quick wins
    - Month 4-6: Skill development and certifications
    - Month 7-9: Project-based learning and portfolio building
    - Month 10-12: Career advancement strategies
    
    Resume:
    {resume_text}
    
    Make it specific, actionable, and realistic."""
    
    return ask_gemini(prompt, max_tokens=700)


@mcp.tool()
async def generate_job_keywords(resume_summary: str):
    """
    Extract optimal job search keywords from a resume summary.
    
    Args:
        resume_summary: Professional summary of the resume
    
    Returns:
        Comma-separated list of job titles and keywords
    """
    prompt = f"""Based on this professional summary, extract the most relevant job titles and keywords for job searching.
    
    Summary: {resume_summary}
    
    Instructions:
    - Focus on job titles, roles, and technical skills
    - Include both specific and general terms
    - Prioritize terms that appear in job postings
    - Return ONLY a comma-separated list
    
    Example: "Senior Software Engineer, Python Developer, Backend Engineer, Full Stack Developer"
    """
    
    return ask_gemini(prompt, max_tokens=150)


# ==================== PROMPTS ====================

@mcp.prompt()
async def analyze_candidate_profile():
    """
    Complete AI-powered career analysis workflow for job seekers.
    
    This prompt guides you through analyzing a candidate's resume, identifying strengths,
    weaknesses, and recommending suitable job opportunities.
    """
    return [
        {
            "role": "system",
            "content": """You are an expert career counselor and recruiter with deep knowledge of:
            - Technical and non-technical skill assessment
            - Industry hiring trends across multiple sectors
            - Career development strategies
            - Resume optimization techniques
            
            Your goal is to provide comprehensive, actionable career guidance."""
        },
        {
            "role": "user",
            "content": """Please help me with a complete career analysis:
            
            1. First, I'll provide my resume text
            2. Analyze my skills, experience, and education
            3. Identify my strengths and competitive advantages
            4. Highlight skill gaps and areas for improvement
            5. Create a 12-month career development roadmap
            6. Generate optimal job search keywords
            7. Find relevant job opportunities on LinkedIn and Naukri
            
            Let's start with step 1 - I'll paste my resume."""
        }
    ]


@mcp.prompt()
async def resume_optimization():
    """
    Get expert advice on improving your resume for better job prospects.
    
    Provides specific recommendations on content, formatting, keywords, and presentation.
    """
    return [
        {
            "role": "system",
            "content": """You are a professional resume writer and ATS (Applicant Tracking System) expert.
            You help candidates optimize their resumes to:
            - Pass ATS screening
            - Highlight achievements effectively
            - Use powerful action verbs
            - Quantify accomplishments
            - Match job descriptions"""
        },
        {
            "role": "user",
            "content": """I need help optimizing my resume. Please review it and provide:
            
            1. **Content Improvements**: What should I add, remove, or rewrite?
            2. **ATS Optimization**: Keywords and formatting for better screening
            3. **Achievement Focus**: How to better quantify my accomplishments
            4. **Impact Statements**: Stronger ways to present my experience
            5. **Industry Alignment**: Tailoring for my target role/industry
            
            Here's my current resume:"""
        }
    ]


@mcp.prompt()
async def skill_gap_analysis():
    """
    Detailed analysis of skills needed vs skills possessed for target roles.
    
    Identifies specific skills, certifications, and experiences to acquire.
    """
    return [
        {
            "role": "system",
            "content": """You are a technical skills assessor and career development specialist.
            You analyze professional profiles against industry requirements and provide:
            - Gap analysis between current and desired skills
            - Prioritized learning roadmaps
            - Certification recommendations
            - Project ideas for practical experience"""
        },
        {
            "role": "user",
            "content": """I want to understand my skill gaps for my target roles. Please analyze:
            
            1. My current skills and experience level
            2. Skills required for my target job roles
            3. Critical gaps that need immediate attention
            4. Nice-to-have skills for competitive advantage
            5. Recommended certifications and courses
            6. Projects to build practical experience
            7. Timeline for skill acquisition (3, 6, 12 months)
            
            My resume/profile:"""
        }
    ]


@mcp.prompt()
async def career_transition_guide():
    """
    Strategic guidance for professionals looking to transition to a new role or industry.
    
    Provides actionable steps for successful career pivots.
    """
    return [
        {
            "role": "system",
            "content": """You are a career transition coach specializing in helping professionals
            pivot to new roles or industries. You understand:
            - Transferable skills identification
            - Industry requirements and expectations
            - Networking strategies
            - Personal branding
            - Interview preparation for career changers"""
        },
        {
            "role": "user",
            "content": """I'm planning a career transition and need guidance:
            
            **My Current Situation:**
            - Current role/industry: [to be provided]
            - Target role/industry: [to be provided]
            - Years of experience: [to be provided]
            
            **What I Need:**
            1. Assessment of transferable skills
            2. Skills/knowledge I need to acquire
            3. 90-day action plan for transition
            4. Resume repositioning strategy
            5. Networking and personal branding tips
            6. Interview preparation focused on career change narrative
            
            My current background:"""
        }
    ]


@mcp.prompt()
async def interview_preparation():
    """
    Comprehensive interview preparation based on your resume and target roles.
    
    Includes common questions, technical topics, and behavioral scenarios.
    """
    return [
        {
            "role": "system",
            "content": """You are an interview coach and recruiter with experience across industries.
            You help candidates prepare for:
            - Technical interviews
            - Behavioral questions (STAR method)
            - System design discussions
            - Salary negotiations
            - Company-specific interview processes"""
        },
        {
            "role": "user",
            "content": """Help me prepare for interviews based on my background and target roles:
            
            **Preparation Areas:**
            1. Common questions for my role/level
            2. Technical topics to review
            3. Behavioral scenarios (STAR format)
            4. Questions about gaps or transitions in my resume
            5. My unique selling points to highlight
            6. Smart questions to ask interviewers
            7. Salary negotiation talking points
            
            My resume and target role:"""
        }
    ]


@mcp.prompt()
async def job_market_insights():
    """
    Get current job market trends, salary ranges, and demand analysis for specific roles.
    
    Helps make informed career decisions based on market data.
    """
    return [
        {
            "role": "system",
            "content": """You are a labor market analyst with real-time knowledge of:
            - Job market trends and demand
            - Salary ranges by role, location, and experience
            - Growing and declining industries
            - Remote work opportunities
            - Regional variations in hiring"""
        },
        {
            "role": "user",
            "content": """I need job market insights for strategic career planning:
            
            **Information Needed:**
            1. Current demand for my skills/role
            2. Salary ranges (entry/mid/senior level)
            3. Top hiring companies in my domain
            4. Remote vs on-site opportunities
            5. Future outlook (6-12 months)
            6. Geographic hotspots for my role
            7. Emerging opportunities in adjacent fields
            
            My role/skills:"""
        }
    ]


@mcp.prompt()
async def personalized_job_search():
    """
    Customized job search strategy based on your unique profile and preferences.
    
    Provides targeted search terms, platforms, and networking approaches.
    """
    return [
        {
            "role": "system",
            "content": """You are a job search strategist helping candidates find the right opportunities.
            You provide personalized advice on:
            - Optimal search keywords and Boolean queries
            - Best job boards and platforms for specific roles
            - Networking strategies (LinkedIn, events, communities)
            - Application prioritization
            - Follow-up tactics"""
        },
        {
            "role": "user",
            "content": """Create a personalized job search strategy for me:
            
            **My Preferences:**
            - Target roles: [to be specified]
            - Industries: [to be specified]
            - Location preferences: [to be specified]
            - Company size/type: [to be specified]
            - Work arrangement: [remote/hybrid/on-site]
            
            **Strategy Needed:**
            1. Best job search keywords for my profile
            2. Top platforms/boards to focus on
            3. LinkedIn optimization tips
            4. Networking approach (groups, events, connections)
            5. Application strategy (volume vs targeted)
            6. Daily/weekly action plan
            
            My background:"""
        }
    ]


if __name__ == "__main__":
    mcp.run(transport='stdio')