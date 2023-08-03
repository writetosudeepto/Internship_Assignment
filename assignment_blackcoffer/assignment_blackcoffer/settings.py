BOT_NAME = 'assignment_blackcoffer'
SPIDER_MODULES = ['assignment_blackcoffer.spiders']
NEWSPIDER_MODULE = 'assignment_blackcoffer.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'assignment_blackcoffer.pipelines.SaveToFilePipeline': 1,
}
LOG_ENABLED = True
# Set to the desired log level (DEBUG, INFO, WARNING, ERROR, or CRITICAL)
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'scrapy.log'  # Specify the log file name (optional)
