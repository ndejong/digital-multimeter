# Supported Multimeters 

The DigitalMultimeter Python module and accompanying `dmm` command-line tool have been 
written to accommodate the addition of new digital multimeter protocols in the future.

Two fantastic references for multimeter brands, models and their associated protocols:-

* [Sigrok](https://sigrok.org/wiki/Multimeter_comparison)
* [QtDMM2](http://www.mtoussaint.de/qtdmm2.html)

If you are willing to implement an additional protocol please do get in [contact](../project) or just submit a 
pull request!


| Brand     | Model     | `--model` parameter | Protocol               | Notes                                                                               |
|-----------|-----------|---------------------|------------------------|-------------------------------------------------------------------------------------|
| -         | -         | `Default`           | FortuneFS9721          | -                                                                                   |
| Digitec   | DT9604    | `Digitec_DT9604`    | MultimeterEDI9604      | Reverse Engineered                                                                  |
| Digitech  | QM1538    | `Digitech_QM1538`   | FortuneFS9721          | Reference [cdmm](http://www.mtoussaint.de/cdmm/doc/index.html)                      |
| Digitek   | DT4000ZC  | `Digitek_DT4000ZC`  | FortuneFS9721          | Reference [Sigrok](https://sigrok.org/wiki/Digitek_DT4000ZC)                        |
| Editronic | EDI9604   | `Editronic_EDI9604` | MultimeterEDI9604      | Reverse Engineered                                                                  |
| PCE       | PCEDM32   | `PCE_PCEDM32`       | FortuneFS9721          | Reference [Sigrok](https://sigrok.org/wiki/Multimeter_comparison)                   |
| Tecpel    | DMM8062   | `Tecpel_DMM8062`    | FortuneFS9721          | Product [website](http://www.tecpel.net/multimeter-dmm8062.html)                    |
| TekPower  | TP4000ZC  | `TekPower_TP4000ZC` | FortuneFS9721          | Product [website](https://tekpower.us/multimeter/digital-multimeters/tp4000zc.html) |
| UniTrend  | UT30A     | `UniTrend_UT30A`    | FortuneFS9721          | Reference [cdmm](http://www.mtoussaint.de/cdmm/doc/index.html)                      |
| UniTrend  | UT30E     | `UniTrend_UT30E`    | FortuneFS9721          | Reference [cdmm](http://www.mtoussaint.de/cdmm/doc/index.html)                      |
| UniTrend  | UT60E     | `UniTrend_UT60E`    | FortuneFS9721          | Reference [Sigrok](https://sigrok.org/wiki/UNI-T_UT60E)                             |
| Voltcraft | VC820     | `Voltcraft_VC820`   | FortuneFS9721          | Reference [Sigrok](https://sigrok.org/wiki/Voltcraft_VC-820)                        |
| Voltcraft | VC840     | `Voltcraft_VC840`   | FortuneFS9721          | Reference [Sigrok](https://sigrok.org/wiki/Voltcraft_VC-840)                        |
| Voltcraft | VC870     | `Voltcraft_VC870`   | MultimeterVC870USBHID  | NA                                                                                  |
