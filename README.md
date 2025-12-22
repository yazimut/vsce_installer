# *VSCode extensions automatic installer*
This script automatically parse your project directory and install recommended extensions online from marketplace or offline form previously downloaded .vsix files

## Table of contents
<!--
    Markdown doesn't support nested ordered lists
    Using HTML
-->
<ol type="1" start="0">
    <li><a href="#table-of-contents">Table of contents</a></li>
    <li><a href="#contacts-and-support">Contacts and support</a></li>
    <li><a href="#software-requirements">Software requirements</a></li>
    <li><a href="#usage">Usage</a></li>
        <ol type="1">
            <li><a href="#recommendations-searching">Recommendations searching</a></li>
            <li><a href="#online-installation-from-vscode-marketplace">Online installation from VSCode Marketplace</a></li>
            <li><a href="#offline-installation">Offline installation</a></li>
            <li><a href="#vscode-cli-interface">VSCode CLI interface</a></li>
            <li><a href="#silent-mode">Silent mode</a></li>
            <li><a href="#verbose-mode">Verbose mode</a></li>
        </ol>
    <li><a href="#contribution">Contribution</a>
        <ol type="1">
            <li><a href="#software-for-development">Software for development</a></li>
        </ol>
    </li>
</ol>



## Contacts and support
If you have any questions or suggestions, contact the developers:
* Eugene Azimut e-mail: [y.azimut@mail.ru](mailto:y.azimut@mail.ru)
* Eugene Azimut on VK: [vk.ru/yazimut](https://vk.ru/yazimut "https://vk.ru/yazimut")



## Software requirements
* OS:
    * or Ubuntu 24.04 amd64 (x64) (tested)
    * or Any Debian-like (possibly, not tested)
    * or Mirosoft Windows 10 amd64 (x64) (possibly, not tested)
    * or Mirosoft Windows 11 amd64 (x64) (possibly, not tested)
* Python 3.12.3
    * pip 24.0
    * python3.12-venv
    * Modules from [requirements.txt](requirements.txt):
        * colorama 0.4.6



## Usage
### Recommendations searching
Script searching recommended extensions in your project directory (current working directory) in following order:
1. First `*.code-workspace` file<br>
    Often here it is only one such file, but in other case first found will be used. Note that these files is NOT always sorted in alphabetical order (depends on your system)
2. `.vscode/extensions.json`

> [!IMPORTANT]
> These files must be a valid VSCode JSON files without comments!

### Online installation from VSCode Marketplace
By default script will try to install extensions from [VSCode Marketplace](https://marketplace.visualstudio.com)
```bash
    cd MyAwesomeProject
    python3 vscode_extensions.py
```

### Offline installation
You can install recommended extensions from previously downloaded .vsix files
```bash
    cd MyAwesomeProject
    python3 vscode_extensions.py --offline=/path/to/vsix/dir
```
> [!NOTE]
> Extensions for which no corresponding .vsix files are found will be skipped

### VSCode CLI interface
You can specify path to VSCode executable, if you need
```bash
    cd MyAwesomeProject
    python3 vscode_extensions.py --vscode-path=/path/to/vscode
```
It can be useful, if you want to install extensions on remote VSCode server from remote host terminal.<br>
Typically integrated VSCode terminal adding VSCode to the beginning of the environment PATH.

### Silent mode
In silent mode any script and VSCode output will be redirected to the NULL-device (e.g. `/dev/null` in Linux or `NUL` in Windows)
```bash
    cd MyAwesomeProject
    python3 vscode_extensions.py --silent
```

### Verbose mode
Can be useful for debugging script
```bash
    cd MyAwesomeProject
    python3 vscode_extensions.py --verbose
```

> [!IMPORTANT]
> Silent mode takes precedence over verbose mode, but their combination will lead to output only the one warning about this combination



## Contribution
### Software for development
* Any supported OS from previous section
* Git 2.43.0
* VSCode 1.107.1 *(optional)*
