import logging


main_logger = logging.getLogger('main')
test_logger = logging.getLogger('test')
minor_logger = logging.getLogger('minor functionality')


__all_loggers__ = [main_logger, test_logger, minor_logger]


class AnsiColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        no_style = '\033[0m'
        bold = '\033[91m'
        grey = '\033[90m'
        yellow = '\033[93m'
        red = '\033[31m'
        red_light = '\033[91m'
        start_style = {
            'DEBUG': grey,
            'INFO': no_style,
            'WARNING': yellow,
            'ERROR': red,
            'CRITICAL': red_light + bold,
        }.get(record.levelname, no_style)
        end_style = no_style
        return f'{start_style}{super().format(record)}{end_style}'


for l in __all_loggers__:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG) # DEBUG INFO WARNING ERROR CRITICAL
    formatter = AnsiColorFormatter('{asctime} | {levelname:<8s} | {name:<20s} | {message}', style='{')
    handler.setFormatter(formatter)
    l.addHandler(handler)
    l.setLevel(logging.DEBUG) # DEBUG INFO WARNING ERROR CRITICAL


if __name__ == '__main__':
    for l in __all_loggers__: l.debug('Test')
    for l in __all_loggers__: l.info('Test')
    for l in __all_loggers__: l.warning('Test')
    for l in __all_loggers__: l.error('Test')
    for l in __all_loggers__: l.critical('Test')
    