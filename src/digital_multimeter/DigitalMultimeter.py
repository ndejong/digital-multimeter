
import logging
from digital_multimeter.multimeters import multimeter_models
from digital_multimeter.exceptions.MultimeterException import MultimeterException


logger = logging.getLogger(__name__)


class DigitalMultimeter:
    """
    Implements an interface to various digital multimeters
    """

    connect = None
    model = None
    multimeter = None

    def __init__(self, connect=None, model='Default'):
        """
        NB: Connection to the digital multimeter does not occur until required in a `get_reading()` call.

        _parameters_
        * _connect_ (str) - the connection to the digital multimeter, for example `/dev/ttyUSB0`
        * _model_ (str) default: `Default` - the digital multimeter model to use for this connection; check models
        supported for a list of supported.  Model names are case sensitive.
        """
        self.connect = connect
        if model not in multimeter_models.keys():
            raise MultimeterException('Multimeter model not supported', model)
        self.model = model

    def get_reading(self):
        """
        Load the digital multimeter and establish a connection if required, then get a reading of the instrument
        and return.
        """
        if not self.multimeter:
            self.__load_multimeter()
        return getattr(self.multimeter, 'get_reading')()

    def __load_multimeter(self):
        if self.multimeter:
            return
        class_name = multimeter_models[self.model]
        logger.debug('Digital multimeter model: {}'.format(self.model))
        logger.debug('Loading digital multimeter class: {}'.format(class_name))
        module = __import__('digital_multimeter.multimeters.{}'.format(class_name), fromlist=['digital_multimeter'])
        self.multimeter = getattr(module, class_name)(connect=self.connect)

    def get_models_supported(self):
        """
        Returns a list of the supported digital multimeter models.
        """
        return {'models': list(multimeter_models.keys())}
