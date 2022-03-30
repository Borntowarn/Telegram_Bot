import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="Crypto Bot",
    version="1.0",
    author="Chistyakov Daniil, Kozlov Mikhail",
    author_email="kozlovmihail02@mail.ru",
    description="Trading and tracking assistant",
    long_description=read_me_description,
    long_description_content_type="markdown",
    url="https://github.com/Borntowarn/Telegram_Bot",
    packages=['Bot'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)