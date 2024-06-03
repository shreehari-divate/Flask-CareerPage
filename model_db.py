from app import JobDesc, db, JobPos, app
from flask_migrate import Migrate

with app.app_context():
    # Create the database and the database table
    db.create_all()
    migrate = Migrate(app, db)  # Migrate is used only on schema level updation

    # Check if job1 and job2 already exist
    job1 = JobPos.query.filter_by(title='AI Engineer', location='Bengaluru, Karnataka').first()
    job2 = JobPos.query.filter_by(title='Data Scientist', location='Bengaluru, Karnataka').first()

    # Insert initial job positions if they do not exist
    if not job1:
        job1 = JobPos(title='AI Engineer', exp=3, sal='12 LPA', location='Bengaluru, Karnataka')
        db.session.add(job1)
    if not job2:
        job2 = JobPos(title='Data Scientist', exp=2, sal='10 LPA', location='Bengaluru, Karnataka')
        db.session.add(job2)
    
    db.session.commit()

    # Check if desc1 already exists
    desc1 = JobDesc.query.filter_by(job_id=job1.id).first() if job1 else None

    # Insert initial job descriptions if they do not exist
    if not desc1 and job1:
        desc1 = JobDesc(
            job_id=job1.id,
            desc='We are seeking an experienced AI Engineer to join our innovative team. The ideal candidate will have a robust understanding of Artificial Intelligence and Machine Learning techniques, and a passion for building AI models that drive business results.',
            resp=', '.join([
                'Design, develop, and deploy AI models tailored to our business needs.',
                'Collaborate with data scientists to transform data science prototypes into high-quality software products.',
                'Conduct research to advance the state of the art and solve specific business problems.',
                'Optimize existing AI models for performance and scalability.',
                'Maintain up-to-date knowledge of AI trends and developments.'
            ]),
            qualif=', '.join([
                'Bachelor\'s degree in Computer Science, Engineering, or a related field.',
                '3 years of experience working as an AI Engineer or similar role.',
                'Proficiency in Python and familiarity with machine learning frameworks.',
                'Strong problem-solving skills and ability to work in a team environment.'
            ]),
            pref_skills=', '.join([
                'Proficiency in Python Programming Language',
                'Expertise in Machine Learning/Deep Learning/Computer Vision',
                'Proficient in ML frameworks like TensorFlow/PyTorch',
                'Experience with version control systems and containerization',
                'Experience with AWS/GCP/Azure',
                'Experience with Natural Language Processing (NLP).'
            ])
        )
        db.session.add(desc1)

    # Check if desc2 already exists
    desc2 = JobDesc.query.filter_by(job_id=job2.id).first() if job2 else None

    if not desc2 and job2:
        desc2 = JobDesc(
            job_id=job2.id,
            desc='We are seeking a highly motivated and skilled Data Scientist to join our dynamic team. The ideal candidate will have 2 years of experience in data science and a strong background in data analysis, statistical modeling, and machine learning. This role requires a detail-oriented individual who can transform data into actionable insights to support our business goals.',
            resp=', '.join([
                'Analyze large and complex datasets to uncover trends,patterns, and insights.',
                'Develop and implement data models algorithms and statistical analyses to solve business problems.',
                'Design and maintain databases and data systems to ensure data integrity and accessibility.',
                'Perform data cleaning preprocessing and feature engineering to prepare data for analysis.',
                'Stay updated with the latest industry trends tools and technologies in data science and machine learning.'
            ]),
            qualif=', '.join([
                'Bachelor\'s degree in Data Science/Computer Science/Statistics/Mathematics or a related field.',
                'Proven experience of 2 years in data science/analytics or a related role.',
                'Proficiency in programming languages such as Python or R.',
                'Strong knowledge of statistical analysis data mining and machine learning techniques.',
                'Experience with data visualization tools like Tableau/PowerBI/Matplotlib.',
                'Familiarity with databases and query languages such as SQL.',
                'Excellent problem-solving skills and attention to detail.',
                'Strong communication and collaboration skills.'
            ]),
            pref_skills=', '.join([
                'Experience with big data technologies like Hadoop or Spark.',
                'Familiarity with cloud platforms such as AWS/Azure/GCP.',
                'Knowledge of deep learning frameworks such as TensorFlow or PyTorch.',
                'Understanding of A/B testing and experimental design.',
                'Experience with data pipeline and ETL processes.'
            ])
        )
        db.session.add(desc2)

    db.session.commit()
