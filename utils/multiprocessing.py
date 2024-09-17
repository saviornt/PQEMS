import asyncio
import multiprocessing as mp
import torch
from loguru import logger
import os
import subprocess


class MultiProcessingManager:
    def __init__(self):
        """
        Initialize the multiprocessing manager to handle different processing types:
        CPU-bound, GPU-bound, and async-bound tasks.
        """
        self.cpu_pool = mp.Pool(mp.cpu_count())  # CPU pool with the number of available CPU cores
        self.gpu_available = torch.cuda.is_available()  # Check if GPU is available
        self.gpu_device = torch.device("cuda" if self.gpu_available else "cpu")
        self.loop = asyncio.get_event_loop()
        logger.info(f"Multiprocessing Manager initialized with {mp.cpu_count()} CPUs and GPU: {self.gpu_available}")

    def _run_cpu_task(self, task, *args, **kwargs):
        """
        Run CPU-bound tasks using multiprocessing pool.
        :param task: The task function to be executed.
        :param args: Arguments for the task.
        :param kwargs: Keyword arguments for the task.
        :return: The result of the task execution.
        """
        try:
            result = self.cpu_pool.apply(task, args=args, kwds=kwargs)
            logger.info(f"CPU task completed: {task.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error running CPU task {task.__name__}: {e}")
            raise

    async def _run_async_task(self, task, *args, **kwargs):
        """
        Run async-bound tasks using asyncio.
        :param task: The async task function to be executed.
        :param args: Arguments for the task.
        :param kwargs: Keyword arguments for the task.
        :return: The result of the task execution.
        """
        try:
            result = await task(*args, **kwargs)
            logger.info(f"Async task completed: {task.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error running async task {task.__name__}: {e}")
            raise

    def _check_cuda_availability(self):
        """
        Check if the system has CUDA 11 or higher installed. If not, fall back to PyTorch's default GPU settings.
        :return: Boolean indicating whether CUDA 11 or higher is available.
        """
        try:
            # Check for CUDA version using the 'nvcc' command
            result = subprocess.run(['nvcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            
            # Look for the version number in the output
            if 'release' in output:
                version = output.split('release ')[-1].split(',')[0].strip()
                major_version = int(version.split('.')[0])
                if major_version >= 11:
                    logger.info(f"CUDA {version} detected, using CUDA for GPU tasks.")
                    return True
                else:
                    logger.warning(f"CUDA version {version} detected, but CUDA 11 or higher is required. Falling back to PyTorch.")
            else:
                logger.warning("No valid CUDA version found. Falling back to PyTorch.")
        except FileNotFoundError:
            # 'nvcc' command not found, meaning CUDA is not installed
            logger.warning("CUDA is not installed or 'nvcc' command is unavailable. Falling back to PyTorch.")
        except Exception as e:
            logger.error(f"Error checking CUDA version: {e}")

        return torch.cuda.is_available()

    def _run_gpu_task(self, task, *args, **kwargs):
        """
        Run GPU-bound tasks using PyTorch.
        :param task: The task function to be executed.
        :param args: Arguments for the task.
        :param kwargs: Keyword arguments for the task.
        :return: The result of the task execution.
        """
        try:
            with torch.cuda.device(self.gpu_device):
                result = task(*args, **kwargs)
            logger.info(f"GPU task completed: {task.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error running GPU task {task.__name__}: {e}")
            raise

    def run_task(self, task, task_type="cpu", *args, **kwargs):
        """
        General task runner that routes tasks based on their type: CPU, async, or GPU.
        :param task: The task function to be executed.
        :param task_type: Type of task: 'cpu', 'async', 'gpu'.
        :param args: Arguments for the task.
        :param kwargs: Keyword arguments for the task.
        :return: The result of the task execution.
        """
        if task_type == "cpu":
            return self._run_cpu_task(task, *args, **kwargs)
        elif task_type == "async":
            return self.loop.run_until_complete(self._run_async_task(task, *args, **kwargs))
        elif task_type == "gpu":
            if self.gpu_available:
                return self._run_gpu_task(task, *args, **kwargs)
            else:
                logger.error("GPU task requested, but no GPU is available.")
                raise RuntimeError("No GPU available for task.")
        else:
            logger.error(f"Invalid task type provided: {task_type}")
            raise ValueError(f"Unsupported task type: {task_type}")

    def close(self):
        """
        Close all resources such as CPU pool and event loop.
        """
        try:
            self.cpu_pool.close()
            self.cpu_pool.join()
            logger.info("CPU pool closed.")
            self.loop.close()
            logger.info("Event loop closed.")
        except Exception as e:
            logger.error(f"Error closing resources: {e}")


# Example task functions to be passed to the manager:

def cpu_bound_task(x):
    logger.info(f"Running CPU-bound task with input {x}")
    return x ** 2

async def async_bound_task(x):
    logger.info(f"Running Async-bound task with input {x}")
    await asyncio.sleep(1)  # Simulate I/O-bound operation
    return x * 2

def gpu_bound_task(x):
    logger.info(f"Running GPU-bound task with input {x}")
    tensor = torch.tensor([x], device="cuda")
    return (tensor * 2).cpu().numpy()

