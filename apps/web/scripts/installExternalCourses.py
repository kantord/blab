import json
import sys
import os


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} PATH_TO_CONFIG_FILE")
    config_filename = sys.argv[1]
    with open(config_filename) as f_h:
        config = json.load(f_h)

    for course in config:
        if course["deploy"]:
            cmd = f"""yarn installCourse "{course['url']}" {course["paths"]["jsonFolder"]}"""
            print(cmd)
            exit_code = os.system(cmd)
            if exit_code != 0:
                sys.exit(
                    f"""We failed to install {course["paths"]["jsonFolder"]}. Terminating"""
                )


if __name__ == "__main__":
    main()
