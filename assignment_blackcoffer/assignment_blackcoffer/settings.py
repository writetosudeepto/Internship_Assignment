BOT_NAME = 'assignment_blackcoffer'
SPIDER_MODULES = ['assignment_blackcoffer.spiders']
NEWSPIDER_MODULE = 'assignment_blackcoffer.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'assignment_blackcoffer.pipelines.SaveToFilePipeline': 1,
}
