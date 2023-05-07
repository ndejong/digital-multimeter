#
# Digital Multimeter models
#
# The __multimeter_models__ dict maps DMM product-models to their chipset implementations as
# code, thus making it possible to map multiple products to the same chipsets
#
# References:
#  - MultimeterFortuneFS9721 https://www.ic-fortune.com/upload/Download/FS9721_LP3-DS-21_EN.pdf
#  - MultimeterVC870USBHID ??
#  - MultimeterEDI9604 ??
#

__multimeter_models__ = {
    "Default": "MultimeterFortuneFS9721",
    "Digitec_DT9604": "MultimeterEDI9604",
    "Digitech_QM1538": "MultimeterFortuneFS9721",
    "Digitek_DT4000ZC": "MultimeterFortuneFS9721",
    "Editronic_EDI9604": "MultimeterEDI9604",
    "PCE_PCEDM32": "MultimeterFortuneFS9721",
    "Tecpel_DMM8062": "MultimeterFortuneFS9721",
    "TekPower_TP4000ZC": "MultimeterFortuneFS9721",
    "UniTrend_UT30A": "MultimeterFortuneFS9721",
    "UniTrend_UT30E": "MultimeterFortuneFS9721",
    "UniTrend_UT60E": "MultimeterFortuneFS9721",
    "Voltcraft_VC820": "MultimeterFortuneFS9721",
    "Voltcraft_VC840": "MultimeterFortuneFS9721",
    "Voltcraft_VC870": "MultimeterVC870USBHID",
}
