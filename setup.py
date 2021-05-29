from distutils.core import setup
setup(
    name='automaton-linux',
    packages=["automaton"],
    version='0.5',
    license='MIT',
    description='An automation library for Linux using Uinput.',
    author='Abdul Muiz Iqbal',
    author_email='parkermuiz0@gmail.com',
    url='https://github.com/Abdul-Muiz-Iqbal/Automaton/',
    download_url='https://github.com/Abdul-Muiz-Iqbal/Automaton/archive/refs/tags/0.5.tar.gz',
    keywords=['automation', 'linux', 'uinput'],
    install_requires=[
        'evdev',
        'pgi',
        'zenipy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
