
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time

from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen, Request


def should_ignore(name):
    """
    Returns True if the given name (directory or file) should not be copied.
    :param name: String
    :return: bool
    """

    # Ignore python virtual envs or the python cache
    if name in ["venv", "__pycache__"]:
        return True

    # Ignore bytecode files
    if name.endswith(".pyc"):
        return True

    # Copy everything else
    return False


class Deploy_To_Mothership:

    def __init__(self):

        self.src_path = "./src"
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdir_src = Path(self.tempdir.name) / "src"
        self.ssh_key = f'{os.getcwd()}/.ssh/robolab_group_key'

        try:
            with open(self.ssh_key) as f:
                for line in f:
                    pass
        except FileNotFoundError:
            print("Your ssh group key could not be found.")
            print("Please make sure to place your key at " + self.ssh_key)
            exit()
        self.group = line.strip()
        try:
            int(self.group)
        except ValueError:
            print("Your ssh group key file is malformed.")
            print("Please make sure the key file isn't modified.")
            exit()

        if(1 < int(self.group) > 42):
            print("Your ssh group key file is malformed.")
            print("Please make sure the key file isn't modified.")
            exit()

        self.ssh_url = "se"+str(self.group)+"@mothership.inf.tu-dresden.de"

        with open(self.ssh_key, "rb") as key:
            bytes = key.read()
            self.key_hash = hashlib.sha256(bytes).hexdigest()

    def copy_files(self):
        """
        Copy local files to brick
        :return: void
        """
        print('Uploading ./src to mothership...')

        def filter(src, names):
            """
            Filter overwrite
            :param src: String
            :param names: String
            :return: List
            """
            return [name for name in names if should_ignore(name)]

        # Copy files into temporary directory first
        shutil.copytree(str(self.src_path), str(
            self.tempdir_src), ignore=filter)

        # Connect with SSH-PubKey and copy files
        subprocess.run(
            ['scp', '-i', self.ssh_key,
             #'-o', 'IdentitiesOnly=yes',
             #'-o', 'StrictHostKeyChecking=no',
             '-r', "src",
             # this file must be copied last, it triggers the reloader on the brick
             # ".trigger", no trigger here!
             '{}:~/'.format(self.ssh_url)
             ], cwd=str(self.tempdir.name), stdout=subprocess.DEVNULL)
        print('Upload complete.')

    def deploy(self):
        # let the mothership copy files to robot
        print("Downloading ./src into robot...")
        subprocess.run([
            'ssh', '-i', self.ssh_key,
            self.ssh_url,
            'python /home/students/deploy.py'
        ])
        print("Download complete.")

    def start_connect_in_screen(self):
        # starts the connect script inside our screen
        print("Connecting screen to robot...")
        subprocess.run([
            'ssh', '-i', self.ssh_key,
            self.ssh_url,
            """screen -S robolab -X stuff "python3 /home/students/connect.py\n\""""
        ])

    def open_screen(self):
        # attaches to screen
        print("Attaching to screen...")
        subprocess.run([
            'ssh', '-tt', '-i', self.ssh_key,
            self.ssh_url,
            "screen -x robolab"
        ])

    def inject_queue_message(self):
        print("Injecting queue message...")
        queueing_time = 0
        queue_position = 0
        planet = ""

        with urlopen('https://robolab.inf.tu-dresden.de/queue/api/v1/robot/'+self.group+'/status') as response:
            status = response.read().decode('utf-8')

            status = json.loads(status)

            queue_position = status['queue']['position']
            queueing_time = status['queue']['timestamp']
            queueing_time = time.ctime(int(queueing_time)//1000)
            planet = status['queue']['planet']

        subprocess.run([
            'ssh', '-i', self.ssh_key,
            self.ssh_url,
            'screen -S robolab -X stuff "\nYou have been queued on ' +
            planet+' at ' +
            str(queueing_time)+'. Your Position in the queue is ' +
            str(queue_position)+'.\n\"'
        ])

    def queue_robot(self):
        print("Placing robot in queue...")
        req = Request(
            "https://robolab.inf.tu-dresden.de/queue/api/v1/robot/"+self.group+"/queue")
        req.add_header('Cookie', 'robot_ssh_auth='+self.key_hash)
        try:
            urlopen(req)
        except HTTPError as response:
            print(response)
            print("Did you set your robot position?")
            print("You can do so at https://robolab.inf.tu-dresden.de/queue")
            print("If so, make sure your key is unmodified.")
            exit()

    def unqueue_robot(self):
        print("Placing robot in queue...")
        req = Request("https://robolab.inf.tu-dresden.de/queue/api/v1/robot/" +
                      self.group+"/unqueue")
        req.add_header('Cookie', 'robot_ssh_auth='+self.key_hash)
        try:
            urlopen(req)
        except HTTPError as response:
            print(response)
            print("Your key may be wrong. Please make sure not to modify it.")
            exit()

    def get_log(self):
        print("Getting latest log file from Robot...")
        subprocess.run([
            'ssh', '-i', self.ssh_key,
            self.ssh_url,
            "/home/students/get_latest_log.sh"
        ])
        print("Downloading latest log file from Mothership...")
        subprocess.run([
            'scp', '-i', self.ssh_key,
            '{}:/home/students/se{}/logs/latest.log'.format(
                self.ssh_url, self.group),
            "./logs/latest.log"
        ])

    def check_screen(self):

        def destroy_screens(self):
            print("Something unexpected happened. Closing all robolab screens...")
            screen_sessions = subprocess.check_output(
                ['ssh', '-i', self.ssh_key,
                 self.ssh_url,
                 'bash', '-c', "\"screen -ls | grep robolab  | sed 's/\\t//' | sed 's/\\t.*$//'\""
                 ])
            screen_sessions = screen_sessions.decode('utf-8')
            screen_sessions_list = screen_sessions.splitlines()
            for session in screen_sessions_list:
                subprocess.run([
                    'ssh', '-i', self.ssh_key,
                    self.ssh_url,
                    'screen -X -S ' + session + ' kill'
                ])

        def create_screen(self):
            print("Creating new screen...")
            subprocess.run([
                'ssh', '-i', self.ssh_key,
                self.ssh_url,
                'screen -dmS robolab && screen -S robolab -X multiuser on'
            ])

        # get the state of all robolab screens
        screens = subprocess.check_output(
            ['ssh', '-i', self.ssh_key,
             self.ssh_url,
             'bash', '-c', "\"screen -ls | grep robolab  | sed 's/.*\\t.*\\t.*\\t//'\""
             ])
        screens = screens.decode('utf-8')
        screens = screens.splitlines()
        # If theres no robolab screen, start one
        if (not screens):
            create_screen(self)
            self.start_connect_in_screen()
            return

        elif(len(screens) == 1):
            # if there is exactly one robolab screen, check if multiuser mode is enabled
            # if not, enable it
            if(screens[0] == "(Detached)" or screens[0] == "(Attached)"):
                subprocess.run([
                    'ssh', '-i', self.ssh_key,
                    self.ssh_url,
                    'screen -S robolab -X multiuser on'
                ])
        else:
            # If there are multiple robolab screens running, kill all of them and start a new one
            destroy_screens(self)
            # create a new screen after all robolab screens were killed
            create_screen(self)
            self.start_connect_in_screen()
            return

        # we now have exactly one robolab-screen for this group. We need to make sure, that the right command runs in it
        screen_pid = subprocess.check_output(
            ['ssh', '-i', self.ssh_key,
             self.ssh_url,
             'bash', '-c', "\"screen -ls | grep robolab  | sed 's/^\\t//' | sed 's/\\..*$//'\""
             ]).decode('utf-8').splitlines()
        # if the above would return an empty list, something killed our screen the moment we created it.
        screen_bash_pid = subprocess.check_output(
            ['ssh', '-o', 'LogLevel=QUIET', '-tt', '-i', self.ssh_key,
             self.ssh_url,
             '/home/students/bash_pid_in_screen.sh', screen_pid[0]
             ]).decode('utf-8').splitlines()

        if not screen_bash_pid:
            # something messed with this screen, we need to recreate it.
            destroy_screens(self)
            create_screen(self)
            self.start_connect_in_screen()

        else:
            command_in_screen = subprocess.check_output(
                ['ssh', '-o', 'LogLevel=QUIET', '-tt', '-i', self.ssh_key,
                 self.ssh_url,
                 '/home/students/command_in_screen.sh', screen_pid[0]
                 ]).decode('utf-8').splitlines()
            if(not command_in_screen[0]):
                # just a plain bash in screen, we can start connect
                self.start_connect_in_screen()
            elif(command_in_screen[0].strip() == "python3 /home/students/connect.py"):
                pass  # connect is already running.
            else:
                # something else is running in this screen. destroy, recreate, connect.
                destroy_screens(self)
                create_screen(self)
                self.start_connect_in_screen()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy your code.')
    parser.add_argument('-r', '--restart', action='store_true',
                        help="requeue without reuploading code", default=False)
    parser.add_argument('-l', '--get-log', action='store_true',
                        help="download latest log file into ./logs", default=False)
    parser.add_argument('-j', '--just-listen',
                        action='store_true', help="tune into the current session", default=False)

    flags = parser.parse_args()
    if flags.get_log + flags.just_listen + flags.restart > 1:
        print("Only one simultaneous flag is permitted.")
        exit()

    mothership = Deploy_To_Mothership()

    if flags.get_log:
        mothership.get_log()
        exit()

    if not flags.restart and not flags.just_listen:
        mothership.copy_files()
        mothership.deploy()
    mothership.check_screen()
    if not flags.just_listen:
        mothership.queue_robot()
        mothership.inject_queue_message()
    mothership.open_screen()
    if not flags.just_listen:
        mothership.unqueue_robot()
