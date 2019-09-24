from datafetcher import MyDataFetcher
from dataclass import MyDataClass
# from presentation import MyPresentation
from generalfunc import general
from program import MyHeatPainProgramme
from presentaion import MyPresentation
import matplotlib.pyplot as plt


def run():

    data = MyDataClass()
    MyPresentation(data)
    fetcher = MyDataFetcher(data)
    prog = MyHeatPainProgramme()

    fetcher.start()
    prog.start()
    plt.show()


if __name__ == "__main__":
    import config
    config.init()
    run()
