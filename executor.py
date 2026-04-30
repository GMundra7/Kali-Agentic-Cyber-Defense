import docker

client = docker.from_env()

CONTAINER_NAME = "girish-container"  # change this

def run_command(cmd: str, timeout: int = 60):
    try:
        container = client.containers.get(CONTAINER_NAME)

        result = container.exec_run(
            cmd,
            stdout=True,
            stderr=True,
            demux=False
        )

        return result.output.decode()

    except Exception as e:
        return f"Error: {str(e)}"