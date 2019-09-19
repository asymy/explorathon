from datafetcher import MyDataFetcher
from dataclass import MyDataClass
# from presentation import MyPresentation
import config
from generalfunc import general
from program import MyHeatPainProgramme
from presentaion import MyPresentation
import matplotlib.pyplot as plt


config.init()
gen = general()
data = MyDataClass()
pres = MyPresentation(data)
fetcher = MyDataFetcher(data)
prog = MyHeatPainProgramme()

fetcher.start()
prog.start()
plt.show()
