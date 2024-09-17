import os
from qiskit import QuantumCircuit, transpile, execute
from qiskit_aer import AerSimulator
from qiskit_ibm_provider import IBMProvider
from loguru import logger

# Create logs directory if it does not exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger.add(os.path.join(logs_dir, "quantum_connection.log"), rotation="1 week", retention="1 month", level="DEBUG")

class QuantumConnection:
    def __init__(self):
        """
        Initialize the QuantumConnection class and set up the quantum backend.
        """
        self.backend = self._connect_to_backend()

    def _connect_to_backend(self):
        """
        Connect to a quantum backend based on the environment settings.
        :return: The selected quantum backend.
        """
        mode = os.getenv('MODE', 'DEVELOPMENT').upper()
        provider = os.getenv('QUANTUM_PROVIDER', 'IBMQ').upper()
        
        if mode == 'DEVELOPMENT':
            logger.info("Using local simulator for development.")
            return AerSimulator()
        
        elif mode == 'PRODUCTION':
            if provider == 'IBMQ':
                logger.info("Connecting to IBMQ backend.")
                IBMProvider.load_account()
                return IBMProvider.get_backend('ibmq_qasm_simulator')
            
            elif provider == 'GOOGLE':
                # Handle connection to Google's CIRQ provider.
                logger.warning("Google CIRQ is not yet supported.")
                raise NotImplementedError("Google CIRQ is not yet supported.")
            
            elif provider == 'LOCAL':
                # Handle local quantum computers if available
                logger.warning("Local quantum computers are not yet supported.")
                raise NotImplementedError("Local quantum computers are not yet supported.")
            
            else:
                logger.error(f"Unsupported provider: {provider}")
                raise ValueError(f"Unsupported provider: {provider}")
        
        else:
            logger.error(f"Unsupported mode: {mode}")
            raise ValueError(f"Unsupported mode: {mode}")

    def get_backend(self):
        """
        Get the current quantum backend.
        :return: The quantum backend.
        """
        return self.backend

    def transpile_circuit(self, circuit):
        """
        Transpile the quantum circuit for execution on the selected backend.
        :param circuit: The quantum circuit to transpile.
        :return: Transpiled quantum circuit.
        """
        return transpile(circuit, backend=self.backend)

    def execute_circuit(self, circuit):
        """
        Execute the quantum circuit on the selected backend.
        :param circuit: The quantum circuit to execute.
        :return: The result of the execution.
        """
        return execute(circuit, backend=self.backend).result()

    def get_counts(self, result):
        """
        Extract measurement counts from the execution result.
        :param result: The result of the quantum circuit execution.
        :return: Measurement counts.
        """
        return result.get_counts()
