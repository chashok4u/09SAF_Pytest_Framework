format_logger = {
    'version': 1,
     'formatters':
         {
             'simple':{'format': '%(asctime)s: %(name)s: %(levelname)s: %(message)s'},
             'detail': {'format': '%(asctime)s:%(levelname)s : File: %(filename)s : Line: %(lineno)d : %(message)s'}
         },
     'loggers':
         {
             'all':
                 {
                     'handlers': ['console', 'error_console', 'debug_console'],
                     'propagate': False
                 }
         },
     'handlers':
         {
               'console':
                  {
                      'class': 'logging.StreamHandler',
                      'level': 'INFO',
                      'formatter': 'detail',
                      'stream': 'ext://sys.stdout'
                  },
              'error_console':
                  {
                      'class': 'logging.StreamHandler',
                      'level': 'ERROR',
                      'formatter': 'detail',
                      'stream': 'ext://sys.stdout'
                  },
              'debug_console':
                  {
                      'class': 'logging.StreamHandler',
                      'level': 'DEBUG',
                      'formatter': 'detail',
                      'stream': 'ext://sys.stdout'
                  }
         },
     'root':
         {
             'level': 'NOTSET',
             'handlers': ['console'],
             'propagate': True
          }
}
