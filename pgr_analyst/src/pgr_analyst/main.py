#!/usr/bin/env python
import sys
from pgr_analyst.crew import PgrAnalystCrew


def run():
    """
    Run the crew.
    """
    PgrAnalystCrew().crew().kickoff()


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        PgrAnalystCrew().crew().train(n_iterations=4, filename="pgr_analyst")

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        PgrAnalystCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "Cruzeiro esporte clube"
    }
    try:
        PgrAnalystCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "train":
            train()
        elif sys.argv[1] == "replay":
            replay()
        elif sys.argv[1] == "test":
            test()
    else:
        run()