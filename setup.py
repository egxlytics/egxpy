from setuptools import setup

setup(
    name="egxpy",
    version="1.1.0",
    packages=["egxpy"],
    url="https://github.com/egxlytics/egxpy/",
    project_urls={
        "Web App": "https://egxpy-lab.streamlit.app/",
        "Source": "https://github.com/egxlytics/egxpy/",
    },
    license="MIT License",
    author="@egxlytics",
    author_email="egxlytics@gmail.com",
    description="Historical Data EGX",
    long_description_content_type="text/markdown",
    install_requires=[
        "setuptools",
        "pandas",
        "numpy",
        "holidays",
        "retry",
        "tvDatafeed @ git+https://github.com/rongardF/tvdatafeed.git@main"
    ]
)
