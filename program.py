from datafetcher import MyDataFetcher
from dataclass import MyDataClass
import config
from generalfunc import general
gen = general()

config.init()

data = MyDataClass()
fetcher = MyDataFetcher(data)
fetcher.start()
