from setuptools import setup, find_packages

setup(
    name='BioModelsRAG',  
    version='0.3.1',            
    packages=find_packages(), 
    install_requires=[
        'requests',                
        'tellurium',               
        'ollama',                  
        'langchain_text_splitters',
        'chromadb',                
    ],
    entry_points={
        'console_scripts': [
            'biomodels-cli = searchBioModels:main',  
        ],
    },
    author='Bhavyahshree Navaneetha Krishnan', 
    author_email='your_email@example.com',     
    description='A package for processing and querying biomodels', 
    url='https://github.com/your_username/your_repo', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)
