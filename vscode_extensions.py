import argparse
import os, sys, io, platform
from colorama import Fore, Style, init as colorama_init
import json
from pathlib import Path
import subprocess



VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 1
VERSION =   (VERSION_MAJOR & 0xFF) << 24 | \
            (VERSION_MINOR & 0xFF) << 16 | \
            (VERSION_PATCH & 0xFFFF)
VERSION_STR =   str(VERSION_MAJOR) + '.' + \
                str(VERSION_MINOR) + '.' + \
                str(VERSION_PATCH)

MSG_ERROR = Fore.RED + Style.BRIGHT + 'ERROR:' + Style.RESET_ALL
MSG_WARNING = Fore.YELLOW + Style.BRIGHT + 'WARNING:' + Style.RESET_ALL



def testFile(File: str) -> bool:
    if not os.path.exists(File):
        print(f'{Fore.RED}failure{Fore.RESET} - not exists', file = VerboseFile)
        return False

    if not os.path.isfile(File):
        print(f'{Fore.RED}failure{Fore.RESET} - not a file', file = VerboseFile)
        return False

    return True

def testExecutable(File: str) -> bool:
    if testFile(File) == False:
        return False

    if not os.access(File, os.X_OK, follow_symlinks = True):
        print(f'{Fore.RED}failure{Fore.RESET} - not executable', file = VerboseFile)
        return False

    return True

def testVSCodeExec() -> bool:
    global ARGS
    print(f'Checking VSCode executable: {ARGS['VSCodeExec']}', file = VerboseFile)

    VSCodePath = os.path.expanduser(os.path.expandvars(ARGS['VSCodeExec']))
    ARGS['VSCodeExec'] = VSCodePath
    print(f'Expanded path: {VSCodePath}', file = VerboseFile)

    if not os.path.isabs(VSCodePath) and os.path.dirname(VSCodePath) == '':
        # Try find in $PATH
        print(f'Try find in $PATH:', file = VerboseFile)

        PATH = os.getenv('PATH', '').encode('utf-8').decode('utf-8').split(os.pathsep)
        for Dir in PATH:
            FullPath = os.path.join(Dir, VSCodePath)
            print(f'Test {FullPath}: ', end = '', file = VerboseFile)
            if testExecutable(FullPath):
                print(f'{Fore.GREEN}success{Fore.RESET}', file = VerboseFile)
                return True

    else:
        # Try given path
        print(f'Test {VSCodePath}: ', end = '', file = VerboseFile)
        if testExecutable(VSCodePath):
            print(f'{Fore.GREEN}success{Fore.RESET}', file = VerboseFile)
            return True

    # Not found!
    return False

def getExtensionsList() -> list | None:
    print(f'Searching input JSON', file = VerboseFile)

    # Test all *.code-workspace files
    InputJSONFiles = [
        file.path for file in os.scandir(os.path.curdir)
        if file.name.endswith('.code-workspace')
    ]
    InputJSONFiles.append(os.path.join('.', '.vscode', 'extensions.json'))

    for File in InputJSONFiles:
        print(f'Test {File}: ', end = '', file = VerboseFile)

        if testFile(File) == False:
            continue
        if not os.access(File, os.R_OK, follow_symlinks = True):
            print(f'{Fore.RED}failure{Fore.RESET} - not readable', file = VerboseFile)
            continue

        try:
            JsonFile = open(File, 'r', encoding = 'utf-8', errors = 'strict')
        except:
            print(f'{Fore.RED}failure{Fore.RESET} - unable to load JSON', file = VerboseFile)
            continue

        try:
            JSON = json.load(JsonFile)
            if File.endswith('.code-workspace'):
                JSON = JSON['extensions']
            List = JSON['recommendations']
        except:
            print(f'{Fore.RED}failure{Fore.RESET} - invalid JSON schema', file = VerboseFile)
            continue

        if len(List) == 0:
            print(f'{Fore.RED}failure{Fore.RESET} - empty list', file = VerboseFile)
            continue

        print(f'{Fore.GREEN}success{Fore.RESET}', file = VerboseFile)
        return List

    return None

def testVSIXDir() -> bool:
    global ARGS
    print(f'Checking VSIX directory: {ARGS['Path2VSIX']}', file = VerboseFile)
    ARGS['Path2VSIX'] = os.path.expanduser(os.path.expandvars(ARGS['Path2VSIX']))

    print(f'Test {ARGS['Path2VSIX']}: ', end = '', file = VerboseFile)
    if not os.path.exists(ARGS['Path2VSIX']):
        print(f'{Fore.RED}failure{Fore.RESET} - not exists', file = VerboseFile)
        return False

    if not os.path.isdir(ARGS['Path2VSIX']):
        print(f'{Fore.RED}failure{Fore.RESET} - not a directory', file = VerboseFile)
        return False

    print(f'{Fore.GREEN}success{Fore.RESET}', file = VerboseFile)
    return True

if __name__ == "__main__":
    sys.stdin  = io.TextIOWrapper(sys.stdin.buffer,  encoding = 'utf-8', errors = 'strict')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8', errors = 'strict')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding = 'utf-8', errors = 'strict')

    colorama_init(autoreset = True)

    if platform.system() == 'Windows':
        sys.argv = [arg.encode('utf-8').decode('utf-8') for arg in sys.argv]

    NullDeviceFile = ''
    if platform.system() == 'Linux':
        NullDeviceFile = '/dev/null'
    elif platform.system() == 'Windows':
        NullDeviceFile = 'NUL'
    else:
        print(f'{MSG_ERROR} unsupported platform "{platform.system()}"', file = sys.stderr)
        exit(1)
    NullFile = open(NullDeviceFile, 'w', encoding = 'utf-8', errors = 'ignore')
    VerboseFile = NullFile


    Parser = argparse.ArgumentParser(
        description =
            'VSCode extensions auto-installer'
    )
    Parser.add_argument(
        '-v', '--version',
        dest = 'DumpVersion',
        action = 'store_true',
        help = 'dump current version of script and exit'
    )
    Parser.add_argument(
        '--verbose',
        dest = 'Verbose',
        action = 'store_true',
        help = 'verbose output - lots of information'
    )
    Parser.add_argument(
        '-s', '--silent',
        dest = 'Silent',
        action = 'store_true',
        help = 'silent installation - no output at all'
    )
    Parser.add_argument(
        '--vscode-path',
        dest = 'VSCodeExec',
        action = 'store',
        type = str,
        default = 'code' if platform.system() == 'Linux' else 'code.cmd',
        metavar = 'PATH',
        help = 'specify path to VSCode executable'
    )
    Parser.add_argument(
        '--offline',
        dest = 'Path2VSIX',
        action = 'store',
        type = str,
        metavar = 'PATH',
        help =
            'offline installation. '
            'Specify path to previously downloaded .vsix files'
    )
    ARGS = vars(Parser.parse_args())

    if ARGS['DumpVersion']:
        print(f'{VERSION_STR}')
        exit(0)

    if ARGS['Verbose']:
        VerboseFile = sys.stdout
        print(f'Verbose mode activated!', file = VerboseFile)

    if ARGS['Silent']:
        print(f'Silent mode! Redirecting STDOUT to "{NullDeviceFile}"', file = VerboseFile)
        if ARGS['Verbose']:
            print(f'{MSG_WARNING} specified "--verbose" and "--silent" flags. Ignoring "--verbose"', file = VerboseFile)
            ARGS['Verbose'] = False
            VerboseFile = NullFile
        sys.stdout = NullFile



    if testVSCodeExec() == False:
        print(f'{MSG_ERROR} VSCode executable not found!', file = sys.stderr)
        exit(1)

    ExtensionsList = getExtensionsList()
    if ExtensionsList == None:
        print(f'{MSG_ERROR} JSON contains extensions list not found!', file = sys.stderr)
        exit(1)

    Extensions2Install = ExtensionsList.copy()
    if ARGS['Path2VSIX'] != None:
        print(f'Offline mode activated', file = VerboseFile)

        if testVSIXDir() == False:
            print(f'{MSG_ERROR} VSIX directory not found!', file = sys.stderr)
            exit(1)

        Extensions2Install.clear()

        print(f'Find local vsix files', file = VerboseFile)
        for Ext in ExtensionsList:
            print(f'Try for "{Ext}":', file = VerboseFile)
            IsFound = False
            for vsix in Path(ARGS['Path2VSIX']).glob('*.vsix'):
                PathToVSIX = os.path.join(ARGS['Path2VSIX'], vsix.name)
                print(f' Test {PathToVSIX}: ', end = '', file = VerboseFile)
                if Ext.lower() in vsix.name:
                    if not os.access(PathToVSIX, os.R_OK):
                        print(f'{Fore.RED}failure{Fore.RESET} - not readable', file = VerboseFile)
                        continue

                    IsFound = True
                    Extensions2Install.append(PathToVSIX)
                    print(f'{Fore.GREEN}yes{Fore.RESET}', file = VerboseFile)
                    break
                else:
                    print(f'{Fore.RED}no{Fore.RESET}', file = VerboseFile)
            if not IsFound:
                print(f'{MSG_WARNING} .vsix for {Ext} not found! Skipping...')

    for Ext in Extensions2Install:
        print(f'Installing {Ext}: ', end = '')
        Result = subprocess.run([
            ARGS['VSCodeExec'],
            '--install-extension',
            Ext
        ], check = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if Result.returncode == 0:
            print(f'{Fore.GREEN}success{Fore.RESET}')
        else:
            print(f'{Fore.RED}failure{Fore.RESET}')
            # Print error onto STDOUT exactly, because this is not critical failure!
            # and it's must be ignored in silent mode
            print(f'{MSG_ERROR} installation error! {Result.stderr.decode('utf-8')}', file = sys.stdout)
