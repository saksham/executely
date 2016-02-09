#!/bin/python
import os
import subprocess, signal, shutil
from executely.constants import Java, ExitCodes
from executely.config import AppConfiguration


def ensure_logfiles_exist(config):
    open(config.stdout_path, 'a').close()
    open(config.stderr_path, 'a').close()


def get_pid_file_path(app_name, app_path):
    return os.path.join(app_path, app_name + '.pid')


def write_pid_file(app_name, app_path, pid):
    pid_file_path = get_pid_file_path(app_name, app_path)
    with open(pid_file_path, 'w') as pid_file:
        pid_file.write(str(pid))

def has_pid_file(app_name, app_path):
    pid_file_path = get_pid_file_path(app_name, app_path)
    return os.path.exists(pid_file_path)

def get_pid(app_name, app_path):
    pid_file_path = get_pid_file_path(app_name, app_path)
    with open(pid_file_path) as pid_file:
        return int(pid_file.readline())


def validate(app_name, app_path):
    if (not os.path.exists(app_path)):
        raise Exception('The app folder %s does not exist!' % app_name)

def cleanup(app_name, app_path):
    validate(app_name, app_path)
    stop(app_name, app_path)
    filelist = [ f for f in os.listdir(app_path) if f.endswith(".log") ]
    for f in filelist:
            os.remove(f)

def verify_java_executable(java_command):
    FNULL = open(os.devnull, 'w')
    try:
        exit_code = subprocess.call([java_command, '-version'], stderr=FNULL, stdout=FNULL)
        if exit_code != 0:
            raise Exception('The command "%s -version" did not exit cleanly' % java_command)
    except Exception:
        raise Exception('Failed to execute Java with "%s" command. Please ensure that java is installed and JAVA_HOME is set' % java_command)

def start(app_name, app_path, java_command=Java.DEFAULT_COMMAND, detached=True):
    os.chdir(app_path)

    app_config = AppConfiguration(app_path)

    if not app_config.is_valid():
        print('Invalid app configuration found, Exiting with exit code: ' + str(ExitCodes.INVALID_CONFIGURATION))
        exit(ExitCodes.INVALID_CONFIGURATION)

    if has_pid_file(app_name, app_path):
        print('An instance of %s app is already running, so new instance will not be started!' % app_name)
        exit(ExitCodes.ALREADY_RUNNING)

    ensure_logfiles_exist(app_config)
    stdout = open(app_config.stdout_path, 'w')
    stderr = open(app_config.stderr_path, 'w')

    verify_java_executable(java_command)
    command = app_config.get_command(java_command)
    try:
        if detached:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr, stdin=subprocess.PIPE)
            write_pid_file(app_name, app_path, process.pid)
        else:
            subprocess.call(command)

    except Exception as inst:
        stdout.close()
        stderr.close()
        print(type(inst), file=sys.stderr) # the exception instance
        print(inst.args, file=sys.stderr)  # arguments stored in .args
        print(inst, file=sys.stderr)
        exit(ExitCodes.FAILED_TO_START)

    return(ExitCodes.SUCCESS)


def stop(app_name, app_path):
    pid_file_path = get_pid_file_path(app_name, app_path)
    if (not os.path.exists(pid_file_path)):
        return

    pid = get_pid(app_name, app_path)
    try:
        os.kill(pid, signal.SIGTERM)
    except:
        print("Failed to stop app %s!" % app_name)
        if pid:
            print("The app '%s' had PID: %s" % (app_name, pid))
        raise
    finally:
        os.remove(pid_file_path)
