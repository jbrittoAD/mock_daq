# MockDAQDevice Project

## Overview

This project provides a mock implementation of a Data Acquisition (DAQ) device, `MockDAQDevice`, designed to simulate the behavior of digital input/output pins. The project includes a main class for the device, unit tests, and a simulation script to demonstrate the functionality of the device. It also includes a GitHub Actions workflow for continuous integration and continuous deployment (CI/CD).

## Project Structure

- `mock_daq.py`: Contains the `MockDAQDevice` class with methods to configure, read, write, toggle, and blink digital pins.
- `test_mock_daq.py`: Contains unit tests for the `MockDAQDevice` class using `pytest`.
- `simulation.py`: Contains a script to simulate and demonstrate the blinking functionality of the `MockDAQDevice`.
- `test.yml`: GitHub Actions workflow configuration for CI/CD.

## Why Use Threading Instead of Multiprocessing

### Advantages of Threading

1. **Shared Memory**: Threading allows sharing memory space between threads, making it easier to manage the state of pins without the need for complex inter-process communication (IPC). This is essential for the `MockDAQDevice` where the state of pins needs to be consistently accessed and modified.
  
2. **Lower Overhead**: Threads have lower overhead compared to processes. Starting a new thread is faster and uses less memory than starting a new process. Since the blinking operation is not CPU-intensive but rather I/O-bound (involves sleeping and toggling states), threading is more efficient.

3. **Simplicity**: Managing threads is generally simpler for I/O-bound tasks. For the `MockDAQDevice`, the operations are primarily about waiting (sleeping) and toggling states, which are well-suited for threading.

4. **GIL (Global Interpreter Lock)**: Python's Global Interpreter Lock (GIL) allows only one thread to execute Python bytecode at a time. For I/O-bound operations like blinking pins, the GIL is less of an issue, making threading a suitable choice.

### Disadvantages of Multiprocessing

1. **Higher Overhead**: Multiprocessing involves more overhead in creating and managing processes. Each process runs in its own memory space, which adds complexity and resource consumption.
   
2. **Complex Communication**: Sharing state between processes requires IPC mechanisms such as queues or pipes, which can be more complex to implement and manage.

### Justification for Using Threading

Given that the `MockDAQDevice` involves managing the state of pins with operations that are primarily I/O-bound (sleeping and toggling), threading provides a more efficient and simpler approach. The overhead and complexity of multiprocessing are not justified for this scenario, where the main tasks are lightweight and benefit from shared memory access.

## Random Delay Function

The `random_microsecond_delay` function simulates a real-world delay that might occur in an actual DAQ device. This function generates a random delay within a specified range, representing the unpredictable timing variations that can happen in real hardware operations. Incorporating this delay into the simulation provides a more realistic behavior, making the simulation closer to how an actual DAQ device would perform. This enhances the robustness and reliability of the simulation, allowing for better testing and understanding of how the device handles real-time operations and timing uncertainties.

## Simulation vs. Unit Tests

- **Simulation (`simulation.py`)**:
  - **Purpose**: Demonstrates the usage and functionality of the `MockDAQDevice` in a practical scenario.
  - **Benefit**: Allows observing the behavior of the device over time, making it easier to understand how the device operates in real-world conditions.

- **Unit Tests (`test_mock_daq.py`)**:
  - **Purpose**: Ensures the correctness of the `MockDAQDevice`'s functionality through automated tests.
  - **Benefit**: Provides a reliable way to verify that each method works as expected, catching bugs and regressions early in the development process.

Having both simulations and unit tests provides a comprehensive approach to validation: simulations for understanding usage and unit tests for ensuring correctness.

## Documentation

For automated documentation, the Sphinx library would be utilized to generate comprehensive documentation from the code. Unfortunately, due to time constraints, this has not been implemented yet. Sphinx would provide a robust solution for maintaining up-to-date and easily navigable documentation for the project.

## How to Run the Project

### Prerequisites

Ensure you have Python installed. It's recommended to use a virtual environment to manage dependencies.

### Cloning the Repository

```sh
git clone https://github.com/jbrittoAD/mock_daq
cd mock_daq
```

### Setting Up the Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Running the Simulation

```sh
python simulation.py
```

### Running Unit Tests

```sh
pytest test_mock_daq.py
```

### Running Tests with GitHub Actions (CI/CD)

The `test.yml` file in the `.github/workflows` directory is configured to run the tests automatically on GitHub. To set up the CI/CD pipeline:

1. Push your code to a GitHub repository.
2. Ensure the `test.yml` workflow file is in the `.github/workflows` directory.
3. GitHub Actions will automatically run the tests on each push or pull request.

## Conclusion

This project provides a mock implementation of a DAQ device, complete with unit tests and simulation scripts to demonstrate its functionality. Using threading for pin blinking operations ensures efficient and manageable code, while having both simulations and tests ensures comprehensive validation of the device's behavior. By following the instructions above, you can clone, run, and test the project effectively. Incorporating Sphinx for automated documentation in the future will further enhance the project's maintainability and usability.