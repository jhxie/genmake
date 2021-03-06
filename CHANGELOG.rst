Change Log
==========

| This document records all notable changes to Skaff.
| This project adheres to `Semantic Versioning <http://semver.org/>`__
  starting from version 1.0.

1.0 (Upcoming)
--------------

-  Add **ini-parsing** functionality for saving/restoring configurations
-  Add custom python module based **hook** support for different
   **file-creation** events
-  Add sample header file (under *include* subdirectory) generation
   functionality
-  Add support for **user-defined** programming languages,
   subdirectories,
   licenses, and templates.
-  Allow specifying *more than one* author(s) for any project
-  Finalize a stable API for *driver* module based on *SkaffConfig*
   class
-  Set up a dedicated website hosted by *GitHubPages* based on existing
   template

0.9 (2016-06-05)
----------------

-  Add **GDB** initialization file *.gdbinit* generation functionality
-  Add full unit test cases for the prototype of *SkaffConfig* class
-  Add sample source file (under *src* subdirectory) generation
   functionality
-  Add tentative developer's documentation on `ReadThe
   Docs <http://skaff.readthedocs.io/en/latest/>`__
-  Optimize performance of regular expression matching for *Doxyfile*
   generation
-  Rename the project to **skaff**

0.8 (2016-05-24)
----------------

-  Add *CHANGELOG.md* template generation
-  Add *Travis-CI* configuration file *.travis.yml* generation
-  Change language option for C++ to be **cpp** instead of **cxx**
-  Implement the prototype of *GenMakeConfig* class to be used for
   external API

0.7 (2016-05-10)
----------------

-  Add dynamic *Doxyfile* generation by invoking *doxygen* executable
-  Add interactive prompt for configuration file editing
-  Add *Travis-CI* integration
-  Extend interactive *Doxyfile* editing to work on *CMakeLists.txt* as
   well

0.6 (2016-05-04)
----------------

-  Add gzipped format for the command-line reference manual

0.5 (2016-05-03)
----------------

-  Add tentative command-line reference manual generated by *help2man*
   program

0.4 (2016-04-30)
----------------

-  Add fully automated unittest module driven by *setuptools*
-  Add installation instructions in *README.rst*
-  Re-design the main logo and banner

0.3 (2016-04-26)
----------------

-  Add editor lookup functionality based on environment variable
   **EDITOR**
-  Fix "*unable to locate configuration file*" bug

0.2 (2016-04-24)
----------------

-  Add static *Doxyfile* generation functionality based on existing
   template
-  Add *Doxyfile* editing by invoking *vi* or *vim* editor

0.1 (2016-04-23)
----------------

-  Add basic *README.md* file generation
-  Add static configuration file generation for *git* and *editorconfig*
-  Add static *CMakeLists.txt* file generation
