from ternya import Ternya
from multiprocessing import Process

if __name__ == "__main__":
    ternya = Ternya()
    ternya.read("config.ini")
    process = Process(target=ternya.work)
    process.start()
