[Link to article](https://medium.com/@kamilmatejuk/inside-python-colorful-logging-ad3a74442cc6)

You can define all your loggers in one module, and then import the one you need.
```python
from loggers import main_logger as logger

logger.warn('WARNING')
```

```python
from loggers import test_logger as logger

try:
    1/0
except ZeroDivisionError as ex:
    logger.exception(ex)
```

Enjoy your colorful logs :)

### Links:
  * [ANSI coloring codes](https://gist.github.com/KamilMatejuk/3438a50b27cdbaa10b62cc0ed7f68450)
  * 