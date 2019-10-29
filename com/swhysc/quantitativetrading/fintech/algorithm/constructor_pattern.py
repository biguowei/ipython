
class Computer:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.memory = None
        self.hadd = None
        self.gpu = None

    def __str__(self):
        info = (f'Memory:{self.memoryGB}',
                'Hard Disk:{self.hadd}GB',
                'Graphics Card:{self.gpu}')
        return ''.join(info)


class ComputerBuilder:
    def __init__(self):
        self.computer = Computer('Jim1996')


    def configure_memory(self, amount):
        self.computer.memory = amount
        return self  # 为了方便链式调用


    def configure_hdd(self, amount):
        pass


    def configure_gpu(self, gpu_model):
        pass


class HardwareEngineer:
    def __init__(self):
        self.builder = None

    def construct_computer(self, memory, hdd, gpu):
        self.builder = ComputerBuilder()
        self.builder.configure_memory(memory).configure_hdd(hdd).configure_gpu(gpu)

    @property
    def computer(self):
        return self.builder.computer