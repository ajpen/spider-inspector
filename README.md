Inspectr
----------------

Inspectr is a scrapy downloader middleware that allows real-time viewing of requests/responses as they
are scheduled/downloaded/dropped.


Installation
---------------

1. Clone the repository.
2. `cd spider-inspector`
3. `python setup.py install`


Usage
--------------

1. After installing, add the following to your extensions:

    `"inspectr.Inspectr": 500`


2. Add the following setting:

  `INSPECTR_ENABLED=True`

Be sure to adjust the middleware order if you need to. It is recommended that Inspectr is the last middleware executed.

Optionally, you can set Inspectr to automatically its client:

   `INSPECTR_AUTOSTART=True`


The host address and port can be adjusted by setting `INSPECTR_HOST` and `INSPECTR_PORT` respectively:using the following settings