from setuptools import setup, find_packages

setup(
    name='BioModelsRAG',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'BioModelsRAG': ['data/*']
    },
    install_requires=[
        'ollama', 
        'langchain', 
        'chromadb', 
        'sentence_transformers', 
        'langchain_text_splitters',
    ],
    entry_points={
        'console_scripts': [
            'start = splitBiomodels:final_items'
        ],
    },
    author='Bhavyahshree Navaneetha Krishnan',
    author_email='bhavyak7@uw.edu',
    description='BioModelsRAG is a tool to analyze the wide repository of BioModels that are available on the internet and ask specific questions about the BioModels. It is created to be an assistant to system biology researchers.',
    long_description_content_type='text/markdown',
    url='https://github.com/TheBobBob/BioModelsRAG',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

