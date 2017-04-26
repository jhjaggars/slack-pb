from setuptools import setup, find_packages

entry_points = {
    'console_scripts': ['pb = slackpb:main']
}

if __name__ == "__main__":

    setup(
        name="slack-pb",
        version="0.1",
        description="Slack Paster (file uploader)",
        packages=find_packages(),
        install_requires=["setuptools", "requests"],
        entry_points=entry_points,
    )
