# coding: utf8
from django.db import models


class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name

    title = models.CharField('书名', max_length=200)
    subtitle = models.CharField('副标题', max_length=200, blank=True)
    rating = models.FloatField('评分', blank=True)
    author = models.CharField('作者', max_length=60)
    translator = models.CharField('译者', max_length=60, blank=True)
    pubdate = models.CharField('出版日期', max_length=60, blank=True)
    price = models.CharField('定价', max_length=60, blank=True)
    publisher = models.CharField('出版社', max_length=200, blank=True)
    pages = models.IntegerField('页数', blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    cover_img = models.URLField('封面图', blank=True)
    summary = models.TextField('内容简介', blank=True, max_length=2000)
    author_intro = models.TextField('作者简介', blank=True, max_length=2000)

    #@property无效语句,使用会报错
    def __unicode__(self):
        return self.title


class CrawlURL(models.Model):
    class Meta:
        verbose_name = '抓取'
        verbose_name_plural = verbose_name
    url = models.URLField('抓取地址', max_length=100, unique=True)
    weight = models.SmallIntegerField('抓取深度', default=0)  # 抓取深度起始1
    is_save = models.BooleanField('是否已保存', default=False)  #
    date = models.DateTimeField('保存时间', auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return self.url