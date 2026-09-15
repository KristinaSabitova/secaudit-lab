import subprocess


def make_backup(label):
    # The lab's command only prints: nothing is archived or written.
    result = subprocess.run(f"echo backup {label}", shell=True,
                            capture_output=True, text=True)
    return result.stdout
