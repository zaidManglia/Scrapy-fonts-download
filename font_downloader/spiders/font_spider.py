import scrapy

class FontSpider(scrapy.Spider):
    name = "font_spider"
    start_urls = [
        "https://www.1001fonts.com/signature-fonts.html"  # Add your desired starting URL here
    ]

    def parse(self, response):
        for font_link in response.css('a::attr(href)').getall():
            if font_link.endswith('.ttf') or font_link.endswith('.otf'):
                yield scrapy.Request(response.urljoin(font_link), callback=self.save_font)

        for next_page in response.css('a::attr(href)').getall():
            yield response.follow(next_page, callback=self.parse)

    def save_font(self, response):
        # Extract the font file name from the URL
        font_name = response.url.split('/')[-1]

        # Save the font file
        with open(font_name, 'wb') as font_file:
            font_file.write(response.body)
        self.log(f"Font '{font_name}' saved.")
