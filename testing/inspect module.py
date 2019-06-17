import os
import inspect

src = inspect.getsource(os)
print(src)