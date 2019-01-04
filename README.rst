========
uGet Cli
========


.. image:: https://img.shields.io/pypi/v/ugetcli.svg
        :target: https://pypi.python.org/pypi/ugetcli

.. image:: https://img.shields.io/travis/AgeOfLearning/uget-cli.svg
        :target: https://travis-ci.org/AgeOfLearning/uget-cli

.. image:: https://readthedocs.org/projects/ugetcli/badge/?version=latest
        :target: https://ugetcli.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




uGet Command Line Interface

Installation
------------

**Disclaimer**: This software is currently alpha. Stability is not guaranteed.

You can install this package using pip:

.. code-block:: bash

    pip install ugetcli



Quickstart
----------

uGet Package Manager for Unity - pack unity plugins into re-usable NuGet packages.
Supports packing assets and correctly handles meta files (GUIDS).

.. code-block:: bash

    cd MySolutionName/MyProjectName
    uget build  // Build Visual Studio project
    uget create // Create Unity Package (.unitypackage)
    uget pack   // Create NuGet Package (.nupkg)
    uget push   // Push to the NuGet feed


uget build
----------

**Builds Visual Studio project using msbuild.**

Arguments:

**-p** / **--path** path to the Visual Studio Project (.csproj) or a directory containing one

**-c** / **--configuration** configuration: *Debug* or *Release*

**-m** / **--msbuild-path** path to the msbuild executable. If not provided, uget cli will try to automatically find it. Can be provided with MSBUILD_PATH environment variable.

**-r** / **--rebuild** (flag) if provided, clean rebuild will be triggered.


uget create
-----------

**Creates .unitypackage using Unity Editor.**

Arguments:

**-p** / **--path** path to the Visual Studio Project (.csproj) or a directory containing one

**-o** / **--output-dir** output directory into which UnityPackage will be built

**-c** / **--configuration** configuration: *Debug* or *Release*

**-u** / **--unity-path** path to Unity Editor.  Can be provided with UNITY_PATH environment variable.

**-t** / **--unity-project-path** path to the Unity project used to build .unitypackage. Project can contain optional assets.

**-r** / **--root-dir** root directory inside the Unity Project into which assembly is copied. Used to export .unitypackage. If not provided, project name is used.

**--clean** (flag) If set, cleans other .unitypackage files with the same configuration at the output location.

**--unity-username** provides username for Unity editor. Can be provided with UNITY_USERNAME environment variable.

**--unity-password** provides password for Unity editor. Can be provided with UNITY_PASSWORD environment variable.

**--unity-serial** provides serial for Unity editor. Can be provided with UNITY_SERIAL environment variable.



uget pack
---------

**Packs NuGet package (.nupkg) using NuGet. Includes Unity Package (.unitypackage) into it.**

Arguments:

**-p** / **--path** path to Visual Studio project (.csproj) or .nuspec file.

**-o** / **--output-dir** output NuGet package directory.

**-n** / **--nuget-path** path to NuGet executable. Can be provided with NUGET_PATH environment variable.

**-u** / **--unitypackage-path** path to .unitypackage.

**-c** / **--configuration** configuration: *Debug* or *Release*



uget push
---------

**Push uGet Package (.nupkg) to the NuGet feed.**

Arguments:

**-p** / **--path** path to NuGet Package (.nupkg) or Visual Studio project.

**-o** / **--output-dir** provides directory in which Nuget Package is being looked for. Used only if path is a .csproj or a directory that contains one (optional).

**-f** / **--feed** NuGet Feed URL.

**-n** / **--nuget-path** path to NuGet executable. Can be provided with NUGET_PATH environment variable.

**-a** / **--api-key** NuGet Api Key.  Can be provided with NUGET_API_KEY environment variable.


Configuration file
------------------

**--config-path**
As an alternative to command line arguments, configuration file can be provided.
By default, **uget.config.json** will be used. Config file will be searched in the execution directory.
You can provide custom config file by passing it's path to the **--config**.

Example config file (uget.config.json):

.. code-block:: json

    {
        "output_dir": "../../Output",
        "unity_project_path": "../../UnityProjects/MyUnityProject",
        "clean": true,
        "configuration": "Debug",
        "root_dir": "Assets/MyUnityProject", // optional
        "assembly_relative_dir": "Editor", // optional
        "feed": "https://proget.aofl.com/nuget/AOFL-Unity-Development/"
    }

You can override any command line parameter by using *snake_case* instead of *dashed-options*


Configuration json
------------------
**--config**
You can pass configuration as a raw json instead of configuration file by passing **--config**:

.. code-block:: bash

    uget build --config "{\"output_dir\": \"Output\"}"


Debug Mode
------------------
**-d** / **--debug**
This flag can be provided to output more debug information and enable verbose logs from underlying tools.


Quiet Mode
------------------
**-q** / **--quiet**
This flag can be provided to silence any user prompts.
