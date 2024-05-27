from abc import ABC, abstractmethod
import asyncio

class AbstractVMServer(ABC):
    @abstractmethod
    async def connect(self, login, pwd):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def create_vm(self):
        pass

    @abstractmethod
    async def list_vm_authored(self):
        pass

    @abstractmethod
    async def list_vm_connected(self):
        pass

    @abstractmethod
    async def list_vm_all(self):
        pass