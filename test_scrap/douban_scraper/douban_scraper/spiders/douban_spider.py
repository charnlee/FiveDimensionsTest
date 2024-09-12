import scrapy

class DoubanSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 选择每部电影的容器
        movies = response.xpath('//div[@class="item"]')

        # 遍历每部电影并提取信息
        for movie in movies:
            title = movie.xpath('.//div[@class="hd"]/a/span[@class="title"]/text()').get()

            rating = movie.xpath('.//div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').get()

            link = movie.xpath('.//div[@class="hd"]/a/@href').get()

            year = movie.xpath('.//div[@class="bd"]/p/text()').re_first(r'\d{4}')

            quote = movie.xpath('.//span[@class="inq"]/text()').get()

            yield {
                'Title': title,
                'Rating': rating,
                'Year': year,
                'Quote': quote,
                'Link': link
            }

        next_page = response.xpath('//span[@class="next"]/a/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
