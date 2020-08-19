from lyncs_setuptools import setup

setup(
    "lyncs_cppyy",
    install_requires=["cppyy", "numpy"],
    keywords=["Lyncs", "cppyy",],
    extras_require={"test": ["pytest", "pytest-cov", "meson", "ninja",]},
)
