from chaoslib.exceptions import InterruptExecution
from logzero import logger
from msrestazure import azure_cloud

AZURE_CHINA_CLOUD = "AZURE_CHINA_CLOUD"
AZURE_GERMAN_CLOUD = "AZURE_GERMAN_CLOUD"
AZURE_PUBLIC_CLOUD = "AZURE_PUBLIC_CLOUD"
AZURE_US_GOV_CLOUD = "AZURE_US_GOV_CLOUD"


def get_or_raise(value: str = "AZURE_PUBLIC_CLOUD") -> azure_cloud.Cloud:
    """ Returns the proper Azure cloud object or raises
     an InterruptException if not found """

    if not value:
        logger.warn("Azure cloud not provided. Using"
                    " AZURE_PUBLIC_CLOUD as default")
        return azure_cloud.AZURE_PUBLIC_CLOUD

    cloud = value.strip().upper()

    if cloud == AZURE_PUBLIC_CLOUD:
        result = azure_cloud.AZURE_PUBLIC_CLOUD
    elif cloud == AZURE_CHINA_CLOUD:
        result = azure_cloud.AZURE_CHINA_CLOUD
    elif cloud == AZURE_US_GOV_CLOUD:
        result = azure_cloud.AZURE_US_GOV_CLOUD
    elif cloud == AZURE_GERMAN_CLOUD:
        result = azure_cloud.AZURE_GERMAN_CLOUD

    else:
        msg = "Invalid Azure cloud '{}'. Please " \
              "provide a proper cloud value".format(cloud)
        logger.info(msg)
        raise InterruptExecution(msg)

    return result
