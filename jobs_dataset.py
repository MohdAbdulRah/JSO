"""
jobs_dataset.py – Simulated Job Dataset for JSO Career Intelligence System
Contains diverse job listings across AI, Data Science, Software Engineering,
Cloud, and Cybersecurity domains.
"""


def get_jobs() -> list[dict]:
    """Return a list of simulated job postings."""
    return [
        {
            "id": "JOB001",
            "title": "Machine Learning Engineer",
            "company": "DeepMind Technologies",
            "required_skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "MLOps"],
            "description": (
                "Design and deploy production-grade machine learning models. "
                "Work with large-scale datasets, build training pipelines, and "
                "optimise model performance for real-time inference."
            ),
            "experience_level": "Mid-Level",
            "industry": "Artificial Intelligence",
        },
        {
            "id": "JOB002",
            "title": "Data Scientist",
            "company": "Spotify Analytics",
            "required_skills": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
            "description": (
                "Analyse complex datasets to drive product decisions. Build "
                "predictive models, design A/B tests, and communicate insights "
                "to cross-functional stakeholders."
            ),
            "experience_level": "Mid-Level",
            "industry": "Technology / Media",
        },
        {
            "id": "JOB003",
            "title": "AI Research Scientist",
            "company": "OpenAI Labs",
            "required_skills": ["Python", "PyTorch", "NLP", "Computer Vision", "Research", "Mathematics"],
            "description": (
                "Conduct cutting-edge research in large language models and "
                "multimodal AI. Publish papers, prototype novel architectures, "
                "and push the boundaries of artificial intelligence."
            ),
            "experience_level": "Senior",
            "industry": "Artificial Intelligence",
        },
        {
            "id": "JOB004",
            "title": "Full-Stack Developer",
            "company": "Stripe Engineering",
            "required_skills": ["JavaScript", "React", "Node.js", "Python", "PostgreSQL", "REST APIs"],
            "description": (
                "Build and maintain scalable web applications powering global "
                "payment infrastructure. Collaborate with design and product "
                "teams to ship features end-to-end."
            ),
            "experience_level": "Mid-Level",
            "industry": "FinTech",
        },
        {
            "id": "JOB005",
            "title": "Cloud Solutions Architect",
            "company": "Amazon Web Services",
            "required_skills": ["AWS", "Azure", "Kubernetes", "Docker", "Terraform", "Networking"],
            "description": (
                "Design highly available, cost-effective cloud architectures. "
                "Guide enterprise customers through cloud migration, security "
                "best practices, and infrastructure optimisation."
            ),
            "experience_level": "Senior",
            "industry": "Cloud Computing",
        },
        {
            "id": "JOB006",
            "title": "NLP Engineer",
            "company": "Grammarly AI",
            "required_skills": ["Python", "NLP", "Transformers", "SpaCy", "Deep Learning", "Hugging Face"],
            "description": (
                "Build natural language understanding systems that power "
                "writing assistance tools used by millions. Fine-tune LLMs "
                "and deploy low-latency NLP pipelines."
            ),
            "experience_level": "Mid-Level",
            "industry": "Artificial Intelligence",
        },
        {
            "id": "JOB007",
            "title": "DevOps Engineer",
            "company": "Netflix Platform",
            "required_skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "Python", "Monitoring"],
            "description": (
                "Automate infrastructure provisioning and deployment pipelines. "
                "Ensure 99.99% uptime for services serving 200M+ users through "
                "robust monitoring and incident response."
            ),
            "experience_level": "Mid-Level",
            "industry": "Technology / Media",
        },
        {
            "id": "JOB008",
            "title": "Cybersecurity Analyst",
            "company": "CrowdStrike Security",
            "required_skills": ["Network Security", "SIEM", "Python", "Threat Analysis", "Penetration Testing", "Compliance"],
            "description": (
                "Monitor and defend enterprise networks against advanced threats. "
                "Conduct vulnerability assessments, manage SIEM platforms, and "
                "lead incident response operations."
            ),
            "experience_level": "Mid-Level",
            "industry": "Cybersecurity",
        },
        {
            "id": "JOB009",
            "title": "Data Engineer",
            "company": "Snowflake Data",
            "required_skills": ["Python", "SQL", "Apache Spark", "Airflow", "ETL", "Data Warehousing"],
            "description": (
                "Design and maintain robust data pipelines processing petabytes "
                "of data daily. Build ETL workflows, optimise query performance, "
                "and ensure data quality at scale."
            ),
            "experience_level": "Mid-Level",
            "industry": "Data Infrastructure",
        },
        {
            "id": "JOB010",
            "title": "Computer Vision Engineer",
            "company": "Tesla Autopilot",
            "required_skills": ["Python", "OpenCV", "PyTorch", "Computer Vision", "Deep Learning", "C++"],
            "description": (
                "Develop real-time computer vision algorithms for autonomous "
                "driving. Work on object detection, segmentation, and 3D "
                "reconstruction from multi-camera systems."
            ),
            "experience_level": "Senior",
            "industry": "Automotive / AI",
        },
        {
            "id": "JOB011",
            "title": "Backend Software Engineer",
            "company": "Google Cloud",
            "required_skills": ["Java", "Python", "Go", "Microservices", "gRPC", "Distributed Systems"],
            "description": (
                "Build highly scalable backend services for Google Cloud Platform. "
                "Design APIs, implement fault-tolerant distributed systems, and "
                "optimise for low-latency high-throughput processing."
            ),
            "experience_level": "Mid-Level",
            "industry": "Cloud Computing",
        },
        {
            "id": "JOB012",
            "title": "Product Manager – AI",
            "company": "Microsoft Copilot",
            "required_skills": ["Product Management", "AI/ML Understanding", "Agile", "Data Analysis", "UX Research", "Strategy"],
            "description": (
                "Define product strategy for AI-powered productivity tools. "
                "Collaborate with engineering and design to ship features that "
                "leverage large language models for millions of users."
            ),
            "experience_level": "Senior",
            "industry": "Technology",
        },
        {
            "id": "JOB013",
            "title": "Robotics Software Engineer",
            "company": "Boston Dynamics",
            "required_skills": ["Python", "C++", "ROS", "Computer Vision", "Control Systems", "Linux"],
            "description": (
                "Develop software for advanced robotic systems. Implement motion "
                "planning, perception, and control algorithms for autonomous "
                "mobile robots operating in unstructured environments."
            ),
            "experience_level": "Mid-Level",
            "industry": "Robotics",
        },
        {
            "id": "JOB014",
            "title": "Blockchain Developer",
            "company": "Ethereum Foundation",
            "required_skills": ["Solidity", "JavaScript", "Web3.js", "Smart Contracts", "Cryptography", "Rust"],
            "description": (
                "Build decentralised applications and smart contracts on the "
                "Ethereum network. Contribute to protocol-level improvements "
                "and developer tooling for the Web3 ecosystem."
            ),
            "experience_level": "Mid-Level",
            "industry": "Blockchain / Web3",
        },
        {
            "id": "JOB015",
            "title": "MLOps Engineer",
            "company": "Databricks",
            "required_skills": ["Python", "MLflow", "Docker", "Kubernetes", "CI/CD", "Machine Learning"],
            "description": (
                "Bridge the gap between ML research and production. Build and "
                "maintain ML pipelines, model registries, feature stores, and "
                "automated retraining infrastructure."
            ),
            "experience_level": "Mid-Level",
            "industry": "Data Infrastructure",
        },
        {
            "id": "JOB016",
            "title": "UX Designer – AI Products",
            "company": "Figma Design",
            "required_skills": ["Figma", "User Research", "Prototyping", "Design Systems", "Interaction Design", "AI UX"],
            "description": (
                "Design intuitive user experiences for AI-powered design tools. "
                "Conduct user research, create prototypes, and define design "
                "system patterns that scale across products."
            ),
            "experience_level": "Mid-Level",
            "industry": "Design / Technology",
        },
        {
            "id": "JOB017",
            "title": "Quantitative Analyst",
            "company": "Jane Street Capital",
            "required_skills": ["Python", "Mathematics", "Statistics", "Machine Learning", "Financial Modelling", "OCaml"],
            "description": (
                "Develop quantitative trading strategies using statistical models "
                "and machine learning. Analyse market data, build pricing models, "
                "and optimise execution algorithms."
            ),
            "experience_level": "Senior",
            "industry": "Finance",
        },
        {
            "id": "JOB018",
            "title": "Site Reliability Engineer",
            "company": "Cloudflare",
            "required_skills": ["Linux", "Python", "Go", "Monitoring", "Incident Management", "Networking"],
            "description": (
                "Ensure the reliability and performance of a global edge network. "
                "Build automation, improve observability, and respond to incidents "
                "affecting millions of websites."
            ),
            "experience_level": "Mid-Level",
            "industry": "Cloud / Networking",
        },
        {
            "id": "JOB019",
            "title": "Junior Data Analyst",
            "company": "Accenture Analytics",
            "required_skills": ["Python", "SQL", "Excel", "Data Visualization", "Tableau", "Statistics"],
            "description": (
                "Support data-driven decision making for enterprise clients. "
                "Clean and analyse datasets, build dashboards, and present "
                "actionable insights to business stakeholders."
            ),
            "experience_level": "Junior",
            "industry": "Consulting",
        },
        {
            "id": "JOB020",
            "title": "AI Engineer – Generative AI",
            "company": "Anthropic",
            "required_skills": ["Python", "PyTorch", "Transformers", "LLM Fine-tuning", "RAG", "Prompt Engineering"],
            "description": (
                "Build and deploy generative AI systems using large language "
                "models. Implement RAG architectures, fine-tune models for "
                "domain-specific tasks, and ensure AI safety and alignment."
            ),
            "experience_level": "Mid-Level",
            "industry": "Artificial Intelligence",
        },
    ]
