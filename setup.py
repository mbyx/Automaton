from distutils.core import setup
setup(
    name='Automaton',         # How you named your package folder (MyLib)
    packages=['Automaton'],   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='An automation library for Linux using Uinput.',
    author='Abdul Muiz Iqbal',                   # Type in your name
    author_email='parkermuiz0@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/Abdul-Muiz-Iqbal/Automaton/',
    # I explain this later on
    download_url='https://github.com/Abdul-Muiz-Iqbal/Automaton/archive/refs/tags/0.1.tar.gz',
    # Keywords that define your package best
    keywords=['automation', 'linux', 'uinput'],
    install_requires=[            # I get to this in a second
        'evdev',
        'pgi',
        'zenipy'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.9',
    ],
)
