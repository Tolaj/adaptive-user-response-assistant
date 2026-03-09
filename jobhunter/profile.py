# jobhunter/profile.py
# ─────────────────────────────────────────────────────────────────────────────
# EDIT THIS FILE with your real details before running the job hunter.
# The VLM uses this profile to score and filter jobs intelligently.
# ─────────────────────────────────────────────────────────────────────────────

PROFILE = {
    # ── Who you are ───────────────────────────────────────────────────────────
    "name": "Swapnil",
    "job_titles": [
        "Junior Software Developer",
        "Junior Python Developer",
        "Junior Backend Developer",
        "Junior Full Stack Developer",
    ],

    # ── Skills (VLM will check job descriptions for these) ───────────────────
    "skills": [
        "Python",
        "JavaScript",
        "React",
        "Node.js",
        "REST APIs",
        "SQL",
        "Git",
        "Docker",  # remove if you don't know this
    ],

    # ── Experience ────────────────────────────────────────────────────────────
    "years_experience": 1,   # 0–2 for junior
    "education": "Bachelor's in Computer Science",  # or your actual degree

    # ── Location preferences ──────────────────────────────────────────────────
    "location": "India",           # your country/city
    "remote_preference": "remote", # "remote", "hybrid", "onsite", or "any"
    "open_to_relocation": False,

    # ── Salary filter ─────────────────────────────────────────────────────────
    # Set to None to disable salary filtering
    "min_salary_lpa": None,        # e.g. 4 means ₹4 LPA minimum (for India)
    "currency": "INR",             # "INR", "USD", "EUR" etc.

    # ── Keywords to AVOID ─────────────────────────────────────────────────────
    # Jobs containing any of these will be skipped
    "avoid_keywords": [
        "senior",
        "lead",
        "10+ years",
        "5+ years",
        "unpaid",
        "internship",   # remove this if you want internships
        "blockchain",
        "web3",
    ],

    # ── Keywords you WANT ─────────────────────────────────────────────────────
    # Jobs with these get a score boost
    "prefer_keywords": [
        "python",
        "backend",
        "api",
        "startup",
        "product",
    ],
}

# ── Search queries per site ────────────────────────────────────────────────────
# These are what get typed into each job site's search box
SEARCH_QUERIES = {
    "linkedin": [
        "junior python developer remote",
        "junior backend developer india",
        "junior software developer remote india",
    ],
    "indeed": [
        "junior python developer",
        "junior software developer remote",
        "entry level backend developer",
    ],
    "naukri": [
        "junior python developer",
        "junior software developer",
        "entry level developer",
    ],
    "wellfound": [
        "junior engineer python",
        "software engineer junior remote",
    ],
}

# ── Site credentials (needed for LinkedIn login) ──────────────────────────────
CREDENTIALS = {
    "linkedin": {
        "email": "your_email@gmail.com",     # ← EDIT THIS
        "password": "your_password_here",     # ← EDIT THIS
    },
    # Indeed, Naukri, Wellfound work without login for basic search
}